import unittest
from deep_reading import build_context, deterministic_report, original_chart, split_layer, FORMULAS
from engine import CHI

class V3Tests(unittest.TestCase):
    def chart(self):
        # Cases structurally similar to the example; no real identifying data.
        c = {"menh":"Sửu","tat":"Thân","dv":"Dậu","houses":{x:["Bát Tọa"] for x in CHI}}
        c["houses"]["Sửu"]=["Thiên Phủ (B)","Ân Quang","Thiên Quý"]
        c["houses"]["Thân"]=["Kiếp Sát","Tướng Quân","Thiên Đức","L.Tang Môn"]
        c["houses"]["Dần"]=["Thiên Cơ (H)","Thái Âm (H)","Thiên Hình (Đ)"]
        c["houses"]["Tý"]=["Thái Dương (H)","Lộc Tồn"]
        c["houses"]["Thìn"]=["Cự Môn (H)","Linh Tinh (Đ)","Bệnh Phù","P.Hóa Khoa"]
        c["houses"]["Mão"]=["Hỏa Tinh (Đ)","Hóa Kỵ (H)"]
        c["houses"]["Tị"]=["Thiên Tướng (Đ)","Địa Không (Đ)","Địa Kiếp (Đ)"]
        return c

    def test_void_house_and_relations(self):
        x=build_context(self.chart())
        self.assertTrue(x["layers"]["tat"]["vo_chinh_dieu"])
        self.assertEqual(x["layers"]["dvtat"]["anchor"],"Thìn")
        self.assertIn("tam hợp",x["overlap"]["relations"])
        ev=x["layers"]["tat"]["evidence"]
        self.assertTrue(any(y["chi"]=="Dần" and y["relation"]=="xung chiếu" for y in ev))
        self.assertTrue(any(y["chi"]=="Tị" and y["relation"]=="nhị hợp" for y in ev))

    def test_prefix_handling(self):
        self.assertEqual(split_layer("Lưu Hà"),"original")
        for s in ["L.Bạch Hổ","LN.Văn Tinh","P.Hóa Khoa","ĐV.Hóa Lộc","Lưu Thiên Mã"]:
            self.assertEqual(split_layer(s),"other")
        x=original_chart(self.chart())
        self.assertNotIn("P.Hóa Khoa",x["houses"]["Thìn"])

    def test_source_priority(self):
        x=build_context(self.chart())
        eyes=[y for y in x["layers"]["tat"]["body"] if y["star"].startswith("Thái Dương")]
        self.assertTrue(eyes and eyes[0]["group"]=="mắt")
        self.assertTrue(eyes[0]["source"].startswith("A"))

    def test_relation_not_co_location(self):
        x=build_context(self.chart())
        f=[v for v in x["layers"]["tat"]["formulas"] if v["id"]=="A25"][0]
        self.assertIn("chưa xác nhận",f["status"])
        self.assertNotIn("cùng cung",f["status"])

    def test_report(self):
        x=build_context(self.chart())
        r=deterministic_report(x)
        for s in ["I. Cấu trúc và Tật nguyên cục","II. Ách nguyên cục","III. Tính cách","IV. Tật – Ách đại vận","V. Tổng hợp","Vô chính diệu","Sao lưu/phi hóa"]:
            self.assertIn(s,r)
        self.assertEqual(len(FORMULAS),26)

    def test_bad_anchor(self):
        c=self.chart();c["tat"]="Mão"
        with self.assertRaises(ValueError): build_context(c)

if __name__=="__main__":
    unittest.main()
