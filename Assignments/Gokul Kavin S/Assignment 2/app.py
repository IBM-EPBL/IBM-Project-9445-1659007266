from unittest import result
from urllib import request
from flask import Flask
from flask import render_template,request
import ibm_db
app = Flask(__name__)


@app.route("/")
@app.route("/",methods=["POST"])
def register():
    if request.method=="POST":  
        conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=824dfd4d-99de-440d-9991-629c01b3832d.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=qfz71349;PWD=ycPT38SnjYee8oqD;","","")
        result=request.form
        email=result.get('Email')
        username=result.get('UserName')
        rollNumber=result.get('RollNumber')
        password=result.get('Password')
        print(email+rollNumber+password)
        sql = "insert into users values('"+email+"','"+username+"','"+rollNumber+"','"+password+"')"
        if ibm_db.exec_immediate(conn,sql)!=None:
            return render_template("login.html")
    return render_template("register.html")

@app.route("/login")
@app.route("/login",methods=["POST"])
def login():
    if request.method=="POST":  
        conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=824dfd4d-99de-440d-9991-629c01b3832d.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30119;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=qfz71349;PWD=ycPT38SnjYee8oqD;","","")
        result=request.form
        email=result.get('Email')
        password=result.get('Password')
        sql="select username from users where email='"+email+"'and passwd = '"+password+"'"
        stmt=ibm_db.exec_immediate(conn,sql)
        out=ibm_db.fetch_tuple(stmt)
        if out!=None:
            return render_template("welcome.html",result=out)     
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
