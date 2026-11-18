import unittest
from engine import CHI, analyze, relations, tat_dai_van, validate
from seed import CHARTS, RULES

class Tests(unittest.TestCase):
    def test_12_palaces(self):
        for c in CHARTS.values():
            self.assertTrue(validate(c))
            self.assertEqual(set(c["houses"]), set(CHI))

    def test_dai_van(self):
        self.assertEqual(tat_dai_van("Sửu"), "Thân")
        self.assertEqual(tat_dai_van("Mão"), "Tuất")

    def test_nhi_hop(self):
        self.assertEqual(relations("Dần")["nhị hợp"], ["Hợi"])
        self.assertEqual(relations("Mão")["nhị hợp"], ["Tuất"])

    def test_giap(self):
        self.assertEqual(relations("Mùi")["giáp"], ["Ngọ", "Thân"])

    def test_rule_results(self):
        for c in CHARTS.values():
            a = analyze(c, RULES)
            self.assertGreater(len(a["matches"]), 0)
            self.assertTrue(all(x["details"] for x in a["matches"]))

    def test_rule_count(self):
        self.assertEqual(len(RULES), 21)

if __name__ == "__main__":
    unittest.main()
