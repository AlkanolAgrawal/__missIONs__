from flask import Flask, request, jsonify,render_template
import numpy as np
import os
import pandas as pd
from src.pipelines.predict_pline import PredictPipeline, CustomData
from sklearn.preprocessing import StandardScaler


app = Flask(__name__)


# Route Home
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method=='GET':
        return render_template('predict.html')
    else:
        data = CustomData(
            gender=request.form.get('gender'),
            reading_score=float(request.form.get('reading_score')),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            writing_score=float(request.form.get('writing_score')),
            test_preparation_course=request.form.get('test_preparation_course'),
            race_ethnicity=request.form.get('race_ethnicity'),
            lunch=request.form.get('lunch'),
        )
        pred_df = data.get_data_as_dataframe()
        print("Pred DF columns:", pred_df.columns.tolist())  # Debug columns
        print(pred_df)  # Debug content
        predicting = PredictPipeline()
        results = predicting.prediction(pred_df)

        return render_template('predict.html', prediction=results)
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)