"""Website Tử Vi Tật–Ách: quy tắc minh bạch, AI thị giác tùy chọn."""
import base64
import copy
import io
import json
import re
from urllib.parse import quote_plus

import streamlit as st
from PIL import Image

from engine import CHI, analyze, labels_for, relation_table, tat_dai_van, text_report, validate
from seed import CHARTS, RULES

st.set_page_config(page_title="AI Tử Vi · Tật – Ách", page_icon="☯️", layout="wide")
st.markdown("""
<style>
.block-container {max-width:1180px;padding-top:1.5rem}
h1,h2,h3 {letter-spacing:-.028em}
div[data-testid="stMetric"] {background:#f8f6f2;padding:14px;border-radius:12px}
</style>
""", unsafe_allow_html=True)

MODELS = ["Qwen/Qwen3-VL-8B-Instruct", "Qwen/Qwen3-VL-30B-A3B-Instruct"]
READ_PROMPT = """
Bạn CHỈ sao chép chữ và tên sao trong 12 ô lá số Tử Vi tiếng Việt.
Không suy luận sao không nhìn rõ, không luận đoán. Trả về duy nhất JSON:
{"person":"Lá số từ ảnh","menh":null,"tat":null,"dv":null,
"houses":{"Tý":[],"Sửu":[],"Dần":[],"Mão":[],"Thìn":[],"Tị":[],
"Ngọ":[],"Mùi":[],"Thân":[],"Dậu":[],"Tuất":[],"Hợi":[]}}
menh là địa chi ô có nhãn MỆNH; tat ô TẬT ÁCH; dv là Mệnh đại vận
nếu đọc rõ, nếu không rõ để null. Mỗi houses có các tên sao đọc được,
giữ ký hiệu (M),(V),(Đ),(H) và Tuần/Triệt. Không tự điền sao dựa vào quy tắc.
"""
WRITE_PROMPT = """
Viết bài Tử Vi cổ truyền CHỈ từ JSON sao đã được duyệt và các quy tắc khớp.
Không tự thêm sao, đoán cách cục, bịa trang sách hoặc biến giáp/nhị hợp thành đồng cung.
Bố cục: I. Tật gốc (bệnh lý); II. Ách gốc (tai họa, pháp lý);
III. Tính cách qua Mệnh và Tật; IV. Mệnh đại vận, Tật–Ách đại vận;
V. Kết luận và các yếu tố giải. Với mỗi nhận định phải chỉ rõ bộ sao
và quan hệ đã khớp. Những cách chưa đủ không được khẳng định.
Không coi kết quả là chẩn đoán y khoa hay dự báo chắc chắn.
"""

def token():
    try:
        secret = st.secrets.get("HF_TOKEN", "")
    except Exception:
        secret = ""
    return st.session_state.get("typed_token", "") or secret

def infer(model, messages, maximum=4500):
    from huggingface_hub import InferenceClient
    if not token():
        raise ValueError("Chưa có Hugging Face Token. Lá số mẫu vẫn dùng được không cần token.")
    client = InferenceClient(token=token(), provider="auto", timeout=160)
    result = client.chat.completions.create(
        model=model, messages=messages, temperature=0.1, max_tokens=maximum
    )
    answer = result.choices[0].message.content
    if isinstance(answer, str):
        return answer
    return "\n".join(x.get("text", "") for x in answer if isinstance(x, dict))

def image_data(image):
    img = image.convert("RGB")
    img.thumbnail((1950, 1950))
    buff = io.BytesIO()
    img.save(buff, format="JPEG", quality=90)
    return "data:image/jpeg;base64," + base64.b64encode(buff.getvalue()).decode()

def parse_json(raw):
    try:
        return json.loads(raw)
    except ValueError:
        decoder = json.JSONDecoder()
        for index, character in enumerate(raw):
            if character == "{":
                try:
                    obj, _ = decoder.raw_decode(raw[index:])
                    return obj
                except ValueError:
                    continue
    raise ValueError("AI không trả về JSON có thể kiểm tra.")

def clean_image_result(data):
    raw = data.get("houses", {})
    if not isinstance(raw, dict):
        raise ValueError("Thiếu bảng các cung trong phản hồi AI.")
    houses = {chi: [] for chi in CHI}
    for key, items in raw.items():
        chi = str(key).replace("Tỵ", "Tị")
        if chi in CHI and isinstance(items, list):
            houses[chi] = [x.strip()[:90] for x in items
                           if isinstance(x, str) and x.strip()][:60]
    recognized = {}
    for key in ("menh", "tat", "dv"):
        value = data.get(key)
        if value == "Tỵ":
            value = "Tị"
        recognized[key] = value if value in CHI else None
    return {"person": str(data.get("person") or "Lá số từ ảnh")[:90],
            "houses": houses, **recognized}

def sample(key):
    if key == "new":
        return {"person": "Lá số mới", "menh": "Tị", "tat": "Tý", "dv": "Sửu",
                "houses": {c: [] for c in CHI}}
    return copy.deepcopy(CHARTS[key])

def list_rules(items):
    if not items:
        st.info("Chưa có cách nào đủ điều kiện trong 21 quy tắc thử nghiệm.")
    for item in items:
        with st.expander(item["title"] + " · " + item.get("group", item["kind"])):
            st.write(item["result"])
            for detail in item["details"]:
                st.write("• " + detail)
            st.caption("Nguồn: " + item.get("source", "—") +
                       " | Trang/mục: " + item.get("page", "—"))

with st.sidebar:
    st.subheader("Cấu hình AI tùy chọn")
    st.text_input("Hugging Face Token", type="password", key="typed_token")
    model = st.selectbox("Mô hình thị giác", MODELS)
    st.markdown("[Đăng ký Hugging Face](https://huggingface.co/join) · "
                "[Tạo token](https://huggingface.co/settings/tokens)")
    st.caption("Khi dùng AI, ảnh được gửi đến dịch vụ trực tuyến. "
               "Có thể bị giới hạn lượt hoặc tính phí.")
    st.caption("Không lưu token trong GitHub. Không tải ảnh chứa thông tin nhạy cảm nếu chưa đồng ý.")

if "chart" not in st.session_state:
    st.session_state.chart = sample("giapty")
    st.session_state.last_choice = "giapty"
    st.session_state.revision = 0

st.title("☯️ AI TỬ VI · CHUYÊN ĐỀ TẬT – ÁCH")
st.write("Luận Tật gốc, Ách gốc, tính cách Mệnh–Tật và Tật–Ách đại vận.")
st.caption("Bản nghiên cứu V1 · Có thể sử dụng lá số mẫu mà không cần kết nối AI")

st.header("① Chọn lá số hoặc tải ảnh")
left, right = st.columns([1, 1])
with left:
    options = {"Nữ Giáp Tý 1984": "giapty", "Nam Kỷ Mùi 1979": "kymui",
               "Lá số trống": "new"}
    chosen = options[st.selectbox("Lá số", list(options))]
    if chosen != st.session_state.last_choice:
        st.session_state.chart = sample(chosen)
        st.session_state.last_choice = chosen
        st.session_state.revision += 1
        st.session_state.pop("draft", None)
        st.session_state.pop("written", None)
        st.rerun()
    upload = st.file_uploader("Tải ảnh JPG, PNG hoặc WebP",
                              type=["jpg", "jpeg", "png", "webp"])
with right:
    if upload:
        st.image(upload, use_container_width=True)
    else:
        st.info("Chọn lá số mẫu để tra cứu ngay, hoặc tải ảnh để AI đọc.")

if upload and st.button("✨ AI đọc 12 cung", type="primary"):
    try:
        with st.spinner("Đang nhận dạng chữ và sao..."):
            messages = [{"role": "user", "content": [
                {"type": "text", "text": READ_PROMPT},
                {"type": "image_url", "image_url": {
                    "url": image_data(Image.open(upload))
                }}
            ]}]
            st.session_state.draft = clean_image_result(
                parse_json(infer(model, messages, 5500))
            )
    except Exception as exc:
        st.error("Chưa thể đọc ảnh: " + str(exc))

if st.session_state.get("draft"):
    draft = st.session_state.draft
    st.subheader("Kiểm tra kết quả trước khi luận")
    st.warning("AI có thể nhầm vị trí cung, tên sao và miếu/vượng/hãm. "
               "Bạn cần kiểm tra và sửa dữ liệu sau khi xác nhận.")
    st.dataframe([{"Cung": c, "Sao đọc được": ", ".join(draft["houses"][c])
                  or "Chưa đọc được"} for c in CHI], use_container_width=True,
                 hide_index=True)
    cols = st.columns(3)
    confirmed = {}
    for col, key, label in zip(cols, ("menh", "tat", "dv"),
                               ("Mệnh gốc", "Tật gốc", "Mệnh đại vận")):
        value = draft[key]
        with col:
            choice = st.selectbox("Xác nhận " + label, ["Chưa xác định"]+CHI,
                                  index=CHI.index(value)+1 if value in CHI else 0)
            confirmed[key] = choice
    if st.button("✅ Dùng lá số nhận dạng"):
        if "Chưa xác định" in confirmed.values():
            st.error("Hãy xác nhận ba vị trí Mệnh gốc, Tật gốc và Mệnh đại vận.")
        else:
            d = copy.deepcopy(draft)
            d.update(confirmed)
            validate(d)
            st.session_state.chart = d
            st.session_state.revision += 1
            st.session_state.pop("draft")
            st.rerun()

st.divider()
st.header("② Kiểm tra dữ liệu 12 cung và đại vận")
chart = st.session_state.chart
with st.form("edit"):
    cols = st.columns(4)
    name = cols[0].text_input("Hồ sơ", chart.get("person", ""))
    menh = cols[1].selectbox("Mệnh gốc", CHI, index=CHI.index(chart["menh"]))
    tat = cols[2].selectbox("Tật gốc", CHI, index=CHI.index(chart["tat"]))
    dv = cols[3].selectbox("Mệnh đại vận", CHI, index=CHI.index(chart["dv"]))
    st.caption(f"Mệnh đại vận {dv} → Tật đại vận {tat_dai_van(dv)}.")
    edits = {}
    with st.expander("Mở bảng chỉnh sửa sao ở 12 cung"):
        for n in range(0, 12, 3):
            columns = st.columns(3)
            for col, chi in zip(columns, CHI[n:n+3]):
                with col:
                    edits[chi] = st.text_area(
                        chi + " · " + labels_for(menh)[chi],
                        ", ".join(chart["houses"][chi]), height=106,
                        key=f"{chi}_{st.session_state.revision}")
    submitted = st.form_submit_button("💾 Lưu và tính lại")
if submitted:
    revised = copy.deepcopy(chart)
    revised.update(person=name, menh=menh, tat=tat, dv=dv)
    revised["houses"] = {chi: [x.strip() for x in re.split(r"[,;\n]+", edits[chi])
                              if x.strip()] for chi in CHI}
    validate(revised)
    st.session_state.chart = revised
    st.session_state.pop("written", None)
    st.success("Đã lưu trong phiên làm việc.")

chart = st.session_state.chart
result = analyze(chart, RULES)
metrics = st.columns(4)
for col, (label, value) in zip(metrics, [
    ("Mệnh gốc", chart["menh"]), ("Tật gốc", chart["tat"]),
    ("Mệnh đại vận", chart["dv"]), ("Tật đại vận", result["tat_dv"])
]):
    col.metric(label, value)

st.header("③ Xem luận giải và cách cục")
tab1, tab2, tab3, tab4 = st.tabs([
    "Tật – Ách gốc", "Tính cách", "Tật – Ách đại vận", "Căn cứ và nguồn"
])
with tab1:
    st.subheader("I. Tật gốc – bệnh lý theo hệ sao")
    list_rules([x for x in result["groups"]["Tật"] if x["group"] != "tâm tính"])
    st.subheader("II. Ách gốc – tai họa, thương tích và kiện tụng")
    list_rules(result["groups"]["Ách"])
with tab2:
    a, b = st.columns(2)
    a.subheader("Mệnh – biểu hiện bên ngoài")
    a.write(", ".join(chart["houses"][chart["menh"]]) or "Chưa nhập sao")
    b.subheader("Tật – nội tâm")
    b.write(", ".join(chart["houses"][chart["tat"]]) or "Chưa nhập sao")
    list_rules([x for x in result["groups"]["Tật"] if x["group"] == "tâm tính"])
with tab3:
    st.subheader("Mệnh đại vận " + chart["dv"] +
                 " · Tật đại vận " + result["tat_dv"])
    list_rules(result["groups"]["Tật đại vận"])
    st.subheader("Giáp cung và nhị hợp")
    list_rules(result["groups"]["Đối chiếu mở rộng"])
    st.dataframe(relation_table(chart, result["tat_dv"]),
                 use_container_width=True, hide_index=True)
with tab4:
    st.write(f"Đã khớp **{len(result['matches'])}/{len(RULES)}** quy tắc.")
    st.dataframe([{
        "Mã": x["id"], "Cách cục": x["title"], "Loại": x["kind"],
        "Bộ sao": "; ".join(x["details"]),
        "Nguồn": x["source"], "Trang/mục": x["page"]
    } for x in result["matches"]], hide_index=True, use_container_width=True)

st.subheader("📄 Báo cáo")
report = text_report(chart, result)
with st.expander("Báo cáo theo quy tắc (không cần token)", expanded=True):
    st.text_area("Bản phân tích", report, height=270)
    st.download_button("⬇️ Tải báo cáo TXT", report.encode("utf-8-sig"),
                       "Bao_cao_Tat_Ach.txt", "text/plain")
if st.button("🧠 AI viết bài luận đầy đủ"):
    try:
        payload = {"menh": chart["menh"], "tat": chart["tat"],
                   "dv": chart["dv"], "tat_dv": result["tat_dv"],
                   "houses": chart["houses"], "matched_rules": result["matches"]}
        with st.spinner("AI đang viết bài theo căn cứ đã kiểm tra..."):
            st.session_state.written = infer(model, [
                {"role": "system", "content": WRITE_PROMPT},
                {"role": "user", "content": json.dumps(payload, ensure_ascii=False)}
            ])
    except Exception as exc:
        st.error("Chưa tạo được bài luận AI: " + str(exc))
if st.session_state.get("written"):
    st.markdown(st.session_state.written)
    st.download_button("⬇️ Tải bài luận AI",
                       st.session_state.written.encode("utf-8-sig"),
                       "Luan_giai_Tat_Ach_AI.txt", "text/plain")

st.divider()
st.header("④ Tra cứu tài liệu")
st.markdown("[Nguồn an sao lasotuvi](https://github.com/doanguyen/lasotuvi) · "
            "[Hugging Face](https://huggingface.co/) · "
            "[Tài liệu Streamlit](https://docs.streamlit.io/)")
query = st.text_input("Tra cứu bộ sao", "Thất Sát Địa Không Địa Kiếp Tật Ách")
st.link_button("🔎 Mở tìm kiếm", "https://www.google.com/search?q=" + quote_plus(query))
st.caption("Internet chỉ dùng tham khảo, không tự thêm cách cục. Đây là "
           "hệ thống nghiên cứu Tử Vi truyền thống, không phải chẩn đoán "
           "y khoa hay kết luận về tai nạn, pháp lý.")
