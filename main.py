from flask_login import LoginManager, login_manager
from flask import Flask, render_template, jsonify, request, url_for, redirect, flash
from flask_table import Table, columns
from flaskext.mysql import MySQL
from werkzeug.utils import secure_filename
import json
import os

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
UPLOAD_PATH = '/Users/Lenovo/PycharmProjects/HZdev/UPLOADS/Assignments'

app = Flask(__name__)
mysql = MySQL()
app.config['UPLOAD_FOLDER'] = UPLOAD_PATH
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'Project'
mysql.init_app(app)

app.secret_key = 'yeet'
conn = mysql.connect()
cursor = conn.cursor()

# User variables
_userFName = ""
_userLName = ""
_userEmail = ""
_userClass = ""

@app.route('/')
def main():
    return render_template('index.html')


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/testtables')
def showTableTest():
    return render_template('tabletests.html')

# pass all details to landing page to build screen correctly
@app.route('/tabletests2')
def showTableTest2():
    global _userFName
    global _userLName
    print("testing")
    print(_userLName)

# RETURN USER CLASS INFORMATION
    # CURRENTLY RETURNS DOUBLE THE DATA
    global _userClass
    cursor.execute("SELECT title FROM class JOIN classregister ON classregister.Class_classID JOIN user ON classregister.users_userID = user.userID WHERE user.email = '" + _userEmail + "'ORDER BY class.title;")
    _userClass = cursor.fetchall()
    _userClass = (str(_userClass).replace('(', "").replace("'", "").replace(",", "").replace(")", ""))
    print(_userClass)



    return render_template('tabletests2.html', _userFName = _userFName, _userLName = _userLName, _userEmail= _userEmail, _userClass= _userClass)



@app.route('/modaltest')
def showModalTest():
    return render_template('modaltest.html')


# USER SIGNUP#
@app.route('/signup', methods=['POST', 'GET'])
def signUp():
    # read the posted values from the UI

    _fname = request.form['fname']
    _lname = request.form['lname']
    _email = request.form['email']
    _password = request.form['password']
    _parentview = request.form['yes_no']
    if _parentview == 'on':
        _parentview = 1
    else:
        _parentview = 0
    print(_fname)
    print(_lname)
    cursor.callproc('createUser', (_fname, _lname, _password, _email, _parentview))
    data = cursor.fetchall()
    print(data)
    conn.commit()
    return redirect('/login', code=302)


# ADD NEW ASSIGNMENT#
@app.route('/addAssign', methods=['POST', 'GET'])
def addAssign():
    # read the posted values from the UI (modal script)
    _assessTitle = request.form['assessTitle']
    print(_assessTitle)
    _taskDetail = request.form['taskDetail']
    print(_taskDetail)
    _dueDate = request.form['dueDate']
    print(_assessTitle)
    print(_taskDetail)
    _classID = request.form['classID']
    print(_classID)
    cursor.callproc('addAssign', (_assessTitle, _taskDetail, _dueDate, _classID))
    data = cursor.fetchall()
    print(data)
    conn.commit()
    return redirect('/tabletests2', code=302)


def allowed_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ADD NEW SUBMISSION#
@app.route('/addSub', methods=['POST', 'GET'])
def addSub():
    if 'inputfile' not in request.files:
        print("failed")
    else:
        print("Success")
        inputFile = request.files['inputfile']
        if inputFile.filename == '':
            flash("no file selected")
            return (redirect('tableTests2'))
        if inputFile and allowed_files(inputFile.filename):
            filename = secure_filename(inputFile.filename)
            inputFile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            _inputFileName = filename
            _inputFilePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(_inputFileName)
            print(_inputFilePath)
            # read the posted values from the UI (modal script)
            _date = request.form['date']
            print(_date)

            _finalMark = request.form['finalMark']
            print(_finalMark)

            _teachComment = request.form['teachComment']
            print(_teachComment)

            _assignmentID = request.form['assignID']
            print(_assignmentID)

            _userID = request.form['userID']
            print(_userID)

            cursor.callproc('addSubmission',
                            (_date, _inputFileName, _inputFilePath, _finalMark, _teachComment, _assignmentID, _userID))
            data = cursor.fetchall()
            print(data)
            conn.commit()

        return render_template('testing.html')


# USER SIGN IN#
# @bull.route("/loginV3", methods=["GET", "POST"])
# def login():
#   """For GET requests, display the login form.
#  For POSTS, login the current user by processing the form.
# """
# form = LoginForm()
# if form.validate_on_submit():
#   user = User.query.get(form.email.data)
#  if user:
#     if bcrypt.check_password_hash(user.password, form.password.data):
#        user.authenticated = True
#       db.session.add(user)
#      db.session.commit()
#     login_user(user, remember=True)
#    return redirect(url_for("bull.reports"))
# return render_template("loginV3.html", form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if "login" in request.form:
        return render_template('loginV3.html')
    elif "signup" in request.form:
        return render_template('signup.html')
    return render_template('loginV3.html')


# Pull data from database
@app.route('/students', methods=['GET'])
def get_student():
    cursor.execute("SELECT * from user where email = 'technowhiz1@gmail.com' ")
    result_set = cursor.fetchall()
    for row in result_set:
        print(row["fname"], row["lname"])
    return render_template('tabletests2.html', fName=fName)


# Login to HZ
@app.route('/userLogin', methods=['GET', 'POST'])
def detail_check():
# Retrieve details from login screen
    _inputEmail = request.form['username']
    _inputpass = request.form['password']
    print(_inputEmail)
    print(_inputpass)
    if _inputpass == "" or _inputEmail == "":
        error = 'Invalid credentials, please try again'
        return render_template('loginV3.html', error=error)
# Pull correct user password from DB based on inputted email address
    cursor.execute("SELECT password from user where email ='" + _inputEmail + "';")
    _verifiypass = cursor.fetchall()
    _verifiypass = (str(_verifiypass).replace('(', "").replace("'", "").replace(",", "").replace(")", ""))
    print(_verifiypass)

# INCOMPLETE
#Pull User's Name
#could use storedproc?
    cursor.execute("SELECT fname from user where email ='" + _inputEmail + "';")
    global _userFName
    _userFName = cursor.fetchall()
    _userFName = (str(_userFName).replace('(',"").replace("'","").replace(",","").replace(")",""))
    print(_userFName)

    cursor.execute("SELECT lname from user where email ='" + _inputEmail + "';")
    global _userLName
    _userLName = cursor.fetchall()
    _userLName = (str(_userLName).replace('(',"").replace("'","").replace(",","").replace(")",""))
    print(_userLName)

    cursor.execute("SELECT email from user where email ='" + _inputEmail + "';")
    global _userEmail
    _userEmail = cursor.fetchall()
    _userEmail = (str(_userEmail).replace('(',"").replace("'","").replace(",","").replace(")",""))
    print(_userEmail)

# DETERMINE IF PASSWORD MATCHES PASSWORD STORED IN DATABASE
    if _inputpass == _verifiypass:
        return showTableTest2()
    elif _inputpass == '':
        return render_template('loginV3.html', error=error)
    elif _inputEmail != _verifiypass:
        return render_template('loginV3.html')

#def return_user_details():


#def manageclasses():










if __name__ == "__main__":
    app.run(debug=True)
