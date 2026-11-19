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
from interpretation import baseline, baseline_report
from deep_reading import build_context, deterministic_report, FORMULAS

st.set_page_config(page_title="AI Tử Vi · Tật – Ách", page_icon="☯️", layout="wide")
st.markdown("""
<style>
.block-container {max-width:1180px;padding-top:1.5rem}
h1,h2,h3 {letter-spacing:-.028em}
div[data-testid="stMetric"] {background:#f8f6f2;padding:14px;border-radius:12px}
</style>
""", unsafe_allow_html=True)

HF_MODELS = ["Qwen/Qwen3-VL-8B-Instruct", "Qwen/Qwen3-VL-30B-A3B-Instruct"]
GEMINI_MODELS = ["gemini-3.5-flash-lite", "gemini-3.5-flash", "gemini-3.1-flash-lite", "gemini-2.5-flash", "gemini-2.5-flash-lite"]
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
Bạn là trợ lý biên tập chuyên đề Tật – Ách trong Tử Vi Đẩu Số.
Viết bằng tiếng Việt, theo bố cục bài mẫu nghiên cứu, rõ ràng, mạch lạc,
khoảng 1500–2400 từ nếu dữ liệu đủ. Không kéo dài bằng cách lặp lại sao.
CHỈ dùng dữ liệu lá số đã xác nhận và căn cứ trong JSON; không tự thêm sao,
không suy luận triệu chứng, bệnh thực tế, hành vi phạm pháp, tai nạn hoặc tâm lý
chắc chắn. Không chẩn đoán, không xếp nguy cơ y khoa hoặc pháp lý.
Tôn trọng nguồn A ưu tiên hơn B về bệnh lý, và giữ nguyên vị trí địa chi,
miếu/vượng/đắc/hãm. Không coi sao lưu, phi hóa là sao nguyên cục.
Các công thức đủ thành phần là ứng viên tra cứu, không khẳng định thành cách
nếu kiểu phối, vị trí hoặc điều kiện chưa xác nhận. Không bịa tác giả/trang.
Giáp, nhị hợp là lớp đối chiếu bổ sung. Vô chính diệu phải phân tích chính tinh
xung chiếu và tam hợp theo đúng vị trí, không chuyển chúng thành tọa thủ.
Bố cục bắt buộc:
## I. Xác định hệ thống Tật – Ách
Bảng Mệnh gốc, Tật gốc, Mệnh đại vận, Tật đại vận. Bảng quan hệ cung Tật gốc.
## II. Tật nguyên cục
Luận các nhóm tượng bệnh lý có căn cứ; phân biệt tượng sao với cách bệnh.
## III. Ách nguyên cục
Cách cục cổ về tai nạn, thương tích, khẩu thiệt/quan tụng khi có căn cứ;
nêu điều kiện còn thiếu và sao gia giảm. Không kết luận một cá nhân phạm tội.
## IV. Tính cách Mệnh – Tật
Bề ngoài, bề chìm và đối chiếu; nét tâm tính chỉ là diễn giải truyền thống.
Nêu rõ ý trực tiếp từ nguồn B và ý vận dụng bổ trợ, không gán tính xấu như sự thật.
## V. Tật – Ách đại vận 10 năm
Luận riêng Mệnh đại vận và Tật đại vận; bảng quan hệ Tật đại vận;
so sánh các dấu hiệu gốc và vận, xét sao trợ lực và giới hạn dữ liệu.
## VI. Bảng tổng kết
Tật gốc, Ách gốc, Mệnh–Tật, Tật đại vận, Ách đại vận, gia giảm.
Nêu 2–4 trọng tâm có căn cứ, không gán xác suất hoặc độ nặng thực tế.
Dẫn tên nguồn A/B và mục/bảng của dữ liệu được cấp ngay tại đoạn liên quan.
Nếu thiếu dữ liệu, ghi rõ thiếu ở đâu; không thay thế bằng lời khẳng định.
"""


def token():
    """Chỉ đọc khóa từ phiên làm việc hoặc Streamlit Secrets; không ghi vào GitHub."""
    provider = st.session_state.get("ai_provider", "gemini")
    if provider == "gemini":
        typed, secret_name = "typed_gemini", "GEMINI_API_KEY"
    else:
        typed, secret_name = "typed_token", "HF_TOKEN"
    try:
        secret = st.secrets.get(secret_name, "")
    except Exception:
        secret = ""
    return str(st.session_state.get(typed, "") or secret).strip()


def friendly_error(exc):
    """Thông báo dễ hiểu thay cho tracebacks HTTP có thể chứa dữ liệu truy vấn."""
    text = str(exc)
    code = getattr(exc, "status_code", None)
    if code == 402 or "402" in text or "Payment Required" in text:
        return ("Hugging Face yêu cầu mua tín dụng để tiếp tục (HTTP 402). "
                "Hãy chọn 'Google Gemini' ở thanh bên trái để thử hạn mức miễn phí, "
                "hoặc nạp tín dụng nếu muốn tiếp tục dùng Hugging Face.")
    if code == 429 or "429" in text or "RESOURCE_EXHAUSTED" in text:
        return ("Dịch vụ AI đã chạm giới hạn lượt hoặc hạn mức. "
                "Hãy kiểm tra mục Usage/Rate limits của nhà cung cấp.")
    if code == 401 or "401" in text or "API_KEY_INVALID" in text:
        return "Khóa API không hợp lệ. Hãy tạo lại khóa của đúng nhà cung cấp."
    if code == 403 or "403" in text or "PERMISSION_DENIED" in text:
        return ("Tài khoản/khóa AI chưa được cấp quyền hoặc dịch vụ không hỗ trợ "
                "khu vực này. Kiểm tra thiết lập trên trang quản lý API.")
    if "404" in text or "NOT_FOUND" in text:
        return ("Mô hình không khả dụng với dự án/khóa API này (404). "
                "Google đã hạn chế Gemini 2.5 với một số dự án mới. "
                "Hãy chọn Gemini 3.5 Flash-Lite hoặc nhấn nút "
                "'Tự kiểm tra và chọn mô hình hoạt động'.")
    return "Dịch vụ AI chưa xử lý được yêu cầu. Hãy thử lại hoặc kiểm tra khóa và hạn mức."


def probe_gemini_models():
    """Thử một câu văn bản rất ngắn để xác minh quyền gọi API thực tế.
    models.list có thể hiển thị model nhưng generateContent vẫn bị 404.
    """
    from google import genai
    from google.genai import types
    key = token()
    if not key:
        raise ValueError("Chưa điền Google AI Studio API Key.")
    client = genai.Client(api_key=key)
    failures = []
    for candidate in GEMINI_MODELS[:3]:
        try:
            reply = client.models.generate_content(
                model=candidate,
                contents="Trả lời đúng một từ: OK",
                config=types.GenerateContentConfig(
                    max_output_tokens=48, temperature=0
                )
            )
            if reply.text:
                return candidate, failures
            failures.append(candidate + ": không có nội dung phản hồi")
        except Exception as error:
            failures.append(candidate + ": " + friendly_error(error))
    return None, failures


def infer(model, messages, maximum=4500):
    key = token()
    if not key:
        provider = st.session_state.get("ai_provider", "gemini")
        name = "Google AI Studio API Key" if provider == "gemini" else "Hugging Face Token"
        raise ValueError("Chưa có " + name + ". Các lá số mẫu vẫn tra cứu được không cần AI.")
    provider = st.session_state.get("ai_provider", "gemini")
    try:
        if provider == "gemini":
            from google import genai
            from google.genai import types
            contents = []
            for message in messages:
                content = message.get("content", "")
                if isinstance(content, str):
                    contents.append(content)
                elif isinstance(content, list):
                    for part in content:
                        if part.get("type") == "text":
                            contents.append(part.get("text", ""))
                        elif part.get("type") == "image_url":
                            data_url = part.get("image_url", {}).get("url", "")
                            if not data_url.startswith("data:image/") or "," not in data_url:
                                raise ValueError("Dữ liệu ảnh không đúng định dạng.")
                            image_bytes = base64.b64decode(data_url.split(",", 1)[1])
                            contents.append(Image.open(io.BytesIO(image_bytes)).convert("RGB"))
            client = genai.Client(api_key=key)
            response = client.models.generate_content(
                model=model, contents=contents,
                config=types.GenerateContentConfig(
                    temperature=0.1, max_output_tokens=maximum
                )
            )
            answer = response.text
            if not answer:
                raise RuntimeError("Gemini trả về nội dung rỗng.")
            return answer
        from huggingface_hub import InferenceClient
        client = InferenceClient(token=key, provider="auto", timeout=160)
        result = client.chat.completions.create(
            model=model, messages=messages, temperature=0.1, max_tokens=maximum
        )
        answer = result.choices[0].message.content
        if isinstance(answer, str):
            return answer
        return "\n".join(x.get("text", "") for x in answer if isinstance(x, dict))
    except (ValueError, RuntimeError) as exc:
        if isinstance(exc, ValueError) and ("Chưa có" in str(exc) or "Dữ liệu ảnh" in str(exc)):
            raise
        raise RuntimeError(friendly_error(exc)) from None
    except Exception as exc:
        raise RuntimeError(friendly_error(exc)) from None


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
        st.info("Chưa có **cách cục chuyên biệt** khớp đủ điều kiện trong thư viện thử nghiệm. Phần luận nền tảng vẫn có ở phía trên.")
    for item in items:
        with st.expander(item["title"] + " · " + item.get("group", item["kind"])):
            st.write(item["result"])
            for detail in item["details"]:
                st.write("• " + detail)
            st.caption("Nguồn: " + item.get("source", "—") +
                       " | Trang/mục: " + item.get("page", "—"))

with st.sidebar:
    st.subheader("Kết nối AI đọc lá số")
    provider = st.selectbox(
        "Dịch vụ AI", ["gemini", "huggingface"],
        format_func=lambda p: "Google Gemini (có hạn mức miễn phí)" if p == "gemini"
                               else "Hugging Face (có thể yêu cầu tín dụng)",
        key="ai_provider"
    )
    if provider == "gemini":
        st.text_input("Google AI Studio API Key", type="password", key="typed_gemini")
        model = st.selectbox("Mô hình đọc ảnh", GEMINI_MODELS, key="gemini_choice")
        st.markdown("[Lấy khóa API trên Google AI Studio](https://aistudio.google.com/app/apikey)")
        st.caption("Google hạn chế Gemini 2.5 với một số tài khoản mới. "
                   "Bản V1.2 ưu tiên Gemini 3.5 Flash-Lite; dịch vụ có giới hạn lượt và "
                   "có thể tính phí tùy tài khoản.")
        if st.button("🔎 Tự kiểm tra và chọn mô hình hoạt động", use_container_width=True):
            try:
                with st.spinner("Đang kiểm tra một yêu cầu văn bản rất ngắn..."):
                    working, failures = probe_gemini_models()
                if working:
                    st.session_state.working_model = working
                    st.success("AI kết nối thành công với " + working)
                else:
                    st.session_state.pop("working_model", None)
                    st.error("Chưa tìm thấy mô hình hoạt động với khóa này.")
                    with st.expander("Các lỗi phát hiện"):
                        for f in failures:
                            st.write("• " + f)
            except Exception as exc:
                st.error("Chưa kiểm tra được: " + str(exc))
        if st.session_state.get("working_model"):
            model = st.session_state.working_model
            st.success("Đang dùng mô hình đã kiểm tra: " + model)
        st.caption("Lưu ý: dữ liệu dùng ở gói miễn phí có thể được nhà cung cấp "
                   "sử dụng để cải thiện dịch vụ theo điều khoản của họ.")
    else:
        st.text_input("Hugging Face Token", type="password", key="typed_token")
        model = st.selectbox("Mô hình thị giác", HF_MODELS)
        st.markdown("[Hugging Face Tokens](https://huggingface.co/settings/tokens)")
        st.caption("Hugging Face có thể trả HTTP 402 nếu yêu cầu nạp tín dụng.")
    st.info("Ảnh được chuyển đến dịch vụ AI bạn chọn khi nhấn nút đọc ảnh. "
            "Không đăng API Key lên GitHub hoặc chia sẻ công khai.")

if "chart" not in st.session_state:
    st.session_state.chart = sample("giapty")
    st.session_state.last_choice = "giapty"
    st.session_state.revision = 0

st.title("☯️ AI TỬ VI · CHUYÊN ĐỀ TẬT – ÁCH")
st.write("Luận Tật gốc, Ách gốc, tính cách Mệnh–Tật và Tật–Ách đại vận.")
st.caption("V3 · Luận chuyên sâu theo bài mẫu · Tật gốc, Mệnh–Tật, đại vận · Có báo cáo không cần AI")

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

if st.button("✨ AI đọc 12 cung", type="primary", disabled=not bool(upload), use_container_width=True):
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
            st.session_state.pop("written", None)
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
            st.session_state.pop("written", None)
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
st.header("③ Báo cáo Tật – Ách chuyên sâu (V3)")
try:
    context = build_context(chart)
except ValueError as exc:
    st.warning(str(exc))
    st.stop()

layers = context["layers"]
metrics = st.columns(4)
for col, (label, key) in zip(metrics, [
    ("Mệnh gốc", "menh"), ("Tật gốc", "tat"),
    ("Mệnh đại vận", "dv"), ("Tật đại vận", "dvtat")
]):
    col.metric(label, layers[key]["anchor"])

if context["empty_houses"]:
    st.warning("Còn cung trống: " + ", ".join(context["empty_houses"]) +
               ". Có thể AI đọc thiếu. Kiểm tra ảnh trước khi luận.")
if context["omitted_non_original"]:
    st.caption("Sao L./LN./P./ĐV. được tách khỏi dữ liệu dùng để luận nguyên cục và đại vận.")

report = deterministic_report(context)
can_write = not bool(context["empty_houses"])
st.markdown("**Bài luận chuyên sâu bằng AI:** tổng hợp theo đúng sáu phần của bài mẫu, "
            "không chỉ liệt kê sao. Hãy kiểm tra đủ 12 cung trước khi nhấn.")
if st.button("🧠 Tạo bài luận chuyên sâu (V3)", type="primary",
             use_container_width=True, disabled=not can_write):
    st.session_state.pop("written", None)
    try:
        payload = {"menh": chart["menh"], "tat": chart["tat"], "dv": chart["dv"],
                   "dvAge": chart.get("dvAge",""), "context": context}
        with st.spinner("AI đang tổng hợp căn cứ của nguyên cục và đại vận..."):
            st.session_state.written = infer(model, [
                {"role":"system","content":WRITE_PROMPT},
                {"role":"user","content":json.dumps(payload,ensure_ascii=False)}
            ], maximum=7500 if st.session_state.get("ai_provider")=="gemini" else 4096)
    except Exception as exc:
        st.error("Chưa tạo được bài luận AI: " + str(exc))

if st.session_state.get("written"):
    st.subheader("Bài luận tổng hợp bằng AI")
    st.caption("Diễn giải từ bảng căn cứ. Cần đối chiếu lại các sao, quan hệ và nguồn; không phải chẩn đoán.")
    st.markdown(st.session_state.written)
    st.download_button("⬇️ Lưu bài luận AI (.txt)",
                       st.session_state.written.encode("utf-8-sig"),
                       "Luan_giai_Tat_Ach_V3.txt","text/plain")

st.subheader("Báo cáo căn cứ tự động (không cần API Key)")
st.caption("Nguồn A được ưu tiên; các tổ hợp đủ thành phần chưa mặc nhiên đủ điều kiện thành cách. "
           "Báo cáo này là bảng chứng cứ có cấu trúc để kiểm tra và dùng khi dịch vụ AI gặp lỗi.")
parts = re.split(r"(?m)^## (?=I{1,3}\\.|IV\\.|V\\.)", report)
if len(parts) > 1:
    st.markdown(parts[0])
    for p in parts[1:]:
        heading, _, rest = p.partition("\n")
        with st.expander(heading.strip(), expanded=False):
            st.markdown(rest)
else:
    st.markdown(report)
st.download_button("⬇️ Lưu báo cáo căn cứ (.txt)", report.encode("utf-8-sig"),
                   "Bao_cao_can_cu_Tat_Ach_V3.txt","text/plain")

with st.expander("Bảng quan hệ 4 cung trọng tâm"):
    for k, title in [("menh","Mệnh gốc"),("tat","Tật gốc"),("dv","Mệnh đại vận"),("dvtat","Tật đại vận")]:
        st.markdown("**"+title+" — "+layers[k]["anchor"]+"**")
        st.dataframe([{"Quan hệ":e["relation"],"Cung":e["chi"],
                       "Nhãn":e["house"],"Sao":", ".join(e["stars"])}
                      for e in layers[k]["evidence"]],hide_index=True,use_container_width=True)
with st.expander("Kho công thức nguồn A"):
    st.caption("Các tổ hợp tra cứu được mã hóa. Điều kiện hội cụ thể cần đối chiếu nguồn.")
    st.dataframe([{"Mã":ident,"Loại":kind,"Nhóm":group,"Bộ sao":" – ".join(stars),
                   "Ý nghĩa tra cứu":meaning,"Mục":sec}
                   for ident,kind,group,stars,meaning,sec in FORMULAS],
                  hide_index=True,use_container_width=True)

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
