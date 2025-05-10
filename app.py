from flask import Flask,render_template,request
import pymysql


app = Flask(__name__)

db_config = {
    "host" : "localhost",
    "user" : "root",
    "password" : "root",
    "database" : "atm"
    }


@app.route("/")
def landing():
    return render_template("home.html")

@app.route("/withdraw")
def withdraw():
    return render_template("withdraw.html")

@app.route("/withdraw2.html",methods=["POST","GET"])
def withdraw2():
    accno = request.form["accno"]
    pin = request.form["pin"]

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM ACCOUNTS WHERE USER_ACCNO = %s"
    cursor.execute(query,(accno))
    data = cursor.fetchone()
    conn.close()
    print(data)
    if data is None:
        return render_template("withdraw.html",msg="noaccount")
    elif data[-2] is None:
        return render_template("withdraw.html",msg="nopin")
    elif data[-2] != int(pin):
        return render_template("withdraw.html",msg="wrongpin")
    else:
        return render_template("withdraw2.html",user_name=data[1],accno=accno)


    
@app.route("/withdraw3",methods=["POST","GET"])
def withdraw3():
    accno = request.form["accno"]
    amount = request.form["amount"]
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query ="SELECT USER_BALANCE,USER_NAME FROM ACCOUNTS WHERE USER_ACCNO = %s"
    cursor.execute(query,(accno))
    data = cursor.fetchone()
    conn.close()
    print(data)
    if int(amount) <= int(data[0]):
        balance =int(data[0]) - int(amount)
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query ="UPDATE ACCOUNTS SET USER_BALANCE = %s WHERE USER_ACCNO = %s"
        cursor.execute(query,(balance,accno))
        conn.commit()
        conn.close()
        return render_template("withdraw2.html",msg="balance",accno=accno,user_name=data[1])
    else:
        return render_template("withdraw2.html",msg="nobalance",accno=accno,user_name=data[1])

@app.route("/diposit1")
def deposit1():
    return render_template("diposit.html")

@app.route("/diposit2",methods=["POST","GET"])
def diposit2():
    accno = request.form["accno"]
    amount = int(request.form["amount"])

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query ="SELECT USER_BALANCE,USER_NAME FROM ACCOUNTS WHERE USER_ACCNO = %s"
    cursor.execute(query,(accno))
    data = cursor.fetchone()
    conn.close()
    print(data)
    if data is None:
        return render_template("diposit.html",msg="noaccount")
    else:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query ="UPDATE ACCOUNTS SET USER_BALANCE = USER_BALANCE + %s WHERE USER_ACCNO = %s"
        cursor.execute(query,(amount,accno))
        conn.commit()
        conn.close()
        return render_template("diposit.html",msg="accnt")
    
@app.route("/mini_statement1")
def min_statement():
    return render_template("mini_statement.html")
    
@app.route("/mini_statement2",methods=["POST","GET"])
def mini_statement():
    accno = request.form["accno"]
    pin = request.form["pin"]

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query ="SELECT USER_BALANCE,USER_NAME,USER_PIN,USER_EMAIL FROM ACCOUNTS WHERE USER_ACCNO = %s"
    cursor.execute(query,(accno))
    data = cursor.fetchone()
    conn.close()
    print(data)

    if data is None:
        return render_template("mini_statement.html",msg="noaccount")
    elif int(data[2]) != int(pin):
        return render_template("mini_statement.html",msg="wrongpin")
    elif data[2] is None:
        return render_template("mini_statement.html",msg="nopin")
    else:
        name = data[1]
        email =data[-1]
        balance =data[0]
        return render_template("mini_statement2.html",accno=accno,name=name,email=email,balance=balance)
    
@app.route("/pin_generation1")
def pin_generation1():
    return render_template("pin_generation1.html")

@app.route("/pin_generation2",methods=["POST","GET"])
def pin_generation2():
    accno = request.form["accno"]

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query ="SELECT USER_PIN FROM ACCOUNTS WHERE USER_ACCNO = %s"
    cursor.execute(query,(accno))
    data = cursor.fetchone()
    conn.close()
    print(data)
    if data is None:
        return render_template("pin_generation1.html",msg="noaccnt")
    elif data[0] is not None:
        return render_template("pin_generation1.html",msg="Exist")
    else:
        return render_template("pin_generation2.html",accno=accno)
    
@app.route("/pin_generation3",methods=["POST","GET"])
def pin_generation3():
    accno = request.form["accno"]
    pin = request.form["pin"]
    cpin =request.form["cpin"]

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query ="SELECT USER_PIN FROM ACCOUNTS WHERE USER_ACCNO = %s"
    cursor.execute(query,(accno))
    data = cursor.fetchone()
    conn.close()
    print(data)
    if pin != cpin:
        return render_template("pin_generation2.html",msg="wrongpin")
    else:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query ="UPDATE ACCOUNTS SET USER_PIN = %s WHERE USER_ACCNO = %s"
        cursor.execute(query,(pin,accno))
        conn.commit()
        conn.close()
        return render_template("pin_generation2.html",msg="ok")
app.run(port=5004)