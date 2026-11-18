"""Dữ liệu minh họa và 21 quy tắc thử nghiệm. Không chứa hồ sơ người dùng thực."""
from engine import CHI, labels_for

def chart(title, menh, tat, dv, age, rows):
    houses = {c: [x.strip() for x in rows.get(c, "").split("|") if x.strip()] for c in CHI}
    return {"person": title, "menh": menh, "tat": tat, "dv": dv, "dvAge": age,
            "houses": houses, "houseLabels": labels_for(menh)}

CHARTS = {
 "giapty": chart("Nữ Giáp Tý 1984", "Tị", "Tý", "Sửu", "43–52", {
  "Tý":"Thất Sát (M)|Tả Phụ|Bát Tọa|Thanh Long|Thái Tuế|Thiên Sứ",
  "Sửu":"Thiên Khôi|Thiếu Dương|Lực Sĩ|Đà La (Đ)|Thiên Không",
  "Dần":"Liêm Trinh (V)|Hữu Bật|Hóa Lộc|Tang Môn (Đ)|Thiên Mã|Thiên Giải",
  "Mão":"Hồng Loan|Thiên Thọ|Địa Giải|Thiếu Âm|Kình Dương|Linh Tinh (Đ)|Quan Phù",
  "Thìn":"Phá Quân (Đ)|Hóa Quyền|Địa Kiếp (H)|Thiên La|Thiên Giải|Phục Binh",
  "Tị":"Thiên Đồng (Đ)|Văn Xương (M)|Thiên Hình (H)|Kiếp Sát|Phá Toái|Tử Phù|Đại Hao (H)|Nguyệt Đức|Thiên Trù",
  "Ngọ":"Vũ Khúc (V)|Thiên Phủ (M)|Hóa Khoa|Ân Quang|Địa Không (H)|Thiên Khốc|Thiên Hư|Thiên Phúc|Bệnh Phù",
  "Mùi":"Thái Dương (Đ)|Thái Âm (Đ)|Hóa Kỵ|Thiên Việt|Thiên Quan|Long Đức|Thiên Quý",
  "Thân":"Tham Lang (Đ)|Bạch Hổ (Đ)|Thiên Quý|Phi Liêm|Triệt",
  "Dậu":"Thiên Cơ (M)|Cự Môn (M)|Hỏa Tinh (H)|Thiên Diêu|Văn Khúc|Thiên Phúc",
  "Tuất":"Tử Vi (V)|Thiên Tướng (V)|Giải Thần|Phượng Các|Địa Võng|Điếu Khách",
  "Hợi":"Thiên Lương (H)|Tiểu Hao (H)|Trực Phù"
 }),
 "kymui": chart("Nam Kỷ Mùi 1979", "Mùi", "Dần", "Mão", "45–54", {
  "Tý":"Thiên Đồng (V)|Thái Âm (V)|Thiên Khôi|Đào Hoa|Thiên Hư",
  "Sửu":"Vũ Khúc (M)|Tham Lang (M)|Linh Tinh (H)|Hóa Lộc|Hóa Quyền|Tuế Phá",
  "Dần":"Thái Dương (V)|Cự Môn (V)|Địa Kiếp (H)|Long Đức|Hữu Bật|Thiên Phúc|Quốc Ấn|Thiên Tài|Tướng Quân|Đẩu Quân",
  "Mão":"Thiên Tướng (H)|Bạch Hổ (Đ)|Tiểu Hao (Đ)|Giải Thần|Địa Giải|Phượng Các|Bát Tọa",
  "Thìn":"Thiên Cơ (M)|Thiên Lương (M)|Hóa Khoa|Thiên Đức|Thiên Giải|Phúc Đức",
  "Tị":"Tử Vi (M)|Thất Sát (V)|Thiên Hình (H)|Ân Quang|Thiên Mã",
  "Ngọ":"Hỏa Tinh (Đ)|Lộc Tồn|Bác Sĩ|Lưu Hà",
  "Mùi":"Văn Xương (Đ)|Văn Khúc (Đ)|Hoa Cái|Quan Phù|Thái Tuế|Hóa Kỵ|Kình Dương|Mộc Dục",
  "Thân":"Địa Không (H)|Thiên Không|Kiếp Sát|Phục Binh|Cô Thần|Thiên Việt|Thiên Thọ|Thiên Trù",
  "Dậu":"Liêm Trinh (H)|Phá Quân (H)|Tang Môn (Đ)|Thiên Riêu (Đ)|Đại Hao (H)",
  "Tuất":"Bệnh Phù|Địa Võng|Thiếu Âm",
  "Hợi":"Thiên Phủ (Đ)|Quan Phù|Thiên Khốc|Long Trì|Tam Thai"
 }),
}

def rule(ident, kind, group, title, target, requirements, result, source, page, any_of=False):
    return {"id": ident, "kind": kind, "group": group, "title": title,
            "target": target, "any" if any_of else "req": requirements,
            "result": result, "source": source, "page": page}

TAT = "tam phương tứ chính"
TOA = "tọa thủ"
GIA = "giáp"
NHI = "nhị hợp"
TAM = "tam hợp"
XUNG = "xung chiếu"

RULES = [
 rule("B01","Tật","hô hấp","Thất Sát hội Không – Kiếp","tat",
      [("Thất Sát",TOA),("Địa Không",TAT),("Địa Kiếp",TAT)],
      "Cách cục cổ truyền liên hệ phế khí, ho và yếu phổi; không đồng nghĩa mắc bệnh cụ thể.","A; C","C, tr. 325"),
 rule("B02","Tật","tiêu hóa","Thiên Đồng – Hóa Kỵ","tat",
      [("Thiên Đồng",TAT),("Hóa Kỵ",TAT)],
      "Dấu hiệu cổ truyền về trục trặc tiêu hóa; cần xét quan hệ phối sao cụ thể.","A","Mục bệnh tiêu hóa"),
 rule("B03","Tật","huyết khí","Tang Môn – Bạch Hổ","tat",
      [("Tang Môn",TAT),("Bạch Hổ",TAT)],
      "Bộ sao được quy chiếu về huyết khí trong phép luận truyền thống.","A","Mục bệnh máu huyết"),
 rule("B04","Tật","dao kéo","Thiên Hình – Kiếp Sát","tat",
      [("Thiên Hình",TAT),("Kiếp Sát",TAT)],
      "Tổ hợp liên hệ mổ xẻ, dao kéo khi hội đủ điều kiện phối sao.","A","Các bộ sao chỉ mổ xẻ"),
 rule("B05","Tật","hô hấp","Vũ Khúc – Thất Sát","tat",
      [("Vũ Khúc",TAT),("Thất Sát",TAT)],
      "Bộ sao cổ truyền được liên hệ các bệnh thuộc phổi và hô hấp.","A","Mục bệnh hô hấp"),
 rule("B06","Tật","tâm tính","Cự Môn tọa thủ Tật","tat",
      [("Cự Môn",TOA)],
      "Nội tâm có khuynh hướng đa nghi, suy xét, thích phân tích và phản biện.","B","Phần tính cách qua Tật"),
 rule("B07","Tật","tâm tính","Thái Tuế tọa thủ Tật","tat",
      [("Thái Tuế",TOA)],
      "Nội tâm có chính kiến mạnh, đôi khi cố chấp và muốn bảo vệ quan điểm.","B","Phần tính cách qua Tật"),
 rule("B08","Tật","tâm tính","Tả Phụ hoặc Hữu Bật tọa thủ Tật","tat",
      [("Tả Phụ",TOA),("Hữu Bật",TOA)],
      "Có lòng trắc ẩn và thiên hướng giúp đỡ người khác.","B","Phần tính cách qua Tật",True),
 rule("B09","Tật","tâm tính","Thiên Đồng tọa thủ Tật","tat",
      [("Thiên Đồng",TOA)],
      "Nội tâm thiên thiện lương nhưng dễ thay đổi cảm xúc.","B","Phần tính cách qua Tật"),
 rule("B10","Tật","tâm tính","Vũ Khúc tọa thủ Tật","tat",
      [("Vũ Khúc",TOA)],
      "Nội tâm cương nghị, độc lập và có phần cô độc.","B","Phần tính cách qua Tật"),
 rule("A01","Ách","tai nạn","Không – Kiếp hội Tật","tat",
      [("Địa Không",TAT),("Địa Kiếp",TAT)],
      "Cách cổ truyền liên hệ tai họa bất ngờ; chưa đủ điều kiện chỉ đích danh loại tai nạn.","A; C","Phần Giải Ách"),
 rule("A02","Ách","thương tích","Hình – Kiếp Sát hội Tật","tat",
      [("Thiên Hình",TAT),("Kiếp Sát",TAT)],
      "Dấu hiệu thương tích, dao kéo hoặc can thiệp ngoại khoa trong cách luận cổ.","A","Các bộ sao chỉ mổ xẻ"),
 rule("A03","Ách","tranh chấp","Cự Môn – Quan Phù","tat",
      [("Cự Môn",TAT),("Quan Phù",TAT)],
      "Nhóm sao liên quan khẩu thiệt và tranh chấp; phải đối chiếu điều kiện thành cách.","C","tr. 625–627"),
 rule("A04","Ách","tranh chấp","Quan Phù – Hóa Kỵ","tat",
      [("Quan Phù",TAT),("Hóa Kỵ",TAT)],
      "Gợi nhóm tranh chấp hoặc vướng mắc pháp lý trong phép luận truyền thống.","C","tr. 625–627; nhóm cách"),
 rule("E01","Đối chiếu mở rộng","giáp/nhị hợp","Hỏa giáp Mệnh, Linh xung Mệnh","menh",
      [("Hỏa Tinh",GIA),("Linh Tinh",XUNG)],
      "Giả thuyết phối hợp hai quan hệ; không phải Hỏa – Linh cùng giáp Mệnh.","Kinh nghiệm đối chiếu","Trường hợp bỏng nước"),
 rule("E02","Đối chiếu mở rộng","giáp/nhị hợp","Đà La nhị hợp Tật","tat",
      [("Đà La",NHI)],
      "Lớp sao bổ sung từ nhị hợp; không phải Đà La tọa thủ Tật.","Phương pháp nghiên cứu","Quy tắc nhị hợp"),
 rule("E03","Đối chiếu mở rộng","giáp/nhị hợp","Hỏa Tinh giáp Tật đại vận","dvtat",
      [("Hỏa Tinh",GIA)],
      "Xét tác động giáp biên; chưa đủ để xác định riêng một tai họa.","Phương pháp nghiên cứu","Quy tắc giáp cung"),
 rule("E04","Đối chiếu mở rộng","giáp/nhị hợp","Hình – Kiếp Sát nhị hợp Tật đại vận","dvtat",
      [("Thiên Hình",NHI),("Kiếp Sát",NHI)],
      "Bộ sao ở cung nhị hợp là tầng phụ trợ, không phải đồng cung Tật đại vận.","A; phương pháp nghiên cứu","Nhóm mổ xẻ; quy tắc nhị hợp"),
 rule("D01","Tật đại vận","huyết khí","Bạch Hổ tọa thủ Tật đại vận","dvtat",
      [("Bạch Hổ",TOA)],
      "Nhấn mạnh nhóm huyết khí và thương tích ở cung Tật của đại vận.","A","Mục bệnh máu huyết"),
 rule("D02","Tật đại vận","tai nạn","Địa Kiếp tam hợp Tật đại vận","dvtat",
      [("Địa Kiếp",TAM)],
      "Sát tinh hội về Tật đại vận; cần xét thêm sao khác để luận loại tai họa.","A; C","Các cách Không – Kiếp"),
 rule("D03","Tật đại vận","tranh chấp","Quan Phù tam hợp Tật đại vận","dvtat",
      [("Quan Phù",TAM)],
      "Dấu hiệu thị phi hoặc quan tụng, chưa đủ thành cách pháp lý riêng biệt.","C","tr. 625–627"),
]
assert len(RULES) == 21
