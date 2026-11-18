"""Bộ máy quy tắc Tật–Ách. Không dùng AI để tự tạo sao hoặc cách cục."""
import re
import unicodedata

CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tị", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
NHI = dict(zip(CHI, ["Sửu", "Tý", "Hợi", "Tuất", "Dậu", "Thân", "Mùi", "Ngọ", "Tị", "Thìn", "Mão", "Dần"]))
HOUSE_ORDER = ["Mệnh", "Phụ Mẫu", "Phúc Đức", "Điền Trạch", "Quan Lộc", "Nô Bộc",
               "Thiên Di", "Tật Ách", "Tài Bạch", "Tử Tức", "Phu Thê", "Huynh Đệ"]

def offset(chi, n):
    return CHI[(CHI.index(chi) + n) % 12]

def labels_for(menh):
    return {offset(menh, i): label for i, label in enumerate(HOUSE_ORDER)}

def relations(chi):
    return {
        "tọa thủ": [chi],
        "tam hợp": [offset(chi, 4), offset(chi, 8)],
        "xung chiếu": [offset(chi, 6)],
        "giáp": [offset(chi, -1), offset(chi, 1)],
        "nhị hợp": [NHI[chi]],
        "tam phương tứ chính": [chi, offset(chi, 4), offset(chi, 8), offset(chi, 6)],
    }

def tat_dai_van(dv_menh):
    """Tật Ách là cung thứ 8 tính từ Mệnh đại vận; offset +7 địa chi."""
    return offset(dv_menh, 7)

def normalize(value):
    x = re.sub(r"\([^)]*\)", "", str(value))
    x = unicodedata.normalize("NFD", x).replace("đ", "d").replace("Đ", "D")
    x = "".join(c for c in x if unicodedata.category(c) != "Mn")
    return " ".join(re.sub(r"[-_.]+", " ", x).casefold().split())

def validate(chart):
    for key in ("menh", "tat", "dv"):
        if chart.get(key) not in CHI:
            raise ValueError(f"Thiếu hoặc sai cung {key}.")
    houses = chart.get("houses", {})
    if set(houses) != set(CHI):
        raise ValueError("Cần đủ 12 cung địa chi.")
    for chi, stars in houses.items():
        if not isinstance(stars, list) or not all(isinstance(s, str) for s in stars):
            raise ValueError(f"Danh sách sao cung {chi} không hợp lệ.")
    return True

def has_star(chart, chi, name):
    return any(normalize(star) == normalize(name) for star in chart["houses"][chi])

def matched_rules(chart, rules):
    validate(chart)
    anchors = {"tat": chart["tat"], "menh": chart["menh"], "dvtat": tat_dai_van(chart["dv"])}
    out = []
    for rule in rules:
        anchor = anchors.get(rule["target"])
        if not anchor:
            continue
        conditions = rule.get("req") or rule.get("any") or []
        details = []
        matched = []
        for star, relation in conditions:
            matching = [chi for chi in relations(anchor)[relation] if has_star(chart, chi, star)]
            matched.append(bool(matching))
            if matching:
                details.append(f"{star} – {relation} tại {', '.join(matching)}")
        good = any(matched) if "any" in rule else all(matched)
        if good and conditions:
            out.append({**rule, "anchor": anchor, "details": details})
    return out

def analyze(chart, rules):
    matches = matched_rules(chart, rules)
    groups = {kind: [r for r in matches if r["kind"] == kind]
              for kind in ("Tật", "Ách", "Tật đại vận", "Đối chiếu mở rộng")}
    return {"tat_dv": tat_dai_van(chart["dv"]), "matches": matches, "groups": groups}

def relation_table(chart, anchor):
    return [{"Quan hệ": rel, "Địa chi": ", ".join(chis),
             "Các sao": "; ".join(f"{chi}: {', '.join(chart['houses'][chi])}" for chi in chis)}
            for rel, chis in relations(anchor).items()]

def text_report(chart, result):
    lines = [
        "AI TỬ VI – CHUYÊN ĐỀ TẬT ÁCH | BẢN KIỂM NGHIỆM",
        str(chart.get("person", "Lá số")),
        f"Mệnh {chart['menh']} | Tật gốc {chart['tat']} | "
        f"Mệnh đại vận {chart['dv']} | Tật đại vận {result['tat_dv']}",
        "",
    ]
    for heading, kind, predicate in [
        ("I. TẬT NGUYÊN CỤC – BỆNH LÝ", "Tật", lambda r: r.get("group") != "tâm tính"),
        ("II. ÁCH NGUYÊN CỤC – TAI NẠN, THƯƠNG TÍCH, KIỆN TỤNG", "Ách", lambda r: True),
        ("III. TÍNH CÁCH MỆNH – TẬT", "Tật", lambda r: r.get("group") == "tâm tính"),
        ("IV. TẬT VÀ ÁCH ĐẠI VẬN", "Tật đại vận", lambda r: True),
        ("V. GIÁP CUNG, NHỊ HỢP – ĐỐI CHIẾU MỞ RỘNG", "Đối chiếu mở rộng", lambda r: True),
    ]:
        lines.extend(["", heading, "-" * 45])
        if kind == "Tật" and "TÍNH CÁCH" in heading:
            for k, c in (("Mệnh", chart["menh"]), ("Tật", chart["tat"])):
                lines.append(f"{k} {c}: {', '.join(chart['houses'][c])}")
        items = [x for x in result["groups"][kind] if predicate(x)]
        if not items:
            lines.append("Chưa có quy tắc đủ điều kiện trong thư viện thử nghiệm.")
        for x in items:
            lines += [f"• {x['title']}", x["result"],
                      "Điều kiện: " + "; ".join(x["details"]),
                      f"Nguồn: {x.get('source','—')} | {x.get('page','—')}"]
    lines += ["", "Lưu ý: Đây là cách giải đoán Tử Vi truyền thống để nghiên cứu; "
              "không phải chẩn đoán y khoa, tiên đoán tai nạn chắc chắn hay kết luận pháp lý."]
    return "\n".join(lines)
