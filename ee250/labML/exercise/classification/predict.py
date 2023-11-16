# Owen Zeng
# Felix Chen
# GitHub Repo: https://github.com/usc-ee250-fall2023/lab09-ml-lab09-owen-felix.git
# We made changes to predict.py as well because our model has the output of 0 or 1 instead of 1 or 2
# The change is approved by the Instructor
import pickle
from flask import Flask,request
import json

clf = pickle.load(open('model.pickle','rb'))


app = Flask(__name__)

@app.route("/classify")
def hello_world():
    weight = float(request.args.get('w'))
    reflectance = float(request.args.get('r'))

    # find the possibility from 0 to 1, it will be a float number
    predicted_possiblility = clf.predict([[reflectance, weight]])[0][0]
    # change the denomination from 0-1 to 1-2
    denomination = round(predicted_possiblility) + 1

    #print(denomination)
    return json.dumps({"weight":weight, "reflectance":reflectance ,"denomination":denomination})
