# 🛡️ On-Device Scam & Phishing Detector
Built for the Snapdragon AI Lab Build & Present Challenge

## Problem
India mein har din lakhs scam SMS, UPI fraud aur phishing links aate hain. Cloud-based checkers mein user ka private message bahar jaata hai.

## Solution
Ek local app jo SMS/email/link ko laptop par hi analyze karta hai. **Zero data cloud par.**

## How it works
1. Open-source BERT-tiny spam model (Hugging Face) -> ONNX format
2. ONNX Runtime se inference; Snapdragon NPU ke liye QNN Execution Provider support code mein already hai
3. Rule engine Indian scam patterns pakadta hai (KYC, OTP, UPI refund, lottery)
4. Gradio UI: verdict + reasons + hardware info + benchmark button

## Current status
- Tested on CPU (AMD Ryzen laptop)
- Designed and intended to be optimised for Snapdragon NPU via QNN
- NPU benchmark: pending, Snapdragon hardware par test hona baaki hai

## Run
    pip install -r requirements.txt
    python export_model.py
    python app.py

Snapdragon laptop par sirf ye extra: `pip install onnxruntime-qnn`

## Future work
Hindi/Hinglish model, browser extension, WhatsApp forward checker, Qualcomm AI Hub se quantized model.

## Author
Rahul
