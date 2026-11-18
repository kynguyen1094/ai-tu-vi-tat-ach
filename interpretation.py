"""Luận nền tảng dựa trên hai tài liệu người dùng cung cấp.
A: 'Các cách chỉ bệnh tật trong Tử Vi' (ưu tiên về bệnh lý).
B: 'Cung Tật Ách: Bản chất, bệnh lý và các yếu tố liên quan'.
Trình bày theo nghĩa cổ thư, không chẩn đoán hoặc dự báo chắc chắn.
"""
from engine import normalize, relations, tat_dai_van

SOURCE_A = "Các cách chỉ bệnh tật trong Tử Vi"
SOURCE_B = "Cung Tật Ách: Bản chất, bệnh lý và các yếu tố liên quan"

# Bảng sao–tạng phủ: trích ý theo bảng 4 của tài liệu B, KHÔNG phải bệnh đã xác định.
BODY_B = {
    "Tử Vi": "tỳ vị, hệ tiêu hóa",
    "Thiên Cơ": "gan, mật và nội tiết",
    "Thái Dương": "tim, tuần hoàn và thần kinh",
    "Vũ Khúc": "phổi, khí quản và hô hấp",
    "Thiên Đồng": "bàng quang và hệ bài tiết",
    "Liêm Trinh": "hệ tuần hoàn",
    "Thiên Phủ": "miệng và khoang miệng",
    "Thái Âm": "thận, hệ sinh dục và miễn dịch",
    "Tham Lang": "gan và nội tiết",
    "Cự Môn": "hệ tiêu hóa và khoang miệng",
    "Thiên Tướng": "mật và hệ bài tiết",
    "Thiên Lương": "tuyến vú",
    "Thất Sát": "hệ hô hấp",
    "Phá Quân": "thận",
}

# Tính cách: chỉ những sao được mô tả trực tiếp tại Tật trong bảng 0, tài liệu B.
NATURE_B = {
    "Tử Vi": "Theo tài liệu, khuynh hướng nhân hậu, hiền lành.",
    "Thiên Cơ": None,
    "Thái Dương": None,
    "Vũ Khúc": "Cương nghị, có phần cô độc trong nội tâm.",
    "Thiên Đồng": "Có phần bốc đồng; lương thiện nhưng hay thay đổi.",
    "Liêm Trinh": None,
    "Thiên Phủ": "Bao dung, hòa nhã, không muốn ép người khác đến đường cùng.",
    "Thái Âm": None,
    "Tham Lang": None,
    "Cự Môn": "Đa nghi, suy xét và tính toán nhiều.",
    "Thiên Tướng": None,
    "Thiên Lương": "Có phần kiêu kỳ nhưng lương thiện.",
    "Thất Sát": None,
    "Phá Quân": None,
}

# Sao phụ có luận Tật trực tiếp trong bảng tính cách B.
NATURE_SUPPORT_B = {
    "Thái Tuế": "Có chính kiến và đôi khi cố chấp.",
    "Quốc Ấn": "Đoan chính, ngay thẳng.",
    "Thiên Hình": "Cẩn thận, hơi tiểu tiết.",
    "Lộc Tồn": "Có xu hướng độc đoán, giữ kẽ.",
    "Hóa Kỵ": "Theo bảng cổ, có phần nhỏ nhen hoặc hay lo bị người khác tính toán.",
    "Văn Xương": "Nội tâm phong phú, thông minh, lãng mạn.",
    "Văn Khúc": "Nội tâm phong phú, thông minh, lãng mạn.",
    "Tả Phụ": "Có lòng trắc ẩn, thích giúp đỡ.",
    "Hữu Bật": "Có lòng trắc ẩn, thích giúp đỡ.",
    "Thanh Long": "Tài liệu liên hệ với sự nhạy bén về trực giác.",
    "Thiên Khôi": "Ham học, thích tìm hiểu nhiều bộ môn.",
    "Thiên Việt": "Ham học, thích tìm hiểu nhiều bộ môn.",
}

# Các lớp nghĩa có nguồn, tách khỏi bảng sao–tạng phủ.
MODIFIERS = {
    "Đại Hao": ("Tật", "Song Hao theo tài liệu A liên hệ tình trạng tiêu chảy, đau bụng hoặc rối loạn tiêu hóa; đây là cách luận cổ, không phải chẩn đoán.", SOURCE_A, "Mục 1 – Tiêu hóa"),
    "Tiểu Hao": ("Tật", "Song Hao theo tài liệu A liên hệ tình trạng tiêu chảy, đau bụng hoặc rối loạn tiêu hóa; đây là cách luận cổ, không phải chẩn đoán.", SOURCE_A, "Mục 1 – Tiêu hóa"),
    "Bệnh Phù": ("Tật", "Tài liệu A liên hệ Bệnh Phù với một số vấn đề dạ dày, dinh dưỡng và tiêu hóa.", SOURCE_A, "Mục 1 – Tiêu hóa"),
    "Bạch Hổ": ("Tật", "Bạch Hổ liên hệ huyết khí trong tài liệu A; cần phối hợp mới xét hình thái cụ thể.", SOURCE_A, "Mục 3 – Tuần hoàn"),
    "Tang Môn": ("Tật", "Tang Môn được nêu cùng Bạch Hổ trong nhóm sao liên hệ máu huyết.", SOURCE_A, "Mục 3 – Tuần hoàn"),
    "Địa Không": ("Ách", "Địa Không là sát tinh mạnh; cần xem phối hợp và địa vị, không tự chỉ đích danh tai họa.", SOURCE_A, "Mục 1 – Địa Không, Địa Kiếp"),
    "Địa Kiếp": ("Ách", "Địa Kiếp là sát tinh mạnh; cần xem phối hợp và địa vị, không tự chỉ đích danh tai họa.", SOURCE_A, "Mục 1 – Địa Không, Địa Kiếp"),
    "Thiên Hình": ("Ách", "Tài liệu A liên hệ Thiên Hình với khả năng mổ xẻ khi đi với bộ sao chỉ bệnh.", SOURCE_A, "Mục 1 – Thiên Hình, Kiếp Sát"),
    "Kiếp Sát": ("Ách", "Tài liệu A liên hệ Kiếp Sát với khả năng mổ xẻ khi đi với bộ sao chỉ bệnh.", SOURCE_A, "Mục 1 – Thiên Hình, Kiếp Sát"),
}

def stars_present(chart, chi):
    return {normalize(x) for x in chart["houses"].get(chi, [])}

def notes_at(chart, chi, viewpoint):
    names = stars_present(chart, chi)
    out = []
    for star in BODY_B:
        if normalize(star) in names:
            out.append({"type": "tạng phủ", "title": star,
                        "text": "Bảng sao–tạng phủ liên hệ với " + BODY_B[star] +
                        ". Để thành cách chỉ bệnh cần xét sao phối hợp và điều kiện cụ thể.",
                        "source": SOURCE_B, "section": "Bảng sao và tạng phủ"})
    for star, (kind, statement, source, section) in MODIFIERS.items():
        if normalize(star) in names and (viewpoint in ("gốc", "đại vận")):
            out.append({"type": kind, "title": star, "text": statement,
                        "source": source, "section": section})
    if "tuan" in names or "triet" in names:
        out.append({
            "type": "gia giảm", "title": "Tuần / Triệt",
            "text": "Theo tài liệu B, Tuần/Triệt có thể làm biến đổi hoặc giảm tác dụng hung tính của sao; không mặc nhiên hóa giải tất cả.",
            "source": SOURCE_B, "section": "1.2. Mệnh, Tật Ách và hạn vận"
        })
    return out

def nature_notes(chart, tat):
    names = stars_present(chart, tat)
    out = []
    for star, meaning in NATURE_B.items():
        if normalize(star) in names:
            out.append({"title": star, "text": meaning or
                        "Bảng tính cách của tài liệu B chưa có mô tả riêng cho sao này; không tự suy diễn thành nhận định tâm lý cụ thể.",
                        "source": SOURCE_B, "section": "Bảng tính cách qua Tật"})
    for star, meaning in NATURE_SUPPORT_B.items():
        if normalize(star) in names:
            out.append({"title": star, "text": meaning,
                        "source": SOURCE_B, "section": "Bảng tính cách qua Tật"})
    if "tuan" in names or "triet" in names:
        out.append({"title": "Tuần/Triệt", "text": "Cần xét khả năng làm đổi tính chất của cách cục khi luận bề chìm nội tâm.",
                    "source": SOURCE_B, "section": "1.2. Mệnh, Tật Ách và hạn vận"})
    return out

def baseline(chart):
    tat = chart["tat"]
    dv_tat = tat_dai_van(chart["dv"])
    tat_notes = notes_at(chart, tat, "gốc")
    dv_notes = notes_at(chart, dv_tat, "đại vận")
    return {
        "tat": tat, "dv_tat": dv_tat,
        "menh_stars": chart["houses"][chart["menh"]],
        "tat_stars": chart["houses"][tat],
        "dv_stars": chart["houses"][chart["dv"]],
        "dv_tat_stars": chart["houses"][dv_tat],
        "tat_body": [x for x in tat_notes if x["type"] == "tạng phủ"],
        "tat_health": [x for x in tat_notes if x["type"] == "Tật"],
        "tat_ach": [x for x in tat_notes if x["type"] == "Ách"],
        "tat_modifiers": [x for x in tat_notes if x["type"] == "gia giảm"],
        "nature": nature_notes(chart, tat),
        "dv_body": [x for x in dv_notes if x["type"] == "tạng phủ"],
        "dv_health": [x for x in dv_notes if x["type"] == "Tật"],
        "dv_ach": [x for x in dv_notes if x["type"] == "Ách"],
        "dv_modifiers": [x for x in dv_notes if x["type"] == "gia giảm"],
        "tat_relations": relations(tat),
        "dv_relations": relations(dv_tat),
        "source_note": "Ưu tiên nguồn A khi luận bệnh lý; nguồn B bổ sung bảng sao–tạng phủ, tính cách và Tuần/Triệt. Những điểm không có nguồn chưa được diễn giải."
    }

def baseline_report(chart):
    b = baseline(chart)
    lines = [
        "PHẦN LUẬN NỀN TẢNG – TẬT/ÁCH V2",
        "I. TẬT ÁCH NGUYÊN CỤC",
        "Tật gốc tại " + b["tat"] + ": " + ", ".join(b["tat_stars"]),
    ]
    for group in ("tat_body", "tat_health", "tat_modifiers"):
        for item in b[group]:
            lines += ["- " + item["title"] + ": " + item["text"],
                      "  Nguồn: " + item["source"] + " / " + item["section"]]
    lines += ["II. ÁCH NGUYÊN CỤC"]
    for item in b["tat_ach"]:
        lines += ["- " + item["title"] + ": " + item["text"]]
    if not b["tat_ach"]:
        lines.append("Không có dấu hiệu Ách riêng được kích hoạt trong lớp nền tảng; tiếp tục xét tam phương tứ chính và các cách chuyên biệt.")
    lines += ["III. TÍNH CÁCH QUA MỆNH – TẬT",
              "Mệnh tại " + chart["menh"] + ": " + ", ".join(b["menh_stars"]),
              "Tật tại " + b["tat"] + ": " + ", ".join(b["tat_stars"])]
    for item in b["nature"]:
        lines.append("- " + item["title"] + ": " + item["text"])
    lines += ["IV. ĐẠI VẬN",
              "Mệnh đại vận tại " + chart["dv"] + ": " + ", ".join(b["dv_stars"]),
              "Tật đại vận tại " + b["dv_tat"] + ": " + ", ".join(b["dv_tat_stars"])]
    for group in ("dv_body", "dv_health", "dv_ach", "dv_modifiers"):
        for item in b[group]:
            lines += ["- " + item["title"] + ": " + item["text"]]
    lines += ["V. NGUYÊN TẮC ĐỐI CHIẾU", b["source_note"],
              "Những quan hệ giáp cung/nhị hợp không tự động coi là đồng cung.",
              "Đây là nghiên cứu lý số truyền thống, không phải chẩn đoán y tế hoặc kết luận pháp lý."]
    return "\n".join(lines)
