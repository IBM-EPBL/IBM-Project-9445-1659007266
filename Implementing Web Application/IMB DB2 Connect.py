import ibm_db
conn=ibm_db.connect("DRIVER='{IBM DB2 ODBC DRIVER}';DATABASE=bludb;HOSTNAME=824dfd4d-99de-440d-9991-629c01b3832d.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30119;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=qfz71349;PWD=ycPT38SnjYee8oqD;","","")
email='digeesh@gmail.com'
password='digeesh123'
username='Digeesh'
rollNumber='12335'
sql = "insert into users values('"+email+"','"+username+"','"+rollNumber+"','"+password+"')"
stat = ibm_db.exec_immediate(conn,sql)
print(stat)
