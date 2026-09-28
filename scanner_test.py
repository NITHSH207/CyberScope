import unittest

from scanner.nmap_scanner import build_arguments
from scanner.validator import is_allowed_target


class CyberScopeScannerTests(unittest.TestCase):
    def test_default_scan_uses_tcp_connect(self):
        self.assertIn("-sT", build_arguments([]))

    def test_syn_option(self):
        args = build_arguments(["syn"])
        self.assertIn("-sS", args)
        self.assertNotIn("-sT", args)

    def test_service_and_os_options(self):
        args = build_arguments(["tcp", "version", "os"])
        self.assertIn("-sT", args)
        self.assertIn("-sV", args)
        self.assertIn("-O", args)

    def test_aggressive_option(self):
        self.assertIn("-A", build_arguments(["aggressive"]))

    def test_local_targets_are_allowed(self):
        self.assertTrue(is_allowed_target("localhost"))
        self.assertTrue(is_allowed_target("127.0.0.1"))

    def test_public_target_is_rejected(self):
        self.assertFalse(is_allowed_target("8.8.8.8"))


if __name__ == "__main__":
    unittest.main()
