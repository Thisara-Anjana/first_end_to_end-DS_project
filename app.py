from flask import Flask, render_template_string, request
import os
import sys
import numpy as np
from src.datascience.pipeline.prediction_pipeline import PredictionPipeline

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wine Quality Predictor</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            color: #1f2937;
        }
        .container { max-width: 900px; margin: 40px auto; padding: 24px; }
        .card { background: white; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.12); padding: 24px; }
        h1 { margin-top: 0; color: #111827; }
        .grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }
        .field { display: flex; flex-direction: column; gap: 6px; }
        input { padding: 10px 12px; border: 1px solid #d1d5db; border-radius: 8px; font-size: 14px; }
        .actions { display: flex; gap: 12px; margin-top: 20px; }
        button { border: none; border-radius: 8px; padding: 10px 16px; cursor: pointer; font-size: 15px; font-weight: 600; }
        .primary { background: #2563eb; color: white; }
        .secondary { background: #e5e7eb; color: #111827; }
        .result { margin-top: 18px; padding: 14px; border-radius: 8px; background: #ecfeff; color: #0f172a; }
        .error { margin-top: 18px; padding: 14px; border-radius: 8px; background: #fee2e2; color: #991b1b; }
        @media (max-width: 768px) { .grid { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>Wine Quality Prediction</h1>
            <p>Enter the wine features below and get a quality prediction from the backend model.</p>
            <form action="/predict" method="post">
                <div class="grid">
                    <div class="field"><label for="fixed_acidity">Fixed Acidity</label><input type="text" name="fixed_acidity" id="fixed_acidity" required></div>
                    <div class="field"><label for="volatile_acidity">Volatile Acidity</label><input type="text" name="volatile_acidity" id="volatile_acidity" required></div>
                    <div class="field"><label for="citric_acid">Citric Acid</label><input type="text" name="citric_acid" id="citric_acid" required></div>
                    <div class="field"><label for="residual_sugar">Residual Sugar</label><input type="text" name="residual_sugar" id="residual_sugar" required></div>
                    <div class="field"><label for="chlorides">Chlorides</label><input type="text" name="chlorides" id="chlorides" required></div>
                    <div class="field"><label for="free_sulfur_dioxide">Free Sulfur Dioxide</label><input type="text" name="free_sulfur_dioxide" id="free_sulfur_dioxide" required></div>
                    <div class="field"><label for="total_sulfur_dioxide">Total Sulfur Dioxide</label><input type="text" name="total_sulfur_dioxide" id="total_sulfur_dioxide" required></div>
                    <div class="field"><label for="density">Density</label><input type="text" name="density" id="density" required></div>
                    <div class="field"><label for="pH">pH</label><input type="text" name="pH" id="pH" required></div>
                    <div class="field"><label for="sulphates">Sulphates</label><input type="text" name="sulphates" id="sulphates" required></div>
                    <div class="field"><label for="alcohol">Alcohol</label><input type="text" name="alcohol" id="alcohol" required></div>
                </div>
                <div class="actions">
                    <button type="submit" class="primary">Predict Quality</button>
                    <a href="/train"><button type="button" class="secondary">Run Training Pipeline</button></a>
                </div>
            </form>
            {% if prediction_text %}
            <div class="result"><strong>Prediction:</strong> {{ prediction_text }}</div>
            {% endif %}
            {% if error_message %}
            <div class="error">{{ error_message }}</div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""


@app.route('/', methods=['GET'])
def homePage():
    return render_template_string(HTML_TEMPLATE, prediction_text="", error_message="")


@app.route('/train', methods=['GET'])
def training():
    os.system(f'"{sys.executable}" main.py')
    return render_template_string(HTML_TEMPLATE, prediction_text="Training pipeline started successfully.", error_message="")


@app.route('/predict', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            data = [
                float(request.form['fixed_acidity']),
                float(request.form['volatile_acidity']),
                float(request.form['citric_acid']),
                float(request.form['residual_sugar']),
                float(request.form['chlorides']),
                float(request.form['free_sulfur_dioxide']),
                float(request.form['total_sulfur_dioxide']),
                float(request.form['density']),
                float(request.form['pH']),
                float(request.form['sulphates']),
                float(request.form['alcohol']),
            ]
            values = np.array(data).reshape(1, 11)
            prediction = PredictionPipeline().predict(values)
            return render_template_string(HTML_TEMPLATE, prediction_text=str(prediction), error_message="")
        except Exception as e:
            return render_template_string(HTML_TEMPLATE, prediction_text="", error_message=f"Something went wrong: {e}")

    return render_template_string(HTML_TEMPLATE, prediction_text="", error_message="")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
