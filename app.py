from flask import Flask, request, jsonify, render_template
import torch
from transformers import RobertaForSequenceClassification, AutoTokenizer

app = Flask(__name__)

# Load the trained model and tokenizer
model = RobertaForSequenceClassification.from_pretrained("roberta-base", num_labels=3)  # Ensure num_labels=3
import joblib
model_path= "model.pkl"
model = joblib.load("model.pkl")  # Load model.pkl instead
model.eval()

tokenizer = AutoTokenizer.from_pretrained("roberta-base")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        text = request.form["text"]

        # Tokenize input
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

        # Get model predictions
        with torch.no_grad():
            outputs = model(**inputs)

        # Get predicted class
        predicted_class = torch.argmax(outputs.logits, dim=1).item()

        sentiment_mapping = {0: "Negative", 1: "Neutral", 2: "Positive"}
        sentiment_label = sentiment_mapping.get(predicted_class, "Unknown")

        return render_template("index.html", prediction=sentiment_label)

    return render_template("index.html", prediction=None)

if __name__ == "__main__":
    app.run(debug=True)
