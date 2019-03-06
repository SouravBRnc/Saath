from flask import Flask, render_template, request, redirect,url_for,session
import mysql.connector
import os

app = Flask(__name__)

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "",
    database = "SAATH"
)

mycursor = mydb.cursor()

app.secret_key = os.urandom(24)

@app.route('/')
def home_page():
    return render_template("login_signup_page.html")

@app.route('/donsignup', methods= ['POST', 'GET'])
def don_signup():
    if request.method == 'POST':
        user = request.form
        #username = user.get("username")
        uemail = user.get("don_email2")
        upassword = user.get("don_password2")
        add = user.get("address")
        contact = user.get("contact")
        #age = int(user.get("user_age"))
        #gender = user.get("user_gender")
        sql = "INSERT INTO donators(email, password, address, contact) VALUES (%s, %s, %s, %s)"
        val = (uemail, upassword, add, contact)
        mycursor.execute(sql, val)
        mydb.commit()
        sql = "INSERT INTO mob_don(id,address,url) VALUES (%s, %s, %s)"
        val = ("0", add, "0")
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template("login_signup_page.html")

@app.route('/mobsignup', methods= ['POST', 'GET'])
def mob_signup():
    if request.method == 'POST':
        user = request.form
        #username = user.get("username")
        uemail = user.get("mob_email2")
        upassword = user.get("mob_password2")
        contact = user.get("contact")
        #age = int(user.get("user_age"))
        #gender = user.get("user_gender")
        sql = "INSERT INTO mobile(email, password, contact) VALUES (%s, %s, %s)"
        val = (uemail, upassword, contact)
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template("login_signup_page.html")


@app.route('/ngosignup', methods= ['POST', 'GET'])
def ngo_signup():
    if request.method == 'POST':
        user = request.form
        uemail = user.get("ngo_email2")
        upassword = user.get("ngo_password2")
        add = user.get("address")
        contact = user.get("contact")
        # age = int(user.get("user_age"))
        # gender = user.get("user_gender")
        sql = "INSERT INTO ngo(email, password, address, contact) VALUES (%s, %s, %s, %s)"
        val = (uemail, upassword, add, contact)
        mycursor.execute(sql, val)
        mydb.commit()
        sql = "INSERT INTO mob_ngo(id,address,url) VALUES (%s, %s, %s)"
        val = ("0", add, "0")
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template("login_signup_page.html")


@app.route('/donlogin', methods= ['POST', 'GET'])
def don_login():
    if request.method == 'POST':
        result = request.form
        uemail = result.get("don_email1")
        upass = result.get("don_password1")
        sql = "SELECT * FROM donators WHERE email= %s and password= %s;"
        mycursor.execute(sql, (uemail, upass))
        res = mycursor.fetchone()
        if res :
            session['user']=uemail
            sql = "select address from donators where email=%s;"
            mycursor.execute(sql, (uemail, ))
            res1 = mycursor.fetchone()
            return render_template("don_dashboard.html", result=uemail, address = res1)
            #flash('Logged in Succesfully..!')

        else:
            return render_template("login_signup_page.html")
            #flash('Invalid Credentials.. Please try again..!!')

@app.route('/moblogin', methods= ['POST', 'GET'])
def mob_login():
    if request.method == 'POST':
        result = request.form
        uemail = result.get("mob_email1")
        upass = result.get("mob_password1")
        sql = "SELECT * FROM mobile WHERE email= %s and password= %s;"
        mycursor.execute(sql, (uemail, upass))
        res = mycursor.fetchone()
        if res :
            # sql = "SELECT username FROM user WHERE email= %s;"
            # mycursor.execute(sql, (uemail,))
            # res = mycursor.fetchall()
            session['user']= uemail
            return render_template("mob_dashboard.html", result = session['user'])
            #flash('Logged in Succesfully..!')

        else:
            return render_template("login_signup_page.html")
            #flash('Invalid Credentials.. Please try again..!!')

@app.route('/ngologin', methods= ['POST', 'GET'])
def ngo_login():
    if request.method == 'POST':
        result = request.form
        uemail = result.get("ngo_email1")
        upass = result.get("ngo_password1")
        sql = "SELECT * FROM ngo WHERE email= %s and password= %s;"
        mycursor.execute(sql, (uemail, upass))
        res = mycursor.fetchone()
        if res :
            # sql = "SELECT username FROM user WHERE email= %s;"
            # mycursor.execute(sql, (uemail,))
            # res = mycursor.fetchall()
            session['user']= uemail
            return render_template("ngo_dashboard.html", result = uemail)
            #flash('Logged in Succesfully..!')

        else:
            return render_template("login_signup_page.html")
            #flash('Invalid Credentials.. Please try again..!!')






@app.route('/chat', methods = ['POST','GET'])
def chat():
    if 'user' in session:
        return render_template("chat.html", result = session['user'])
    else:
        return render_template("login_signup_page.html")



# @app.route('/confirm_pick', methods = ['POST', 'GET'])
# def confirm_pick():
#     if 'user' in session:
#         return render_template("confirm_pick.html", result = result)


@app.route('/tologin')
def tologin():
    session.pop('user', None)
    return render_template("after_logout.html")


# @app.route('/map', methods = ['POST', 'GET'])
# def map():
#     result = request.form
#     return render_template("login_signup._page.html")



@app.route('/mob_find_don')
def mob_find_don():
    if 'user' in session:
        query="select * from mob_don;"
        mycursor.execute(query)
        res=mycursor.fetchall()
        print(res)
        #return render_template('mul_map_loc.html',data = res)
        return render_template('map_for_rider.html',data = res)
    else:
        return render_template('login_signup_page.html')




@app.route('/mob_find_ngo')
def mob_find_ngo():
    if 'user' in session:
        query="select * from mob_ngo;"
        mycursor.execute(query)
        res=mycursor.fetchall()
        #return render_template('mul_map_loc.html',data = res)
        return render_template('map_for_rider.html',data = res)
    else:
        return render_template('login_signup_page.html')


@app.route('/contact')
def contact():
    if 'user' in session:
        return render_template('contact_us.html')
    else:
        return render_template('login_signup_page.html')


@app.route('/locate_don', methods=['POST','GET'])
def loc_don():
    if request.method == 'POST':
        if 'user' in session:
            x = request.form

            address = x.get("address")

            data={
                'id': 0,
                'address': address[:],
                'url': 0
            }
            lis = []
            for key in data:
                temp = [key, data[key]]
                lis.append(temp)

            return render_template("map_for_rider.html", data = lis)
        else:
            return render_template("login_signup_page.html")

# @app.route('/transactions', methods=['POST','GET'])
# def trans_comp():
#     if 'user' in session:
#         x= request.form
#         demail= x.get("don_email")
#         nemail=x.get("ngo_email")
#         sql = "INSERT INTO transaction(donator, ngo) values(%s, %s);"
#         mycursor.execute(sql,(demail, nemail))
#         mydb.commit()
#         return render_template("ngo_dashboard.html")
#     else:
#         return render_template("login_signup_page.html")
#


@app.route('/review', methods=['POST','GET'])
def review():
    if 'user' in session:
        return render_template("review.html")
    else:
        return render_template("login_signup_page.html")


@app.route('/my_contrib', methods=['POST','GET'])
def my_contrib():
    return render_template("my_contrib.html")





# @app.route('/don_donate', methods = ['POST','GET'])
# def don_donate():
#     if 'user' in session:
#         return render_template("don_donate.html")
#     else:
#         return render_template("login_signup_page.html")

# @app.route('/donate', methods = ['POST', 'GET'])
# def donate():
#     if 'user' in session:
#         result = request.form
#         type = result.get("")
#

# @app.route('/chat', methods=['POST','GET'])
# def reviews():
#     if 'user' in session:
#         if request.method == 'POST':
#             input = request.form
#             uemail = session['user']
#             umsg = input.get("input_val")
#             sql = "INSERT INTO chat(email, msg) VALUES(%s, %s);"
#             mycursor.execute(sql, (uemail, umsg))
#             mydb.commit()
#             sql = "SELECT email, msg FROM chat;"
#             mycursor.execute(sql)
#             result = mycursor.fetchall()
#             return render_template("chat.html", result= result)
#     else:
#         return render_template("login_signup.html")

# @app.route('/load_chat', methods=['POST', 'GET'])
# def load_chat():
#     if user in session:
#         if request.method == 'GET':
#             last_chat_id = request.form.get("last_chat_id")
#             sql = "SELECT * FROM chat WHERE cid>%s;"
#             mycursor.execute(sql, (last_chat_id, ))
#             result = mycursor.fetchall()
#
#

# @app.route('/send_msg')
# def send_msg():
#     if user in session:
#
#         return render_template("reviews.html")
#     else:
#         return render_template("login_signup.html")
#


if __name__ == '__main__':
    my_ip='192.168.43.198'
    app.run(host=my_ip, port='8000', debug=True)
