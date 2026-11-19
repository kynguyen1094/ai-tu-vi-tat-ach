"""V3: tổng hợp chứng cứ Tử Vi, không dự đoán biến cố thực tế.
Nguồn A: Các cách chỉ bệnh tật trong Tử Vi, các mục 1–11.
Nguồn B: Cung Tật Ách: Bản chất, bệnh lý và các yếu tố liên quan,
phần 1–2, bảng tính cách và bảng sao–tạng phủ.
Chỉ đưa vào các ý tóm tắt; không lưu hồ sơ thật hoặc bản sách.
"""
import re
from engine import CHI, normalize, relations, tat_dai_van, labels_for, validate
from interpretation import BODY_B, NATURE_B, NATURE_SUPPORT_B

A = "A — Các cách chỉ bệnh tật trong Tử Vi"
B = "B — Cung Tật Ách: Bản chất, bệnh lý và các yếu tố liên quan"
M = "M — Phương pháp nghiên cứu / vận dụng từ bài mẫu, không phải trích cổ thư"
REL = ("tọa thủ", "xung chiếu", "tam hợp", "giáp", "nhị hợp")
PRIMARY = {normalize(s) for s in BODY_B}
ALIASES = {"thien dieu":"thien rieu", "ta phu":"ta phu", "huu phu":"huu bat",
           "hy than":"hy than"}
def nstar(s):
    n = normalize(s)
    return ALIASES.get(n, n)

def split_layer(s):
    # P. (phi hóa), L. (lưu), LN. (lưu niên) không được dùng như sao gốc.
    if re.match(r"^\s*(?:L|LN|P|ĐV|DV)\s*[.:\-]", s, re.I):
        return "other"
    if re.match(r"^\s*(?:Lưu niên|Lưu|Phi hóa|Đại vận)\s+", s, re.I):
        # Lưu Hà là sao gốc, không phải tiền tố lưu niên.
        if nstar(s) != "luu ha":
            return "other"
    return "original"

def original_chart(chart):
    validate(chart)
    return {**chart, "houses": {c:[s for s in chart["houses"][c] if split_layer(s)=="original"] for c in CHI}}

def evidence(chart, anchor):
    labels = labels_for(chart["menh"])
    r = relations(anchor)
    return [{"relation": rel, "chi": chi, "house": labels[chi],
             "stars": chart["houses"][chi],
             "main": [s for s in chart["houses"][chi] if nstar(s) in PRIMARY]}
            for rel in REL for chi in r[rel]]

# Nguồn A được ưu tiên: không lấy Thiên Đồng chỉ bài tiết hoặc
# Vũ–Sát chỉ hô hấp từ bảng tổng hợp khi A có mô tả khác.
BODY_A = {
    "Thiên Đồng": ("tiêu hóa", "Tượng chung của bộ máy tiêu hóa; cần phối hợp sao bất lợi.", "1"),
    "Đại Hao": ("tiêu hóa", "Song Hao liên hệ đau bụng, tiêu chảy và tiêu hóa; xét vị trí và sao phối hợp.", "1"),
    "Tiểu Hao": ("tiêu hóa", "Song Hao liên hệ đau bụng, tiêu chảy và tiêu hóa; xét vị trí và sao phối hợp.", "1"),
    "Thiên Riêu": ("tiêu hóa / răng", "Liên hệ ruột và răng trong các mục tương ứng.", "1, 5"),
    "Hỷ Thần": ("tiêu hóa", "Tượng hậu môn theo tài liệu A.", "1"),
    "Bệnh Phù": ("tiêu hóa", "Liên hệ nhóm dạ dày và dinh dưỡng.", "1"),
    "Thái Dương": ("mắt", "Tượng mắt trái; cần sao bất lợi phối hợp để xét bệnh.", "8"),
    "Thái Âm": ("mắt", "Tượng mắt phải; A còn có cách Nguyệt hãm về tiêu hóa và hô hấp.", "1, 2, 8"),
    "Long Trì": ("tai mũi họng", "Tượng mũi, không phải tai.", "5"),
    "Phượng Các": ("tai mũi họng", "Tượng tai.", "5"),
    "Phá Toái": ("tai mũi họng", "Tượng cuống họng.", "5"),
    "Bạch Hổ": ("huyết khí", "Tượng máu; phối hợp Tang Môn để xét bộ khí huyết.", "3"),
    "Tang Môn": ("huyết khí", "Tượng máu theo tài liệu A.", "3"),
    "Lưu Hà": ("huyết khí", "Tượng máu trong các cách của tài liệu A.", "3"),
    "Thiên Khốc": ("hô hấp", "Nhóm tượng phổi, ho theo tài liệu A.", "2"),
}
# Giữ các liên hệ thuộc B khi A không chỉ cơ quan trực tiếp. Không tự biến thành bệnh.
BODY_SECOND = {
    "Tử Vi":"tiêu hóa", "Thiên Cơ":"gan, mật, nội tiết",
    "Vũ Khúc":"hô hấp", "Liêm Trinh":"tuần hoàn",
    "Thiên Phủ":"miệng", "Tham Lang":"gan, nội tiết",
    "Cự Môn":"tiêu hóa, khoang miệng",
    "Thiên Tướng":"mật, bài tiết", "Thiên Lương":"tuyến vú",
    "Thất Sát":"hô hấp", "Phá Quân":"thận",
}
# Cách cục: khi nguồn ghi một chuỗi mà chưa xác định chính xác kiểu hội,
# chỉ gắn trạng thái tra cứu, KHÔNG tự đặt điều kiện thành cách.
FORMULAS = [
 ("A01","Tật","tiêu hóa",["Thiên Đồng","Hóa Kỵ"],"Tổ hợp tiêu hóa và Hóa Kỵ", "1"),
 ("A02","Tật","tiêu hóa",["Vũ Khúc","Thất Sát"],"Tổ hợp tiêu hóa được A liệt kê", "1"),
 ("A03","Tật","tiêu hóa",["Thiên Riêu","Đà La","Hóa Kỵ"],"Nhóm dạ dày, ruột", "1"),
 ("A04","Tật","tiêu hóa",["Địa Không","Địa Kiếp","Bệnh","Thiên Cơ"],"Nhóm mật; sao Bệnh không đồng nhất với Bệnh Phù", "1"),
 ("A05","Tật","tiêu hóa",["Địa Không","Địa Kiếp","Hỷ Thần"],"Nhóm hậu môn", "1"),
 ("A06","Tật","tiêu hóa",["Tham Lang","Đà La"],"Tượng ăn uống quá độ", "1"),
 ("A07","Tật","hô hấp",["Tang Môn","Bạch Hổ","Thiên Khốc","Thiên Hư"],"Nhóm hô hấp trong cổ thư", "2"),
 ("A08","Tật","huyết khí",["Tang Môn","Bạch Hổ"],"Tổ hợp khí huyết", "3"),
 ("A09","Tật","tai mũi họng",["Phượng Các","Kình Dương","Đà La"],"Nhóm tai", "5"),
 ("A10","Tật","tai mũi họng",["Long Trì","Thiên Khốc","Thiên Hư"],"Nhóm mũi", "5"),
 ("A11","Tật","tai mũi họng",["Phá Toái","Thiên Hình"],"Nhóm cuống họng", "5"),
 ("A12","Tật","da",["Vũ Khúc","Thiên Cơ"],"Nhóm ngoài da, tê thấp", "7"),
 ("A13","Tật","da",["Thiên Cơ","Thái Âm"],"Nhóm mụn nhọt", "7"),
 ("A14","Tật","da",["Thiên Cơ","Địa Không","Địa Kiếp"],"Nhóm tổn thương da", "7"),
 ("A15","Tật","da",["Liêm Trinh","Phá Quân"],"Nhóm tỳ vết ở tứ chi", "7"),
 ("A16","Ách","nhiệt",["Hỏa Tinh","Linh Tinh","Mộc Dục"],"Nhóm bỏng nước hoặc lửa trong cổ thư", "7"),
 ("A17","Tật","thị lực",["Thái Âm","Thiên Riêu","Thiên Hình","Hóa Kỵ"],"Nhóm mắt", "8"),
 ("A18","Tật","gân cốt",["Thiên Mã","Đà La"],"Nhóm tứ chi", "9"),
 ("A19","Ách","thương tích",["Thiên Mã","Thiên Hình"],"Nhóm thương tích tay chân", "9"),
 ("A20","Tật","gân cốt",["Thiên Hình","Đà La"],"Nhóm yếu gân", "9"),
 ("A21","Tật","gân cốt",["Vũ Khúc","Thiên Riêu"],"Nhóm tê thấp, phù tứ chi", "9"),
 ("A22","Tật","miệng",["Cự Môn","Linh Tinh"],"Cách cổ về tật vùng miệng", "11"),
 ("A23","Tật","miệng",["Cự Môn","Hỏa Tinh"],"Cách cổ về tật vùng miệng", "11"),
 ("A24","Tật","ám tật",["Vũ Khúc","Thiên Tướng"],"Tượng ám tật theo cổ thư", "11"),
 ("A25","Ách","dao kéo",["Thiên Hình","Kiếp Sát"],"Hai sao liên hệ mổ xẻ; cần bộ sao chỉ bệnh hoặc thương tích đi kèm", "1"),
 ("A26","Tật","hô hấp",["Địa Không","Địa Kiếp"],"Nhóm cách hô hấp, cần đối chiếu các sao chỉ bệnh", "2"),
]
# C: kiểm tra trực tiếp trang in 625–626; chỉ chọn những cách có điều kiện đồng cung rõ.
C = "C — Tử Vi Vựng Tập Bình Chú, Bùi Quang Nhuận"
LEGAL_FORMULAS = [
 ("C01", ["Đường Phù","Bạch Hổ"], [], "Quan tụng", "625"),
 ("C02", ["Thiên Hình","Hóa Kỵ"], ["Hợi","Tý"], "Nhóm hình pháp", "625"),
 ("C03", ["Kình Dương","Thái Tuế"], [], "Quan tụng, hình pháp", "626"),
 ("C04", ["Liêm Trinh","Tham Lang"], [], "Nhóm hình pháp theo cổ thư", "626"),
 ("C05", ["Phá Quân","Địa Không","Địa Kiếp"], [], "Nhóm hình pháp theo cổ thư", "626"),
]
def legal_formulas_at(ev):
    result=[]
    for ident,stars,allowed,meaning,page in LEGAL_FORMULAS:
        for e in ev:
            if allowed and e["chi"] not in allowed:
                continue
            if not {nstar(s) for s in stars}.issubset({nstar(s) for s in e["stars"]}):
                continue
            result.append(dict(id=ident,kind="Ách",group="quan tụng (tư liệu cổ)",meaning=meaning,
                source=C+" · trang in "+page,
                evidence=positions([e],stars),
                status="Đủ điều kiện đồng cung"+(" tại "+e["chi"] if allowed else "")+
                       " ở cung "+e["relation"]+"; chỉ đối chiếu văn bản cổ, không suy ra phạm tội hoặc hình tù thực tế"))
    return result

# Bổ trợ theo mục tính cách của B; các sao chưa có nghĩa riêng không gán bừa.
EXTRA_NATURE = {
 "Phong Cáo":"Khuynh hướng coi trọng danh vị, thích hư vinh.",
 "Thai Phụ":"Khuynh hướng coi trọng danh vị, thích hư vinh.",
 "Lâm Quan":"Khuynh hướng thích thể hiện.",
 "Tang Môn":"Tượng nội tâm nhiều cảm xúc và bận tâm.",
 "Bạch Hổ":"Tượng nội tâm nhiều cảm xúc và bận tâm.",
}
# Bộ sao cứu giải được nêu tại B phần 1.2 và ví dụ phần 2.
HELPERS = ("Ân Quang","Thiên Quý","Long Đức","Phúc Đức","Thiên Đức","Nguyệt Đức","Hóa Khoa","Thiên Phúc","Thiên Giải","Giải Thần","Địa Giải")
HARD = ("Địa Không","Địa Kiếp","Kình Dương","Đà La","Hỏa Tinh","Linh Tinh","Thiên Hình","Kiếp Sát")
LEGAL = ("Quan Phù","Quan Phủ","Thái Tuế","Hóa Kỵ","Thiên La","Địa Võng","Cự Môn","Thiên Hình")
def positions(ev, names):
    requested = {nstar(s) for s in names}
    return [dict(sao=s, cung=e["chi"], quan_he=e["relation"])
            for e in ev for s in e["stars"] if nstar(s) in requested]

def formulas_at(ev):
    result=[]
    for ident,kind,group,stars,meaning,section in FORMULAS:
        found=positions(ev,stars)
        if not {nstar(s) for s in stars}.issubset({nstar(f["sao"]) for f in found}):
            continue
        common=set.intersection(*[{f["cung"] for f in found if nstar(f["sao"])==nstar(s)} for s in stars])
        core=all(any(nstar(f["sao"])==nstar(s) and f["quan_he"] in REL[:3] for f in found) for s in stars)
        result.append(dict(id=ident,kind=kind,group=group,meaning=meaning,
            source=A+" · mục "+section, evidence=found,
            status="Đủ thành phần cùng cung (cần đối chiếu điều kiện cổ thư)" if common else
                   "Đủ thành phần trong tam phương tứ chính, chưa xác nhận kiểu phối" if core else
                   "Đối chiếu mở rộng giáp/nhị hợp, không phải cách đồng cung"))
    return result + legal_formulas_at(ev)

def groups_at(ev):
    rows=[]; used=set()
    for e in ev:
        for raw in e["stars"]:
            for s,(group,val,sec) in BODY_A.items():
                if nstar(raw)==nstar(s) and (e["chi"],s) not in used:
                    rows.append(dict(group=group,star=raw,chi=e["chi"],relation=e["relation"],meaning=val,source=A+" · mục "+sec))
                    used.add((e["chi"],s))
            for s,group in BODY_SECOND.items():
                if nstar(raw)==nstar(s) and (e["chi"],s) not in used:
                    rows.append(dict(group=group,star=raw,chi=e["chi"],relation=e["relation"],meaning="Quy chiếu tạng phủ bổ sung, không phải cách chỉ bệnh.",source=B+" · bảng 4"))
                    used.add((e["chi"],s))
    return rows

def nature_at(ev, inner):
    rows=[]; seen=set()
    meanings={**{s:v for s,v in NATURE_B.items() if v},**NATURE_SUPPORT_B,**EXTRA_NATURE}
    for entry in ev:
        for raw in entry["stars"]:
            for s,meaning in meanings.items():
                if nstar(s)==nstar(raw) and (entry["chi"],s) not in seen:
                    rows.append(dict(star=raw,chi=entry["chi"],relation=entry["relation"],meaning=meaning,
                        source=B+" · bảng tính cách",scope="Tật tọa thủ" if inner and entry["relation"]=="tọa thủ" else "Vận dụng bổ trợ, không phải nguyên văn về vị trí này"))
                    seen.add((entry["chi"],s))
    if not ev[0]["main"] and ev[0]["stars"] and inner:
        rows.insert(0,dict(star="Vô chính diệu",chi=ev[0]["chi"],relation="tọa thủ",meaning="Nguồn B liên hệ với sự biến đổi theo giai đoạn, đa cảm; lấy chính tinh xung chiếu và tam hợp làm lớp đối chiếu, không coi là sao tọa thủ.",source=B+" · bảng tính cách",scope="Tật tọa thủ; phương pháp đối chiếu "+M))
    return rows

def layer(chart,anchor):
    ev=evidence(chart,anchor)
    return dict(anchor=anchor,vo_chinh_dieu=not ev[0]["main"] and bool(ev[0]["stars"]),
                du_lieu_trong=not ev[0]["stars"],evidence=ev,body=groups_at(ev),formulas=formulas_at(ev),
                hard=positions(ev,HARD),help=positions(ev,HELPERS),legal=positions(ev,LEGAL),
                blockers=positions(ev,("Tuần","Triệt","Triệt - Tuần")))

def build_context(chart):
    ch=original_chart(chart)
    dv=tat_dai_van(ch["dv"])
    if tat_dai_van(ch["menh"])!=ch["tat"]:
        raise ValueError("Vị trí Mệnh/Tật không theo thứ tự 12 cung đang sử dụng. Hãy kiểm tra nhận dạng trước khi luận V3.")
    l={k:layer(ch,c) for k,c in [("menh",ch["menh"]),("tat",ch["tat"]),("dv",ch["dv"]),("dvtat",dv)]}
    omitted={c:[s for s in chart["houses"][c] if split_layer(s)!="original"] for c in CHI}
    return {"layers":l,"nature_menh":nature_at(l["menh"]["evidence"],False),"nature_tat":nature_at(l["tat"]["evidence"],True),
            "omitted_non_original":{k:v for k,v in omitted.items() if v},
            "empty_houses":[c for c in CHI if not ch["houses"][c]],
            "overlap":{"tat_goc":ch["tat"],"tat_dai_van":dv,
                       "relations":[r for r in REL if ch["tat"] in relations(dv)[r]]},
            "method": "A ưu tiên hơn B về bệnh lý. Các cách đủ thành phần chưa mặc nhiên đủ điều kiện cổ thư. Mệnh đại vận và Tật đại vận đều xét; giáp và nhị hợp là lớp riêng. Mọi nhận định là tượng lý số."}

def fmt_pos(p):
    return ", ".join(dict.fromkeys(f"{x['sao']} ({x['quan_he']} {x['cung']})" for x in p)) or "Chưa thấy trong dữ liệu"

def deterministic_report(ctx):
    l=ctx["layers"]
    out=["# LUẬN GIẢI TẬT – ÁCH CHUYÊN SÂU · V3",ctx["method"]]
    if ctx["empty_houses"]:
        out+=["**Cần kiểm tra thêm dữ liệu các cung:** "+", ".join(ctx["empty_houses"])+". Ô trống có thể là lỗi nhận dạng."]
    def structure(a,label):
        out.append("### "+label+" tại "+a["anchor"])
        if a["vo_chinh_dieu"]:
            out.append("Vô chính diệu theo dữ liệu đã nhập: xét chính tinh xung chiếu, tam hợp; không đổi thành tọa thủ.")
        for e in a["evidence"]:
            out.append("- **"+e["relation"]+" "+e["chi"]+" ("+e["house"]+"):** "+(", ".join(e["stars"]) or "chưa có dữ liệu"))
    def body(a):
        out.append("### Nhóm tượng bệnh lý")
        grouped={}
        for x in a["body"]: grouped.setdefault(x["group"],[]).append(x)
        for key,values in grouped.items():
            out.append("**"+key.capitalize()+"**")
            for x in values:
                out.append("- "+x["star"]+" ("+x["relation"]+" "+x["chi"]+"): "+x["meaning"]+" ["+x["source"]+"]")
        if not grouped: out.append("Chưa có căn cứ tượng sao trong kho hiện có.")
    def ways(a,kind):
        items=[x for x in a["formulas"] if x["kind"]==kind]
        for x in items:
            out.append("- **"+x["meaning"]+"**: "+fmt_pos(x["evidence"])+". "+x["status"]+". ["+x["source"]+"]")
        if not items: out.append("Chưa tìm đủ thành phần của cách chuyên biệt đã mã hóa.")
    def ach(a):
        out.append("### Ách — các dấu hiệu cần đối chiếu")
        out.append("Sát/hình: "+fmt_pos(a["hard"])+". Đây là danh mục chứng cứ, không xác định tai nạn.")
        out.append("Sao thường được kiểm tra khi xét quan tụng: "+fmt_pos(a["legal"])+". Chưa đủ để chỉ định hình tù hoặc phạm pháp.")
        ways(a,"Ách")
        out.append("Sao trợ lực: "+fmt_pos(a["help"])+". Tuần/Triệt: "+fmt_pos(a["blockers"])+". Cần xét điều kiện gia giảm, không triệt tiêu tự động.")
    out.append("## I. Cấu trúc và Tật nguyên cục")
    structure(l["tat"],"Tật gốc"); body(l["tat"]); ways(l["tat"],"Tật")
    out.append("## II. Ách nguyên cục"); ach(l["tat"])
    out.append("## III. Tính cách Mệnh – Tật")
    for key,title,items in [("menh","Mệnh — bề nổi",ctx["nature_menh"]),("tat","Tật — bề chìm",ctx["nature_tat"])]:
        out.append("### "+title)
        out.append("Tọa thủ "+l[key]["anchor"]+": "+", ".join(l[key]["evidence"][0]["stars"]))
        for x in items:
            out.append("- "+x["star"]+" ("+x["relation"]+" "+x["chi"]+"): "+x["meaning"]+" "+x["scope"]+". ["+x["source"]+"]")
        if not items: out.append("Chưa có nhận xét được mã hóa; không tự gán tâm tính.")
    out.append("## IV. Tật – Ách đại vận 10 năm")
    structure(l["dv"],"Mệnh đại vận"); ach(l["dv"]); structure(l["dvtat"],"Tật đại vận"); body(l["dvtat"]); ways(l["dvtat"],"Tật"); ach(l["dvtat"])
    out.append("## V. Tổng hợp và đối chiếu")
    o=ctx["overlap"]
    out.append("Tật gốc "+o["tat_goc"]+" và Tật đại vận "+o["tat_dai_van"]+": "+(", ".join(o["relations"]) or "không thuộc các quan hệ đang xét")+". Không suy ra độ nặng chỉ từ quan hệ này.")
    if ctx["omitted_non_original"]:
        out.append("**Sao lưu/phi hóa được tách riêng:** "+ "; ".join(c+": "+", ".join(v) for c,v in ctx["omitted_non_original"].items()))
    out.append("Bản báo cáo căn cứ tự động; không phải chẩn đoán, đánh giá tâm lý hay dự báo pháp lý có kiểm chứng.")
    return "\n\n".join(out)
