from flask_login import LoginManager, login_manager
from flask import Flask, render_template, jsonify, request, url_for, redirect, flash
from flask_table import Table, columns
from flaskext.mysql import MySQL
from werkzeug.utils import secure_filename
import json
import os

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
UPLOAD_PATH_ASSIGN = '/Users/Lenovo/PycharmProjects/HZdev/UPLOADS/Assignments'
UPLOAD_PATH_SUBMISSION = '/Users/Lenovo/PycharmProjects/HZdev/UPLOADS/Submissions'

app = Flask(__name__)
mysql = MySQL()
app.config['UPLOAD_FOLDER_ASSIGN'] = UPLOAD_PATH_ASSIGN
app.config['UPLOAD_FOLDER_SUBMISSION'] = UPLOAD_PATH_SUBMISSION


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
_nextAssDue = ""
_nextAssDueDate = ""
_nextAssDueSub = ""
_nextAssDueDetail = ""
_memberID = ""
_avgMark = ""
_weakMark = ""
_weakMarkSub = ""
_strongMark = ""
_strongMarkSub = ""
_userID = ""
_totalComplete = ""





@app.route('/')
def main():
    return render_template('index.html')


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/testtables')
def showTableTest():
    return render_template('tabletests.html')

# pass all details to landing page to build screen correctly STUDENTS ONLY
@app.route('/tabletests2')
def showTableTest2():
    global _userFName
    global _userLName
    print("testing")
    print(_userLName)

# RETURN USER CLASS INFORMATION
    global _userClass
    # COUNT N.O OF CLASSES
    cursor.execute("SELECT COUNT(*) FROM class JOIN classregister ON classregister.Class_classID JOIN user ON classregister.users_userID = user.userID WHERE user.email = '" + _userEmail + "'ORDER BY class.title;")
    _userClassNo = cursor.fetchall()
    _userClassNo =(int((_userClassNo[0][0])*.5))
    print(_userClassNo)
    cursor.execute("SELECT title FROM class JOIN classregister ON classregister.Class_classID JOIN user ON classregister.users_userID = user.userID WHERE user.email = '" + _userEmail + "'ORDER BY class.title;")
    _userClass = cursor.fetchall()
    # Return row 1 and 2 in unison
    _userClass = (_userClass[1]) + (_userClass[2])
    _userClass = (str(_userClass).replace('(', "").replace("'", "").replace(",", "").replace(")", ""))
    print(_userClass)

########################################
# THIS DOESN'T WORK JUST YET
    printedclasses = 0
    while printedclasses <0:
        print(_userClassNo[printedclasses])
        _userClass = _userClass[0]
        printedclasses = printedclasses + 1
        print("CLASSES ATTENDED")
        printedclasses = (str(printedclasses).replace('(', "").replace("'", "").replace(",", "").replace(")", ""))
        print(printedclasses)
########################################

# RETURN NEXT ASSIGNMENT DUE DETAILS

    # MAYBE USE LOOPS TO COUNT NUMBER OF ELEMENTS TO ADD?
    global _nextAssDue
    cursor.execute("SELECT class.title, assTitle, dueDate, taskdetails FROM assignment JOIN class ON assignment.class_classID = class.classID JOIN classregister ON classregister.Class_classID = class.classID JOIN user ON classregister.users_userID = user.userID WHERE user.email = '" + _userEmail + "'ORDER BY assignment.dueDate DESC LIMIT 1;")
    _nextAssDue = cursor.fetchall()
    _nextAssDueDate = (_nextAssDue[0][2])
    _nextAssDueDetail = (_nextAssDue[0][1])
    _nextAssDueSub = (_nextAssDue[0][0])
    _nextAssDueTask = (_nextAssDue[0][3])
    print(_nextAssDue)



   # cursor.execute("INSERT INTO classregister(users_userID, class_classID) values(2,2);")
   # conn.commit()

    # Pass variables to main page
    return render_template('tabletests2.html', _userFName = _userFName, _userLName = _userLName, _userEmail= _userEmail, _userClass= _userClass, _nextAssDueDate = _nextAssDueDate, _nextAssDueSub = _nextAssDueSub, _nextAssDueDetail = _nextAssDueDetail, _nextAssDueTask = _nextAssDueTask, _avgMark = _avgMark, _weakMarkSub = _weakMarkSub, _weakMark = _weakMark, _strongMarkSub=_strongMarkSub, _strongMark = _strongMark)



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




# ADD NEW ASSIGNMENT# NOT YET COMPLETE
@app.route('/addAssignment', methods=['POST', 'GET'])
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
            inputFile.save(os.path.join(app.config['UPLOAD_FOLDER_SUBMISSION'], filename))
            _inputFileName = filename
            _inputFilePath = os.path.join(app.config['UPLOAD_FOLDER_SUBMISSION'], filename)
            print(_inputFileName)
            print(_inputFilePath)

            # read the posted values from the UI (modal script)
            _assTitle = request.form['assTitle']
            print(_assTitle)

            _dueDate = request.form['date']
            print(_dueDate)

            _taskdetails = request.form['taskDetails']
            print(_taskdetails)

            _classID = request.form['classID']
            print(_classID)

            cursor.callproc('addAssign2', (_assTitle, _taskdetails, _dueDate, _inputFileName, _inputFilePath, _classID))
            data = cursor.fetchall()
            print(data)
            conn.commit()

        return render_template('/tabletests2')




# ADDING NEW ASSIGNMENT WITH FILE UPLOAD IN PROGRESSSSSSSSSSS
@app.route('/addSub', methods=['POST', 'GET'])
def addAssign2():
   # if 'inputfile' not in request.files:
    #    print("failed")
    #else:
     #   print("Success")
        inputFile = request.files['inputfile']
      #  if inputFile.filename == '':
       #     flash("no file selected")
        #    return (redirect('tableTests2'))
        if inputFile and allowed_files(inputFile.filename):
            filename = secure_filename(inputFile.filename)
            inputFile.save(os.path.join(app.config['UPLOAD_FOLDER_ASSIGN'], filename))
            _inputFileName = filename
            _inputFilePath = os.path.join(app.config['UPLOAD_FOLDER_ASSIGN'], filename)
            print(_inputFileName)
            print(_inputFilePath)

            # read the posted values from the UI (modal script)
            _assTitle = request.form['assTitle']
            print(_assTitle)

            _dueDate = request.form['date']
            print(_dueDate)

            _taskdetails = request.form['taskDetails']
            print(_taskdetails)

            _classID = request.form['classID']
            print(_classID)

# DETERMINE CLASS ID
            # CONTINUE WORK TO ALLOW FOR CLASS NAME INPUT RATHER THAN CLASSID INPUT

            cursor.execute(
                "SELECT class.title FROM class WHERE classID ='" + _classID + "';  ;")
            _classTitle = cursor.fetchall()
            _classTitle = (str(_classTitle).replace('(', "").replace("'", "").replace(",", "").replace(")", ""))
            print(_classTitle)
            cursor.callproc('addAssign2',
                            (_assTitle, _taskdetails, _dueDate, _inputFileName, _inputFilePath, _classID))
            data = cursor.fetchall()
            print(data)
            conn.commit()

            return redirect('tabletests2', code=302)



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
    cursor.execute("SELECT fname, lname, email, memberID, userID from user where email ='" + _inputEmail + "';")
    global _userFName
    global _userLName
    global _userEmail
    global _userID
    global _memberID
    global _avgMark
    global _weakMark
    global _weakMarkSub
    global _strongMark
    global _strongMarkSub
    global _totalComplete



    _userDetails = cursor.fetchall()
    print(_userDetails)
    _userFName = (_userDetails[0][0])
    _userLName = (_userDetails[0][1])
    _userEmail = (_userDetails[0][2])
    _memberID = (_userDetails[0][3])
    _userID = (_userDetails[0][4])
    #_userFName = (str(_userFName).replace('(',"").replace("'","").replace(",","").replace(")",""))
    print(_userFName)
    # cursor.execute("SELECT lname from user where email ='" + _inputEmail + "';")
    #_userLName = cursor.fetchall()
    #_userLName = (str(_userLName).replace('(',"").replace("'","").replace(",","").replace(")",""))
    print(_userLName)
    #cursor.execute("SELECT email from user where email ='" + _inputEmail + "';")
    #global _userEmail
    #_userEmail = cursor.fetchall()
    #_userEmail = (str(_userEmail).replace('(',"").replace("'","").replace(",","").replace(")",""))
    print(_userEmail)

#Determine user type:
# RETURN DIFFERENT RENDER TEMPLATE BASED ON OUTCOME OF THIS ROUTINE
    if _memberID == 1:
       _userType = 'student'
    elif _memberID ==2:
        _userType ='teacher'
    elif _memberID ==3:
        _userType = 'parent'

# DETERMINE IF PASSWORD MATCHES PASSWORD STORED IN DATABASE
    if _inputpass == _verifiypass:
        return showTableTest2()
    elif _inputpass == '':
        return render_template('loginV3.html', error=error)
    elif _inputEmail != _verifiypass:
        return render_template('loginV3.html')

#DETERMINE AVERAGE MARKS
    cursor.execute("SELECT AVG(finalmark) FROM SUBMISSION JOIN user on submission.user_userID = user.userID WHERE user.email='" + _inputEmail + "';")
    _avgMark = cursor.fetchall()
    print(_avgMark)
#DETERMIN NUM OF COMPLETED ASSIGNMENTS WIHTIN PAST 9 MONTHS
    cursor.execute("SELECT COUNT(*) FROM submission WHERE user_userID ='" + _userID + "' AND finalmark <>'' AND submission.date > DATE_SUB(now(), INTERVAL 9 MONTH);")
    _totalComplete = cursor.fetchall()
    print(_totalComplete)

    #DETERMINE STRONGEST SUBJECT MARKS
    cursor.execute("SELECT MAX(finalmark), class.title FROM submission JOIN assignment on submission.assignment_assID = assignment.assID JOIN class on assignment.class_classID = class.classID JOIN user on submission.user_userID = user.userID WHERE user.email='" + _inputEmail + "';")
    _strongMark = cursor.fetchall()
    _strongMarkSub = (_strongMark[0][1])
    _strongMark = (_strongMark[0][0])

    #DETERMINE WEAKEST SUBJECT
    cursor.execute("SELECT MIN(finalmark), class.title FROM submission JOIN assignment on submission.assignment_assID = assignment.assID JOIN class on assignment.class_classID = class.classID JOIN user on submission.user_userID = user.userID WHERE user.email='" + _inputEmail + "';")
    _weakMark = cursor.fetchall()
    _weakMarkSub = (_weakMark[0][1])
    _weakMark = (_weakMark[0][0])

# Find list of all assignments without a mark assigned (INCOMPLETE SUBMISSIONS)
    cursor.execute("SELECT inputFileName, inputFilePath, finalmark, teachcomment, assignment_assID, user_userID FROM submission WHERE user_userID ='" + _userID + "' AND finalmark ='';")
    _assignsDue = cursor.fetchall()
    print(_assignsDue)

# Find list of all assignments with a mark assigned (COMPLETED SUBMISSIONS)
    cursor.execute("SELECT inputFileName, inputFilePath, finalmark, teachcomment, assignment_assID, user_userID FROM submission WHERE user_userID ='" + _userID + "' AND finalmark <>'';")
    _assignsComplete = cursor.fetchall()
    print(_assignsComplete)


# ADD Students to class(es)
#def return_user_details():
@app.route('/classManagement', methods=['GET', 'POST'])
def manageclasses(): # WORKS
    # GET DATA FROM FORMS
    _userID = request.form['userID']
    _classID = request.form['classID']
    # GET STUDENT DATE FROM FORMS
    cursor.execute("INSERT INTO classregister(users_userID, class_classID) values('" + (str(_userID)) + "','" + str((_classID)) + "');")
    conn.commit()
    return render_template('tabletests2.html')

#REMOVE students from classes
@app.route('/classManageRemove', methods=['GET', 'POST'])
def manageClassRemove(): # WORKS
    # GET DATA FROM FORMS
    _userID = request.form['userID']
    _classID = request.form['classID']
    # GET STUDENT DATE FROM FORMS
    cursor.execute("DELETE FROM classregister WHERE users_userID =('" + (str(_userID)) + "') AND class_classID = ('" + str((_classID)) + "');")
    conn.commit()
    return render_template('tabletests2.html')

#REMOVE students from classes VIA STUDENT NAME
@app.route('/classManageRemoveName', methods=['GET', 'POST'])
def manageClassRemoveName(): # WORKS
    # GET DATA FROM FORMS
    _userID = request.form['userID']
    _classID = request.form['classID']
    _stuFname = request.form['stuFname']
    _stuLname = request.form['stuLname']
    # GET STUDENT DATE FROM FORMS
    cursor.execute("DELETE FROM classregister WHERE users_userID =('" + (str(_userID)) + "') AND class_classID = ('" + str((_classID)) + "');")
    cursor.execute("DELETE classregister FROM classregister JOIN user ON classregister.users_userID = user.userID WHERE user.fname=('" + _stuFname + "' ) AND user.lname =('" + _stuLname + "') AND classregister.class_classID = ('" + str((_classID)) + "');")
    conn.commit()
    return render_template('tabletests2.html')


# TEACHERS VARIABLE SETTING
# def teachervar():



if __name__ == "__main__":
    app.run(debug=True)
