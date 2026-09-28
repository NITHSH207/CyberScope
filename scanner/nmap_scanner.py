import nmap

ALLOWED_OPTIONS = {"tcp", "udp", "syn", "version", "os", "aggressive"}


def _extract_os(host_data):
    """Return the best OS guess reported by Nmap, if available."""
    matches = host_data.get("osmatch", []) or []
    if not matches:
        return "Not detected"
    best = matches[0]
    name = best.get("name", "Unknown OS")
    accuracy = best.get("accuracy")
    return f"{name} ({accuracy}% match)" if accuracy else name


def build_arguments(options):
    """Build Nmap arguments from the UI's limited, explicit scan options."""
    selected = set(options or []) & ALLOWED_OPTIONS
    args = []

    # TCP connect is the safe default. If SYN is selected, use SYN rather than
    # sending both TCP scan types, which are mutually exclusive.
    if "syn" in selected:
        args.append("-sS")
    elif "tcp" in selected or not ({"tcp", "udp"} & selected):
        args.append("-sT")

    if "udp" in selected:
        args.append("-sU")
    if "version" in selected:
        args.append("-sV")
    if "os" in selected:
        args.append("-O")
    if "aggressive" in selected:
        args.append("-A")

    args.extend(["-T3", "--top-ports", "1000"])
    return " ".join(args)


def run_service_scan(target, options=None):
    """Run an authorized local/private Nmap scan using selected UI options."""
    arguments = build_arguments(options)
    scanner = nmap.PortScanner()

    try:
        scanner.scan(hosts=target, arguments=arguments)
        scan_error = ""
    except nmap.PortScannerError as error:
        # Privileged options can fail on unprivileged hosts. Keep the app
        # usable by falling back to a non-privileged TCP service scan.
        fallback_arguments = "-sT -sV --version-light -T3 --top-ports 1000"
        scanner = nmap.PortScanner()
        scanner.scan(hosts=target, arguments=fallback_arguments)
        arguments = fallback_arguments
        scan_error = (
            f"Requested scan could not run with current privileges; "
            f"fallback TCP service scan was used. ({error})"
        )

    result = {
        "hosts": [],
        "services": [],
        "scan_arguments": arguments,
        "scan_note": scan_error,
    }

    for host in scanner.all_hosts():
        host_data = scanner[host]
        result["hosts"].append(
            {
                "address": host,
                "hostname": host_data.hostname(),
                "state": host_data.state(),
                "os": _extract_os(host_data),
            }
        )

        for protocol in host_data.all_protocols():
            for port in sorted(host_data[protocol].keys()):
                item = host_data[protocol][port]
                result["services"].append(
                    {
                        "host": host,
                        "protocol": protocol.upper(),
                        "port": port,
                        "state": item.get("state", "unknown"),
                        "name": item.get("name", "unknown"),
                        "product": item.get("product", ""),
                        "version": item.get("version", ""),
                        "extrainfo": item.get("extrainfo", ""),
                    }
                )

    return result
