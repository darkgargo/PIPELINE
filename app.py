from flask import Flask,render_template,flash,session
from flask.globals import request
from flask.helpers import flash
import pymysql
import mysql.connector
import requests

app = Flask(__name__)


@app.route('/')
def index():
    b=call_all_id()
    id_list=[]
    for i in range(len(b)):
        id_list.append(b[i][0]) 
    return render_template('SignUp.html',id_list=id_list)
  #메인화면 route haha!!!


#회원 가입 진행시 Route
@app.route('/Sign-Up', methods=['GET','POST'])
def post():
    if request.method == 'POST':
        value = request.form['id_name']
        value =str(value)
        value2=request.form['pw_name']
        value2=str(value2)
        value3=request.form['name_name']
        value3=str(value3)
        insert_table(value,value2,value3) #테이블에 ID,PW,NAME 입력
        b=call_all_id()
        id_list=[]
        for i in range(len(b)):
            id_list.append(b[i][0]) 
        return render_template('SignIn.html',id_list=id_list)
        
#로그인 진행
@app.route('/Sign-In', methods=['GET','POST'])
def post2():
    if request.method=='POST':
        value=request.form['id_name']
        value2=request.form['pw_name']
        value=str(value)
        value2=str(value2)
        value3=call_all_id()
        all_id=[]
        for i in range(len(value3)):
            all_id.append(value3[i][0])
        flag=funclength(value,value2) #ID,PW 비교
        if flag==1:
             return render_template('node.html')
        else:
            return "WRONG ID OR PASSWORD"
        
@app.route('/Move',methods=['GET','POST'])
def post3():
    return render_template('SignIn.html')


@app.route('/Move2',methods=['GET','POST'])
def post4():
    b=call_all_id()
    id_list=[]
    for i in range(len(b)):
        id_list.append(b[i][0])
    return render_template('SignUp.html',id_list=id_list)

#DB CONN 함수
def connsql():
    cnx = mysql.connector.connect(user="dbmaster@teamaks-db", password="rkskek123#@!", host="teamaks-db.mariadb.database.azure.com", port=3306, database="SignIn")
    return cnx

#ID,PW 확인용 함수
def funclength(a,b):
    cnx=connsql()
    cursor = cnx.cursor()

    sql="select id from aksmember where id = %s and password=%s" %(a,b)

    cursor.execute(sql)

    dbCheckArr = []

    for row in cursor:
        dbCheckArr.append(row)

    cnx.close()

    return len(dbCheckArr)


#모든 ID 호출
def call_all_id():
    cnx=connsql()
    cursor = cnx.cursor()
    queryArr = []

    queryArr.append("SELECT")

    queryArr.append("id")

    queryArr.append("FROM aksmember")

    queryStr = " ".join(queryArr)

    cursor.execute(queryStr)

    dbCheckArr = []

    for row in cursor:
        dbCheckArr.append(row)

    cnx.close()

    return dbCheckArr

#모든 PW 호출
def call_all_pw():
    cnx=connsql()
    cursor = cnx.cursor()
    queryArr = []

    queryArr.append("SELECT")

    queryArr.append("password")

    queryArr.append("FROM aksmember")

    queryStr = " ".join(queryArr)

    cursor.execute(queryStr)

    dbCheckArr = []

    for row in cursor:
        dbCheckArr.append(row)

    cnx.close()

    return dbCheckArr

#특정 ID 호출 
def call_id(value):
    cnx=connsql()
    cursor = cnx.cursor()

    sql="select id from aksmember where id ='%s'" %(value)


    cursor.execute(sql)

    dbCheckArr = []

    for row in cursor:
        dbCheckArr.append(row)

    cnx.close()

    return dbCheckArr

#특정 PW 호출
def call_pw(value):
    cnx=connsql()
    cursor = cnx.cursor()

    sql="select password from aksmember where id ='%s'" %(value)

    cursor.execute(sql)

    dbCheckArr = []

    for row in cursor:
        dbCheckArr.append(row)

    cnx.close()

    return dbCheckArr

#TABLE INSERT 함수
def insert_table(ID,PW,NAME):
    cnx=connsql()
    cursor=cnx.cursor()
    sql="INSERT INTO aksmember VALUES('%s','%s','%s')" %(ID,PW,NAME)
    cursor.execute(sql)
    cnx.commit()
    cnx.close()
    return 0;

def checkid(id):
    cnx=connsql()
    cursor=cnx.cursor()
    a=call_all_id()
    all_id=[]
    for i in range(len(a)):
        all_id.append(a[i][0])
    if id in all_id:
        return 0
    else:
        return 1

if __name__ == '__main__':
    app.run(host='0.0.0.0')
