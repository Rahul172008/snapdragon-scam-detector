# 🛡️ On-Device Scam & Phishing Detector (Snapdragon AI Lab Challenge)

## Problem
India mein har din lakhs scam SMS, UPI fraud aur phishing links aate hain. Cloud-based checkers mein user ka private message bahar jaata hai.

## Solution
Ek local app jo SMS/email/link ko laptop par hi analyze karta hai. **Zero data cloud par.**

## How it works
1. Open-source BERT-tiny spam model (Hugging Face) -> ONNX
2. ONNX Runtime + QNN Execution Provider se Snapdragon NPU par inference
3. Rule engine Indian scam patterns pakadta hai (KYC, OTP, UPI refund, lottery)
4. Gradio UI: verdict + reasons + CPU vs NPU benchmark

## Run
```
pip install -r requirements.txt
python export_model.py
python app.py
```

## Benchmark (Snapdragon X, meri machine par)
| Backend | Latency |
|---|---|
| CPU | __ ms |
| NPU (QNN) | __ ms |

## Future work
Hindi/Hinglish model, browser extension, WhatsApp forward checker.

## Author
Rahul
