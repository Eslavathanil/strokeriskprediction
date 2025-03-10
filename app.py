import numpy as np
from flask import Flask, request, render_template
import pickle

app = Flask(__name__)
sc = pickle.load(open('sc.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict',methods=['POST'])
def predict():
    lst = []
    cp = int(request.form['chest pain type'])
    if cp == 0:
        lst += [1 , 0 ,0 ,0]
    elif cp == 1:
        lst += [0 ,1 ,0 ,0]
    elif cp == 2:
        lst += [0 ,0 ,1 ,0]
    elif cp >= 3:
        lst += [0 ,0 ,0 ,1]
    trestbps = int(request.form["resting blood pressure" ])
    lst += [trestbps]
    chol = int(request.form["serum cholesterol"])
    lst += [chol]
    fbs = int(request.form["fasting blood sugar > 120 mg/dl"])
    if fbs == 0:
        lst += [1 , 0]
    else:
        lst += [0 , 1]
    restecg = int(request.form["resting ECG results(0-2)"])
    if restecg == 0:
        lst += [1 ,0 ,0]
    elif restecg == 1:
        lst += [0 ,1 ,0]
    else:
        lst += [0 , 0,1]
    thalach = int(request.form["maximum heart rate"])
    lst += [thalach]
    exang = int(request.form["exercise-induced angina"])
    if exang == 0:
        lst += [1 , 0]
    else:
        lst += [0 ,1 ]
    final_features = np.array([lst])
    pred = model.predict( sc.transform(final_features))
    return render_template('result.html', prediction = pred)

if __name__ == "__main__":
    app.run(debug=True)
