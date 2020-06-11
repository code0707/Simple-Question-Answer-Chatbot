import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

import numpy as np
import pandas as pd
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    a = [str(x) for x in request.form.values()]
    
    QnAdata = pd.read_csv("qa.csv")

    output = ""

    flag=0
    for i in range(len(QnAdata)):
        if(fuzz.ratio(QnAdata["Questions"][i],a)>80 or fuzz.partial_ratio(QnAdata["Questions"][i],a)>80 or fuzz.token_sort_ratio(QnAdata["Questions"][i],a)>80):
            output = (QnAdata["Answers"][i])
            flag=1
            break
    if(flag==0):
        output = ("Soryy I don't know")

    return render_template('index.html', prediction_text='Chatbot Replied: {}'.format(output))

@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)