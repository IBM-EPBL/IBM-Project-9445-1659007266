from urllib import request
from flask import Flask
from flask import render_template,request

app = Flask(__name__)

@app.route("/")
@app.route("/",methods=["POST"])
def register():
    if request.method=="POST":
        result=request.form
        print(result)
        return render_template("display.html",result=result)
    return render_template("register.html")