from flask import Flask
from flask import render_template,request
from datetime import date
import numpy as np
import math
import random
import re


app = Flask(__name__)

@app.route("/")
@app.route("/",methods=["POST"])
def register():
    result=dict()
    result["Date package"]=date.today()
    result["Numpy Package"]="Average of 1 to 10 is "+str(np.average(np.arange(1,10)))
    result["Math package"]="2 power 3 is "+ str(math.pow(2,3))
    result['Random package']="This is a random number from 1 to 10: "+str(random.randint(1,10))
    pattern = '\d+'
    test_string = 'Twenty:20, Three:3.'
    result["Regex package"] = "Original String=={str}. After regex--->>> ".format(str=test_string)+ str(re.split(pattern, test_string))

    return render_template("display.html",result=result)