# Step 2: python app.py
import re, time, numpy as np, onnxruntime as ort, gradio as gr
from transformers import AutoTokenizer

MAX_LEN = 128
tok = AutoTokenizer.from_pretrained("model")

def make_session(prefer_npu=True):
    avail = ort.get_available_providers()
    if prefer_npu and "QNNExecutionProvider" in avail:
        return ort.InferenceSession(
            "model/model.onnx",
            providers=[("QNNExecutionProvider", {"backend_path": "QnnHtp.dll"}),
                       "CPUExecutionProvider"])
    return ort.InferenceSession("model/model.onnx", providers=["CPUExecutionProvider"])

sess_fast = make_session(True)
sess_cpu = make_session(False)
ACTIVE = sess_fast.get_providers()[0]

def run(sess, text):
    enc = tok(text, padding="max_length", truncation=True,
              max_length=MAX_LEN, return_tensors="np")
    names = {i.name for i in sess.get_inputs()}
    feed = {k: v.astype(np.int64) for k, v in enc.items() if k in names}
    logits = sess.run(None, feed)[0][0]
    p = np.exp(logits - logits.max()); p /= p.sum()
    return float(p[1])  # index 1 = spam (config check kar lena)

RULES = [
    (r"https?://|bit\.ly|tinyurl|t\.co", "Link mila (shortened/unknown links risky hote hain)"),
    (r"\botp\b|\bpin\b|\bcvv\b", "OTP/PIN/CVV maanga ja raha hai"),
    (r"\bkyc\b|account.*(block|suspend)|band ho", "KYC/account block ka darr dikhaya"),
    (r"upi|paytm|phonepe|gpay|refund|cashback", "UPI/refund/cashback ka lalach"),
    (r"urgent|immediately|abhi|turant|24 hours|last chance", "Jaldi karne ka pressure"),
    (r"lottery|winner|congratulations|jeet|prize|reward", "Inaam/lottery ka claim"),
    (r"apk|install app|download app", "App install karne ko kaha"),
]

def analyze(text):
    if not text.strip():
        return "Kuch paste karo", "", ""
    score = run(sess_fast, text)
    hits = [msg for pat, msg in RULES if re.search(pat, text, re.I)]
    score = min(1.0, score + 0.25 * len(hits))
    label = "🚨 SCAM" if score > 0.7 else "⚠️ SUSPICIOUS" if score > 0.4 else "✅ SAFE"
    reasons = "\n".join(f"- {h}" for h in hits) or "- Koi red flag nahi mila"
    return f"{label}  ({score*100:.0f}% risk)", reasons, f"Running on: {ACTIVE}"

def benchmark(n=50):
    t = "Your KYC is pending. Click http://bit.ly/x and share OTP immediately"
    out = []
    for name, s in [("CPU", sess_cpu), (ACTIVE.replace("ExecutionProvider", ""), sess_fast)]:
        run(s, t)  # warmup
        st = time.perf_counter()
        for _ in range(n): run(s, t)
        out.append(f"{name}: {(time.perf_counter()-st)/n*1000:.1f} ms/inference")
    return "\n".join(out)

with gr.Blocks(title="On-Device Scam Detector") as demo:
    gr.Markdown("# 🛡️ On-Device Scam & Phishing Detector\nSab kuch laptop par local chalta hai, koi data cloud par nahi jaata.")
    inp = gr.Textbox(lines=5, label="SMS / Email / Link paste karo")
    btn = gr.Button("Check karo")
    verdict = gr.Textbox(label="Result")
    why = gr.Textbox(label="Kyun?", lines=4)
    hw = gr.Textbox(label="Hardware")
    btn.click(analyze, inp, [verdict, why, hw])
    gr.Markdown("### ⚡ Benchmark")
    bbtn = gr.Button("CPU vs NPU test")
    bout = gr.Textbox(label="Latency")
    bbtn.click(lambda: benchmark(), None, bout)

demo.launch()