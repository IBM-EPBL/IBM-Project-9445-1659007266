from flask import Flask, render_template, redirect, url_for, request, session, flash, Markup
import ibm_db
import sendgrid #Email API
import os
from dotenv import load_dotenv  #API that exposes environmental variables into the program
from sendgrid.helpers.mail import Mail, Email, To, Content  #Additional Email Helper Classes


app = Flask(__name__)

load_dotenv()   #load keys from .env

#secret key required to maintain unique user sessions
app.secret_key = os.environ.get('APP_KEY')

#establish connection with IBM Db2 Database
connection = ibm_db.connect("DATABASE=bludb;HOSTNAME=824dfd4d-99de-440d-9991-629c01b3832d.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=qfz71349;PWD=ycPT38SnjYee8oqD;","","")

#Email Prerequisites
sg = sendgrid.SendGridAPIClient(api_key = os.environ.get('SENDGRID_API_KEY'))   #set SendGrid API Key
from_email = Email("pnt2022tmi14769@gmail.com")     #the address that sends emails to the users

@app.route('/')
@app.route('/dashboard')
def dashboard():
    if not session:
        return redirect(url_for('signin'))  #ask user to sign in if not done already

    return render_template('dashboard.html')  #go to homepage if signed in




@app.route('/signout')
def signout():
    session.clear()   #remove user session upon signing out
    return redirect('/')




@app.route('/register')
def register():
    if 'UID' in session:   #inform user if they're already signed in the same session
        flash('You are already logged in! Sign out to login with a different account')
        return redirect(url_for('dashboard'))

    else:
        return render_template('register.html') #take user to the registration page




@app.route('/regform', methods=['POST'])
def regform():
    #get user details from the registration form
    uname = request.form['uname']
    uid = request.form['uid']       #Selected contact id type
    pwd = request.form['pwd']
    dtype = request.form['dtype']   #donor/patient user type

    sql = 'SELECT * from ' + dtype + ' WHERE uid=?'   #check if user is already registered
    pstmt = ibm_db.prepare(connection, sql)
    ibm_db.bind_param(pstmt, 1, uid)
    ibm_db.execute(pstmt)

    acc = ibm_db.fetch_assoc(pstmt)

    if acc:     #inform user to sign in if they have an existing account
        flash('You are already a registered member. Please sign in using your registered credentials')

    else:
        sql = 'INSERT INTO ' + dtype + ' (uid, pwd, uname) VALUES(?,?,?)' #insert credentials of new user to the database
        pstmt = ibm_db.prepare(connection, sql)
        ibm_db.bind_param(pstmt, 1, uid)
        ibm_db.bind_param(pstmt, 2, pwd)
        ibm_db.bind_param(pstmt, 3, uname)
        ibm_db.execute(pstmt)


        to_email = To(uid)   #set user as recipient for confirmation email
        subject = "Welcome to Plasma Donor"
        content = Content("text/html", "<p>Hello " + uname + ",</p><p>Thank you for registering to the Plasma Donor Application!</p><p>If it wasn't you, then report it to our <a href=\"mailto:pnt2022tmi14769@gmail.com\">admin</a> or reply to this email.</p>")
        email = Mail(from_email, to_email, subject, content) #construct email format
        email_json = email.get()    #get JSON-ready representation of the mail object
        response = sg.client.mail.send.post(request_body = email_json)  #send email by invoking an HTTP/POST request to /mail/send
        
        flash('Registration Successful! Sign in using the registered credentials to continue')


    return redirect(url_for('signin'))  #ask users to sign in after registration



@app.route('/signin')
def signin():
    if 'UID' in session:   #inform user if they're already signed in the same session
        flash('You are already signed in! Sign out to login with a different account')
        return redirect(url_for('dashboard'))
    return render_template('signin.html')   #take user to the sign in page




@app.route('/signin_form', methods=['POST'])
def signinform():
    uid = request.form['uid']   #get user id and password from the form
    pwd = request.form['pwd']
    dtype = request.form['dtype']

    sql = 'SELECT * from ' + dtype + ' WHERE uid=? AND pwd=?' #check user credentials in the database
    pstmt = ibm_db.prepare(connection, sql)
    ibm_db.bind_param(pstmt, 1, uid)
    ibm_db.bind_param(pstmt, 2, pwd)
    ibm_db.execute(pstmt)

    acc = ibm_db.fetch_assoc(pstmt)
    
    if acc: #if the user is already registered to the application
        for keys, vals in acc.items():
            session[keys] = vals
        session['DTYPE'] = dtype
        flash('Signed in successfully!')
        return redirect(url_for('dashboard'))
        
    else:   #warn upon entering incorrect credentials
        flash('Incorrect credentials. Please try again!')
        return render_template('signin.html')


@app.route('/medform', methods=['POST'])
def medform():
    #get user details from the registration form
    uname = request.form['uname']
    uid = request.form['uid']       #Selected contact id type
    uage = request.form['uage']
    gender = request.form['gender']
    weight = request.form['weight']
    bgroup = request.form['bgroup']
    rh = request.form['rh']
    dtype = session['DTYPE']  #donor/patient user type
    addr = request.form['addr']
    city = request.form['city']
    st = request.form['st']
    zip = request.form['zip']

    #update user's medical and contact details
    sql = f"UPDATE {dtype} SET uname=?, uage=?, gender=?, weight=?, bgroup=?, rh=?, addr=?, city=?, st=?, zip=? WHERE uid=?"
    pstmt = ibm_db.prepare(connection, sql)
    param = uname, uage, gender, weight, bgroup, rh, addr, city, st, zip, uid
    ibm_db.execute(pstmt, param)

    sql = 'SELECT * from ' + dtype + ' WHERE uid=?'
    pstmt = ibm_db.prepare(connection, sql)
    ibm_db.bind_param(pstmt, 1, uid)
    ibm_db.execute(pstmt)

    res = ibm_db.fetch_assoc(pstmt)

    if res:
        flash('Profile updated successfully')
        for keys, vals in res.items():
            session[keys] = vals
    else:
        flash('Error occured while trying to update the profile')

    return redirect(url_for('dashboard'))


@app.route('/donors')
def donors():
    sql = 'SELECT uid, uname, uage, gender, weight, bgroup, rh, addr, city, st, zip from DONOR'
    stmt = ibm_db.exec_immediate(connection, sql)
    
    donor_list = {}
    i=0
    while (res:=ibm_db.fetch_assoc(stmt)) != False:
        donor_list[i] = res
        i+=1

    return render_template('donors.html', donors = donor_list)