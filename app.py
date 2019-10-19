from flask import Flask,render_template,jsonify, redirect,request,g,session,flash,url_for
import urllib.request,json
import ssl
import os
import sqlite3
import re
import time
import threading
from flask_mail import Mail, Message
os.environ['FLASK_APP'] = 'tshirt'
ssl._create_default_https_context = ssl._create_unverified_context
app = Flask(__name__)

app.config.update(
    DEBUG=True,
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'stn131415@gmail.com',
	MAIL_PASSWORD = 'sfanbthbieupcxll'
)

mail = Mail(app)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path,'user.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('closet_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """

    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def add_uesrdetail(weight,age,gender,email,firstName,lastName,address1,postcode,city,phone):
    auth_user = session.get("username")
    db=get_db()
    db.execute("insert into user_inf(username,gender,weight,age,email,firstName,lastName,address1,postcode,city,phone) values (?,?,?,?,?,?,?,?,?,?,?)", [auth_user, gender,weight,age,email,firstName,lastName,address1,postcode,city,phone])
    db.commit()

def get_inf(user):
    db = get_db()
    cur = db.execute("select *  from user_inf where username =?", [user])
    rows = cur.fetchone()
    return rows



@app.route('/')
def index():
    return render_template('home.html')

@app.route('/realtime')
def realtime_chart():
    error='realtime page'
    return render_template('realtime.html',error=error)


@app.route('/get_spo/')
def get_spo():
    start_id = request.args.get('maxId', 0)
    start_date = request.args.get('Date[]',0)
    # 创建数据库对象
    baseurl = "https://api.thingspeak.com/channels/858372/fields/1.json?results=1"
    data_list = []
    date_list = []
    result = urllib.request.urlopen(baseurl)
    result = result.read().decode('utf-8')
    data = json.loads(result)
    for i in data["feeds"]:
        time_last_result = i['created_at']
        last_result = i['field1']
        # time_last_result=time.strftime("%H:%M:%S", time.localtime())
        timeArray = time.strptime(time_last_result, "%Y-%m-%dT%H:%M:%SZ")
        timeStamp = int(time.mktime(timeArray))
        timeArray = time.localtime(timeStamp)
        time_last_result = time.strftime("%H:%M:%S", timeArray)
        if start_id == 0 or start_date!=time_last_result:
            date_list.append(time_last_result)
            data_list.append(last_result)
            max_id = int(start_id) + 1
        else:
            max_id=int(start_id)
        json_str = json.dumps({'data': data_list, 'date': date_list, 'maxId': max_id}, ensure_ascii=False)
    # print(json_str)
    return json_str

@app.route('/get_temp/')
def get_temp():
    start_id = request.args.get('maxId', 0)
    start_date = request.args.get('Date[]', 0)
    baseurl = "https://api.thingspeak.com/channels/858372/fields/3.json?results=1"
    data_list = []
    date_list = []
    result = urllib.request.urlopen(baseurl)
    result = result.read().decode('utf-8')
    data = json.loads(result)
    for i in data["feeds"]:
        time_last_result = i['created_at']
        last_result = i['field3']
        timeArray = time.strptime(time_last_result, "%Y-%m-%dT%H:%M:%SZ")
        timeStamp = int(time.mktime(timeArray))
        timeArray = time.localtime(timeStamp)
        time_last_result = time.strftime("%H:%M:%S", timeArray)
        if start_id == 0 or start_date != time_last_result:
            date_list.append(time_last_result)
            data_list.append(last_result)
            max_id = int(start_id) + 1
        else:
            max_id = int(start_id)
        json_str = json.dumps({'data': data_list, 'date': date_list, 'maxId': max_id}, ensure_ascii=False)
    return json_str

@app.route('/get_bpm/')
def get_bpm():
    start_id = request.args.get('maxId', 0)
    start_date = request.args.get('Date[]', 0)
    baseurl = "https://api.thingspeak.com/channels/858372/fields/2.json?results=1"
    data_list = []
    date_list = []
    result = urllib.request.urlopen(baseurl)
    result = result.read().decode('utf-8')
    data = json.loads(result)
    for i in data["feeds"]:
        time_last_result = i['created_at']
        last_result = i['field2']
        timeArray = time.strptime(time_last_result, "%Y-%m-%dT%H:%M:%SZ")
        timeStamp = int(time.mktime(timeArray))
        timeArray = time.localtime(timeStamp)
        time_last_result = time.strftime("%H:%M:%S", timeArray)
        if start_id == 0 or start_date != time_last_result:
            date_list.append(time_last_result)
            data_list.append(last_result)
            max_id = int(start_id) + 1
        else:
            max_id = int(start_id)
        json_str = json.dumps({'data': data_list, 'date': date_list, 'maxId': max_id}, ensure_ascii=False)
    # print(json_str)
    return json_str

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = request.form['username']
        passw = request.form['password']
        if user and passw:
            db= get_db()
            cur = db.execute("select *  from users where username =? and password=?", [user, passw])
            rows = cur.fetchone()
            if rows:
                session['logged_in'] = True
                session['username'] = user
                cur = db.execute("select *  from user_inf where username =?", [user])
                error='Login Success!'
                rows = cur.fetchone()
                if rows:
                    return render_template('home.html', error=error)
                else:
                    return render_template('userdetail.html',error=error)
            else:
                cur2 = db.execute("select username  from users")
                rows2 = cur2.fetchone()
                if rows2:
                    error = 'Incorrect username or password'
                else:
                    error ='User not registered'

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    time.sleep(1)
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    users = [dict(username=row[0], password=row[1]) for row in get_db().execute('select username, password from users order by username desc').fetchall()]
    registeredmembers=[]
    for i in users:
        registeredmembers.append(i['username'])
    if request.method == 'POST':
        user = request.form['username']
        passw = request.form['password']

        cfm_passw = request.form['cfm_password']
        if user in registeredmembers:
            error = 'User already registered'
        elif passw != cfm_passw:
            error = 'Passwords do not match'
        elif len(passw) < 8:
            error = 'Invalid password. Passwords must contain at least 8 characters, and at least one capital letter and number'
        elif not re.search("[0-9]", passw):
            error = 'Invalid password. Passwords must contain at least 8 characters, and at least one capital letter and number'
        elif not re.search("[A-Z]", passw):
            error = 'Invalid password. Passwords must contain at least 8 characters, and at least one capital letter and number'
        else:
            get_db().execute('insert into users (username, password) values (?, ?)', [user, passw])
            get_db().commit()
            error='You were successfully registered'
            return render_template('login.html',error=error)
    return render_template('register.html', error=error)

@app.route('/adduserdetail', methods=['GET', 'POST'])
def add_watchlist():
    if request.method == 'POST':
            gender=request.form['gender']
            weight = request.form['weight']
            age = request.form['age']
            email = request.form['email']
            firstName = request.form['firstName']
            lastName = request.form['lastName']
            address1 = request.form['address1']
            postcode = request.form['postcode']
            city = request.form['city']
            phone = request.form['phone']
            add_uesrdetail(weight,age,gender, email, firstName, lastName, address1, postcode, city, phone)
            error='add user info Success!'
    return render_template('home.html',error=error)

@app.route("/updateProfile", methods=["GET", "POST"])
def updateProfile():
    auth_user = session.get("username")
    if request.method == 'POST':
        email = request.form['email']
        age=request.form['age']
        weight=request.form['weight']
        address1 = request.form['address1']
        postcode = request.form['postcode']
        city = request.form['city']
        phone = request.form['phone']
        with sqlite3.connect('user.db') as con:
                try:
                    cur = con.cursor()
                    cur.execute('UPDATE user_inf SET email = ?,age=?,weight=?, address1 = ?, postcode = ?, city = ?, phone = ? WHERE username= ?', (email,age, weight, address1, postcode, city, phone,auth_user))
                    con.commit()
                except:
                    con.rollback()
        con.commit()
        con.close()
        error='update success'
        return render_template("home.html",error=error)

@app.route("/editinfo")
def editinfo():
    with sqlite3.connect('user.db') as conn:
        auth_user = session.get("username")
        cur = conn.cursor()
        cur.execute("SELECT * FROM user_inf WHERE username = ?",[auth_user])
        profileData = cur.fetchone()
    conn.close()
    return render_template("veiw_update.html",profileData=profileData)

@app.route('/history')
def history_window():
    error='historydata page'
    return render_template('historydata.html',error=error)

@app.route('/get_history_spo/')
def get_history_spo():
    baseurl = "https://api.thingspeak.com/channels/858372/fields/1.json?results=20"
    data_list = []
    date_list = []
    result = urllib.request.urlopen(baseurl)
    result = result.read().decode('utf-8')
    data = json.loads(result)
    for i in data["feeds"]:
        time_last_result = i['created_at']
        last_result = i['field1']
        timeArray = time.strptime(time_last_result, "%Y-%m-%dT%H:%M:%SZ")
        timeStamp = int(time.mktime(timeArray))
        timeArray = time.localtime(timeStamp)
        time_last_result = time.strftime("%H:%M:%S", timeArray)
        date_list.append(time_last_result)
        data_list.append(last_result)
        json_str = json.dumps({'data': data_list, 'date': date_list}, ensure_ascii=False)
    return json_str


@app.route('/get_history_bpm/')
def get_history_bpm():
    baseurl = "https://api.thingspeak.com/channels/858372/fields/2.json?results=20"
    data_list = []
    date_list = []
    result = urllib.request.urlopen(baseurl)
    result = result.read().decode('utf-8')
    data = json.loads(result)
    for i in data["feeds"]:
        time_last_result = i['created_at']
        last_result = i['field2']
        timeArray = time.strptime(time_last_result, "%Y-%m-%dT%H:%M:%SZ")
        timeStamp = int(time.mktime(timeArray))
        timeArray = time.localtime(timeStamp)
        time_last_result = time.strftime("%H:%M:%S", timeArray)
        date_list.append(time_last_result)
        data_list.append(last_result)
        json_str = json.dumps({'data': data_list, 'date': date_list}, ensure_ascii=False)
    return json_str

@app.route('/get_history_temp/')
def get_history_temp():
    baseurl = "https://api.thingspeak.com/channels/858372/fields/3.json?results=20"
    data_list = []
    date_list = []
    result = urllib.request.urlopen(baseurl)
    result = result.read().decode('utf-8')
    data = json.loads(result)
    for i in data["feeds"]:
        time_last_result = i['created_at']
        last_result = i['field3']
        timeArray = time.strptime(time_last_result,"%Y-%m-%dT%H:%M:%SZ")
        timeStamp = int(time.mktime(timeArray))
        timeArray = time.localtime(timeStamp)
        time_last_result = time.strftime("%H:%M:%S", timeArray)
        date_list.append(time_last_result)
        data_list.append(last_result)
        json_str = json.dumps({'data': data_list, 'date': date_list}, ensure_ascii=False)
    return json_str

@app.route('/feedbacks', methods=['GET', 'POST'])
def feedbacks_fun():
    error=None
    if request.method == 'POST':
        Contact = request.form.get('Contact')
        Subject = request.form.get('Subject')
        mesaage = request.form['mesaage']
        auth_user = session.get("username")
        inf=get_inf(auth_user)
        if Subject=='General Question':
            if Contact=='Email':
                obj=inf['email']+' '+inf['firstName']+' '+inf['lastName']+" General Question"

            else:
                obj=inf['phone']+' '+inf['firstName']+' '+inf['firstName']+" General Question"
            msg = Message(obj, sender='stn131415@gmail.com', recipients=['stn131415@gmail.com'])
            msg.body = mesaage
            mail.send(msg)
            body='Thanks for your support, we will address the issue as soon as possible'
        else:
            body = 'Thanks for your support'
        msg = Message('Thanks for your support', sender='stn131415@gmail.com', recipients=[inf['email']])
        msg.body = body
        mail.send(msg)
        error='send feedback success'
    return render_template('feedback.html', error=error)


if __name__ == "__main__":
    app.run(app.run(debug=True, port=5000, host='0.0.0.0'))
