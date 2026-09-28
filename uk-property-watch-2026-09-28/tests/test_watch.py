import tempfile
import unittest
from pathlib import Path
from openpyxl import load_workbook
from watch import evaluate, fingerprint, key, workbook


class WatchTests(unittest.TestCase):
    def test_cross_run_deduplication_and_change(self):
        base = {"area": "Caversham", "address": "1 Test Road", "postcode": "RG4 0AA", "url": "https://example.com/1", "price": 700000, "detached": True, "bedrooms": 3}
        rows, accepted, rejected, counts = evaluate([base, dict(base, url="https://another.example/2")], {})
        self.assertEqual((counts["skimmed"], counts["new"], len(rejected)), (1, 1, 1))
        history = {key(base): {"fingerprint": fingerprint(base)}}
        _, _, rejected, counts = evaluate([base], history)
        self.assertEqual((counts["unchanged"], len(rejected)), (1, 0))
        changed = dict(base, price=690000)
        _, _, rejected, counts = evaluate([changed], history)
        self.assertEqual((counts["changed"], counts["new"], len(rejected)), (1, 0, 0))

    def test_workbook_hyperlink(self):
        p = {"area": "Earley", "title": "Test", "url": "https://example.com/listing", "detached": False}
        _, _, rejected, _ = evaluate([p], {})
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "rejected.xlsx"
            workbook(path, rejected, "2026-09-28")
            self.assertEqual(load_workbook(path).active["H2"].hyperlink.target, p["url"])


if __name__ == "__main__":
    unittest.main()
