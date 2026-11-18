import unittest
from copy import deepcopy

from engine import CHI, analyze, validate, tat_dai_van
from interpretation import BODY_B, baseline, baseline_report
from seed import CHARTS, RULES


class BaselineTests(unittest.TestCase):
    def test_fourteen_stars_are_covered(self):
        self.assertEqual(len(BODY_B), 14)

    def test_existing_examples(self):
        for ch in CHARTS.values():
            self.assertTrue(validate(ch))
            b = baseline(ch)
            self.assertTrue(b["tat_body"])
            self.assertTrue(b["nature"])
            self.assertTrue(b["visible_nature"])
            self.assertEqual(b["dv_tat"], tat_dai_van(ch["dv"]))
            self.assertIn("I. TẬT ÁCH NGUYÊN CỤC", baseline_report(ch))

    def test_new_chart_thien_tuong_with_hao_tuan(self):
        new = {
            "person": "Lá số thử V2",
            "menh": "Mão", "tat": "Tuất", "dv": "Dậu",
            "houses": {x: [] for x in CHI}
        }
        new["houses"]["Mão"] = ["Thiên Đồng (H)", "Thanh Long", "Long Trì"]
        new["houses"]["Tuất"] = ["Thiên Tướng (Đ)", "Đại Hao (H)", "Trực Phù",
                                    "Thiên Sứ", "Tuần"]
        self.assertTrue(validate(new))
        b = baseline(new)
        self.assertTrue(any(x["title"] == "Thiên Tướng" for x in b["tat_body"]))
        self.assertTrue(any(x["title"] == "Đại Hao" for x in b["tat_health"]))
        self.assertTrue(any(x["title"] == "Tuần / Triệt" for x in b["tat_modifiers"]))
        self.assertTrue(any(x["title"] == "Thiên Tướng" for x in b["nature"]))
        self.assertTrue(any(x["title"] == "Thiên Đồng" for x in b["visible_nature"]))
        self.assertEqual(b["dv_tat"], "Mão")
        # Không có cách đặc biệt vẫn phải cho phép tạo phần nền tảng.
        empty_special = analyze(new, RULES)["matches"]
        self.assertIsInstance(empty_special, list)
        report = baseline_report(new)
        self.assertIn("Thiên Tướng", report)
        self.assertIn("Đại Hao", report)
        self.assertIn("TẬT ÁCH NGUYÊN CỤC", report)

    def test_no_fabricated_disease_if_only_body_association(self):
        new = deepcopy(CHARTS["giapty"])
        new["houses"]["Tý"] = ["Thiên Tướng (Đ)"]
        b = baseline(new)
        self.assertEqual(b["tat_body"][0]["title"], "Thiên Tướng")
        self.assertEqual(b["tat_health"], [])
        self.assertEqual(b["tat_ach"], [])
        self.assertIn("Để thành cách chỉ bệnh", b["tat_body"][0]["text"])


if __name__ == "__main__":
    unittest.main()
