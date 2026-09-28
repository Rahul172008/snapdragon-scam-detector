# Step 1: ek baar chalao (internet chahiye). Model ko ONNX mein convert karta hai.
from optimum.onnxruntime import ORTModelForSequenceClassification
from transformers import AutoTokenizer

NAME = "mrm8488/bert-tiny-finetuned-sms-spam-detection"
model = ORTModelForSequenceClassification.from_pretrained(NAME, export=True)
tok = AutoTokenizer.from_pretrained(NAME)
model.save_pretrained("model")
tok.save_pretrained("model")
print("Done: model/ folder ready")
