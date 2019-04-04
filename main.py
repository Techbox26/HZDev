from flask_login import LoginManager, login_manager
from flask import Flask, render_template, jsonify, request, url_for, redirect, flash
from flask_table import Table, columns
from flaskext.mysql import MySQL
from werkzeug.utils import secure_filename
import json
import os

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
#UPLOAD_PATH_ASSIGN = '/Users/Lenovo/PycharmProjects/HZdev/UPLOADS/Assignments'
#UPLOAD_PATH_SUBMISSION = '/Users/Lenovo/PycharmProjects/HZdev/UPLOADS/Submissions'
UPLOAD_PATH_ASSIGN = '/Users/Lenovo/PycharmProjects/HZdev/static/UPLOADS/Assignments'
UPLOAD_PATH_SUBMISSION = '/Users/Lenovo/PycharmProjects/HZdev/static/UPLOADS/Submissions'


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
_nextAssDueID = ""
_memberID = ""
_avgMark = ""
_weakMark = ""
_weakMarkSub = ""
_strongMark = ""
_strongMarkSub = ""
_userID = ""
_totalComplete = ""
_userType = ""
_graphClasses = ""
_class1 = ""
_class2 = ""
_class3 = ""
_class1Mark = ""
_class2Mark = ""
_class3Mark = ""
_ass1DueID =""
_ass2DueID =""
_ass3DueID =""

@app.route('/')
def main():
    return render_template('index.html')


@app.route('/showModalTest')
def showmodaltest():
    return render_template('modaltest.html', _userID=1)


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/testtables')
def showTableTest():
    return render_template('tabletests.html')


















# Navigate to teachers landing
@app.route('/showTeachTables')
def showteachtables():
    print('ENTERED TEACHER ACCOUNT')
#GET AVERAGE MARKS FOR ALL CLASSES (3 CLASSES)
    _class1Avg =""
    _class1Name =""
    _class2Avg =""
    _class2Name = ""
    _class3Avg =""
    _class3Name=""
    cursor.execute(
    "SELECT CAST(AVG(finalmark) AS DECIMAL(10,2))as FINAL, class.title FROM submission JOIN assignment ON submission.assignment_assID = assignment.assID JOIN class ON assignment.class_classID = class.classID GROUP BY class.title ORDER BY FINAL DESC;")
    _class = cursor.fetchall()
    _class1Avg = (_class[0][0])
    _class1Name = (_class[0][1])
    _class2Avg = (_class[1][0])
    _class2Name = (_class[1][1])
    _class3Avg = (_class[2][0])
    _class3Name = (_class[2][1])
    #Class specific stats - Find highest and lowest prefomers for each class
    #CLASS 1
    cursor.execute(
        "SELECT CAST(AVG(finalmark)AS DECIMAL(10,2))AS MARK, CONCAT(user.fname, '" + " " + "', user.lname)AS STUDENT FROM submission JOIN assignment on submission.assignment_assID = assignment.assID JOIN class on assignment.class_classID = class.classID JOIN user on submission.user_userID = user.userID WHERE class.title =('" + _class1Name + "' ) ORDER BY MARK DESC LIMIT 1;")
    _class1High = cursor.fetchall()
    _class1HighStu = (_class1High[0][1])
    _class1HighStuMark = (_class1High[0][0])
    print(_class1HighStu)
    cursor.execute("SELECT CAST(AVG(finalmark) AS DECIMAL(10, 2))AS MARK, CONCAT(user.fname, '" + " " + "'  , user.lname)AS STUDENT FROM submission JOIN assignment on submission.assignment_assID = assignment.assID JOIN class on assignment.class_classID = class.classID JOIN user on submission.user_userID = user.userID WHERE class.title =('" + _class1Name + "' ) ORDER BY MARK ASC LIMIT 1;")
    _class1Low = cursor.fetchall()
    _class1LowStu = (_class1Low[0][1])
    _class1LowStuMark = (_class1Low[0][0])
    print(_class1LowStu)
    # CLASS 2
    cursor.execute(
        "SELECT CAST(AVG(finalmark) AS DECIMAL(10, 2))AS MARK, CONCAT(user.fname, '" + " " + "'  , user.lname)AS STUDENT FROM submission JOIN assignment on submission.assignment_assID = assignment.assID JOIN class on assignment.class_classID = class.classID JOIN user on submission.user_userID = user.userID WHERE class.title =('" + _class2Name + "' ) ORDER BY MARK DESC LIMIT 1;")
    _class2High = cursor.fetchall()
    _class2HighStu = (_class2High[0][1])
    _class2HighStuMark = (_class2High[0][0])
    print(_class2HighStu)
    cursor.execute(
        "SELECT CAST(AVG(finalmark) AS DECIMAL(10, 2))AS MARK, CONCAT(user.fname, '" + " " + "'  , user.lname)AS STUDENT FROM submission JOIN assignment on submission.assignment_assID = assignment.assID JOIN class on assignment.class_classID = class.classID JOIN user on submission.user_userID = user.userID WHERE class.title =('" + _class2Name + "' ) ORDER BY MARK ASC LIMIT 1;")
    _class2Low = cursor.fetchall()
    _class2LowStu = (_class2Low[0][1])
    _class2LowStuMark = (_class2Low[0][0])
    print(_class1LowStu)
    # CLASS 3
    cursor.execute(
        "SELECT CAST(AVG(finalmark) AS DECIMAL(10, 2))AS MARK, CONCAT(user.fname, '" + " " + "'  , user.lname)AS STUDENT FROM submission JOIN assignment on submission.assignment_assID = assignment.assID JOIN class on assignment.class_classID = class.classID JOIN user on submission.user_userID = user.userID WHERE class.title =('" + _class3Name + "' ) ORDER BY MARK DESC LIMIT 1;")
    _class3High = cursor.fetchall()
    _class3HighStu = (_class3High[0][1])
    _class3HighStuMark = (_class3High[0][0])
    print(_class3HighStu)
    cursor.execute(
        "SELECT CAST(AVG(finalmark) AS DECIMAL(10, 2))AS MARK, CONCAT(user.fname, '" + " " + "'  , user.lname)AS STUDENT FROM submission JOIN assignment on submission.assignment_assID = assignment.assID JOIN class on assignment.class_classID = class.classID JOIN user on submission.user_userID = user.userID WHERE class.title =('" + _class3Name + "' ) ORDER BY MARK ASC LIMIT 1;")
    _class3Low = cursor.fetchall()
    _class3LowStu = (_class3Low[0][1])
    _class3LowStuMark = (_class3Low[0][0])
    print(_class3LowStu)
    print(_class1Name)
   # _class3HighStu
   # _class3HighStuMark
   # _class3LowStu
   # _class3LowStuMark


#SELECT ALL FROM SUBMISSIONS WHERE THERE ARE NO MARKS ASSIGNED
    cursor.execute("SELECT COUNT(*) FROM submission where finalmark is null;")
    _outstanding = cursor.fetchall()
    _outstanding = (_outstanding[0][0])

#SELECT NEXT ASSIGNMENT DUE
    cursor.execute("SELECT assignment.duedate, class.title FROM assignment JOIN class ON assignment.class_classID = class.classID WHERE duedate > CURDATE() ORDER BY duedate LIMIT 1;")
    _nextUp = cursor.fetchall()
    _nextUpDate =(_nextUp[0][0])
    _nextUpClass = (_nextUp[0][1])


    return render_template('teachtables.html',_nextUpClass=_nextUpClass,_nextUpDate=_nextUpDate,_outstanding=_outstanding, _class1LowStuMark=_class1LowStuMark, _class1LowStu=_class1LowStu, _class1HighStuMark=_class1HighStuMark, _class1HighStu=_class1HighStu, _class2LowStuMark=_class2LowStuMark, _class2LowStu=_class2LowStu, _class2HighStuMark=_class2HighStuMark, _class2HighStu=_class2HighStu,_class3LowStuMark=_class3LowStuMark, _class3LowStu=_class3LowStu, _class3HighStuMark=_class3HighStuMark, _class3HighStu=_class3HighStu,_class3Avg=_class3Avg, _class2Avg=_class2Avg, _class1Avg=_class1Avg, _class3Name=_class3Name, _class2Name=_class2Name, _class1Name=_class1Name, _userType=_userType, _userFName=_userFName, _userLName=_userLName, _userEmail=_userEmail)



















# pass all details to landing page to build screen correctly STUDENTS ONLY
@app.route('/tabletests2')
def showTableTest2():
    global _userFName
    global _userLName
    print("testing")
    print(_userLName)

    # RETURN USER CLASS INFORMATION
    global _userClass
    global _graphClasses
    # COUNT N.O OF CLASSES
    cursor.execute(
        "SELECT COUNT(*) FROM class JOIN classregister ON classregister.Class_classID JOIN user ON classregister.users_userID = user.userID WHERE user.email = '" + _userEmail + "'ORDER BY class.title;")
    _userClassNo = cursor.fetchall()
    _userClassNo = (int((_userClassNo[0][0]) * .5))
    print(_userClassNo)
    # cursor.execute("SELECT title FROM class JOIN classregister ON classregister.Class_classID JOIN user ON classregister.users_userID = user.userID WHERE user.userID = '" + _userEmail + "'ORDER BY class.title;")
    cursor.execute(
        "SELECT title, level FROM class JOIN classregister ON classregister.Class_classID JOIN user ON classregister.users_userID = user.userID WHERE user.userID = '" + str(
            _userID) + "' GROUP BY class.title;")
    _userClass = cursor.fetchall()
    print(_userClass)
    _graphClasses = _userClass
    # Return row 1 and 2 in unison
    _userClass = ((_userClass[0][0]) + " " + (_userClass[1][0]) + " " + (_userClass[2][0]))
    # _userClass = (str(_userClass).replace('(', "").replace("'", "").replace(",", "").replace(")", ""))
    print(_userClass)

    ########################################
    # THIS DOESN'T WORK JUST YET
    #  printedclasses = 0
    #  while printedclasses <0:
    #     print(_userClassNo[printedclasses])
    #     _userClass = _userClass[0]
    #     printedclasses = printedclasses + 1
    #    print("CLASSES ATTENDED")
    #    printedclasses = (str(printedclasses).replace('(', "").replace("'", "").replace(",", "").replace(")", ""))
    #    print(printedclasses)
    ########################################

    # RETURN NEXT ASSIGNMENT DUE DETAILS

    # MAYBE USE LOOPS TO COUNT NUMBER OF ELEMENTS TO ADD?
    global _nextAssDue
    global _nextAssDueID
    cursor.execute(
        "SELECT class.title, assTitle, dueDate, taskdetails, assignmentFileName, assID FROM assignment JOIN class ON assignment.class_classID = class.classID JOIN classregister ON classregister.Class_classID = class.classID JOIN user ON classregister.users_userID = user.userID WHERE user.email = '" + _userEmail + "' ORDER BY assignment.dueDate DESC LIMIT 1;")
    _nextAssDue = cursor.fetchall()
    _nextAssDueDate = (_nextAssDue[0][2])
    _nextAssDueDetail = (_nextAssDue[0][1])
    _nextAssDueSub = (_nextAssDue[0][0])
    _nextAssDueTask = (_nextAssDue[0][3])
    _nextAssDueFile = (_nextAssDue[0][4])
    _nextAssDueID = (_nextAssDue[0][5])
    print(_nextAssDue)

    # cursor.execute("INSERT INTO classregister(users_userID, class_classID) values(2,2);")
    # conn.commit()

    ########################################
    # POPULATE AND BUILD GRAPH DATA
    global _class1
    global _class2
    global _class3
    global _class1Mark
    global _class2Mark
    global _class3Mark
    global _ass1file
    global _ass2file
    global _ass3file
    global  _ass1DueID
    global _ass2DueID
    global _ass3DueID

    # Determine 3 class details and marks
    _class1 = (_graphClasses[0][0])
    _class2 = (_graphClasses[1][0])
    _class3 = (_graphClasses[2][0])
    print(_class1, _class2, _class3)

    # Determine class average grades for user to pass to graph
    # class1
    cursor.execute(
        "SELECT AVG(finalmark)FROM submission JOIN assignment ON submission.assignment_assID = assignment.assID JOIN class ON assignment.class_classID = class.classID WHERE user_userID ='" + str(
            _userID) + "' AND class.title = '" + _class1 + "';")
    _class1Mark = cursor.fetchall()
    _class1Mark = (_class1Mark[0][0])
    print("Your average mark for " + _class1 + " is" + str(_class1Mark))
    cursor.execute(
        "SELECT AVG(finalmark)FROM submission JOIN assignment ON submission.assignment_assID = assignment.assID JOIN class ON assignment.class_classID = class.classID WHERE user_userID ='" + str(
            _userID) + "' AND class.title = '" + _class2 + "';")
    _class2Mark = cursor.fetchall()
    _class2Mark = (_class2Mark[0][0])
    print("Your average mark for " + _class2 + " is" + str(_class2Mark))
    cursor.execute(
        "SELECT AVG(finalmark)FROM submission JOIN assignment ON submission.assignment_assID = assignment.assID JOIN class ON assignment.class_classID = class.classID WHERE user_userID ='" + str(
            _userID) + "' AND class.title = '" + _class3 + "';")
    _class3Mark = cursor.fetchall()
    _class3Mark = (_class3Mark[0][0])
    print("Your average mark for " + _class3 + " is" + str(_class3Mark))

    #######################################
    # VIEW DETAILS OF PAST ASSIGNMENTS AND ADD BUTTONS ETC
    # RUN SQL TO SELECT ALL DATA FOR PAST 3 ASSIGNMENTS

    # cursor.execute("SELECT ")
    #cursor.execute("SELECT * FROM user;")
    cursor.execute("SELECT assignment.assTitle, class.title, inputFileName, inputFilePath, finalmark, teachcomment, assignment_assID, user_userID FROM submission JOIN assignment on submission.assignment_assID = assignment.assID JOIN class on assignment.class_classID = class.classID WHERE user_userID ='" + str(_userID) + "' AND finalmark !='' ORDER BY assignment.dueDate DESC LIMIT 3 ;")
    record = cursor.fetchall()
    # Assignment 1

    _ass1name = (record[0][0])
    _ass1class = (record[0][1])
    _ass1mark = (record[0][4])
    _ass1Comm = (record[0][5])
    print(_ass1name)
    print(_ass1class)
    print(_ass1mark)
    # Assignment 2
    _ass2name = (record[1][0])
    _ass2class = (record[1][1])
    _ass2mark = (record[1][4])
    _ass2Comm = (record[1][5])
    print(_ass2name)
    print(_ass2class)
    print(_ass2mark)
    # Assignment 3
    _ass3name = (record[2][0])
    _ass3class = (record[2][1])
    _ass3mark = (record[2][4])
    _ass3Comm = (record[1][5])
    #print(_ass3name)
    #print(_ass3class)
    #print(_ass3mark)

    # FIND FILE DETAIL TO LINK FILES TO BUTTONS
    _ass1file = "EERD_v2.png"
    # _ass1file = (record[0][2])
    _ass2file = (record[1][2])
    _ass3file = (record[2][2])
    print("FILE NAMES")
    print(_ass1file)
    print(_ass2file)
    print(_ass3file)

    #######################################
    # VIEW DETAILS OF DUE ASSIGNMENTS AND ADD BUTTONS ETC
    # RUN SQL TO SELECT ALL DATA FOR 3 DUE ASSIGNMENTS
    # DUE ASSIGNMENTS - ONES THAT ARE INCOMPLETE
    # cursor.execute("SELECT ")
    #cursor.execute("SELECT * FROM user;")
    #cursor.execute("SELECT assignment.assTitle, class.title, inputFileName, inputFilePath, finalmark, teachcomment, assignment_assID, user_userID FROM submission JOIN assignment on submission.assignment_assID = assignment.assID JOIN class on assignment.class_classID = class.classID WHERE user_userID ='" + str(_userID) + "' AND finalmark !='' ORDER BY assignment.duedate DESC LIMIT 3 ;")
    cursor.execute("SELECT assignment.assTitle, class.title, class.classID, assignment.taskdetails,  assignment.assignmentFileName, inputFilePath, assignment_assID, user_userID, dueDate FROM assignment LEFT JOIN submission ON submission.assignment_assID = assignment.assID AND submission.user_userID = '" + str(_userID) + "' JOIN class ON assignment.class_classID = class.classID LEFT JOIN user ON user.userID = submission.user_userID WHERE submission.assignment_assID is null;")
    record = cursor.fetchall()
    print("DUE ASSIGNMENTS")
    print(record)


    # Assignment 1
    #_due1name = (record[0][0])
    #_due1class = (record[0][1])
    #_due1mark = (record[0][4])
    _ass1DueClass = (record[0][1])
    _ass1DueTitle = (record[0][0])
    _ass1DueDetail = (record[0][3])
    _ass1DueSub = (record[0][1])
    _ass1DueFile =(record[0][4])
    _ass1DueID = (record[0][6])
    _ass1DueDate = (record[0][8])
    print(_ass1DueClass)
    print(_ass1DueTitle)

    # Assignment 2
    #_due2name = (record[1][0])
    #_due2class = (record[1][1])
    #_due2mark = (record[1][4])
    _ass2DueClass = (record[1][1])
    _ass2DueTitle = (record[1][0])
    _ass2DueDetail = (record[1][3])
    _ass2DueSub = (record[1][1])
    _ass2DueFile = (record[1][4])
    _ass2DueID = (record[1][6])
    _ass2DueDate = (record[1][8])
    print(_ass2DueClass)
    print(_ass2DueTitle)


    # Assignment 3
    #_due3name = (record[2][0])
    #_due3class = (record[2][1])
    #_due3mark = (record[2][4])
    _ass3DueClass = (record[2][1])
    _ass3DueTitle = (record[2][0])
    _ass3DueDetail = (record[2][3])
    _ass3DueSub = (record[2][1])
    _ass3DueFile = (record[2][4])
    _ass3DueID = (record[2][6])
    _ass3DueDate = (record[2][8])
    print(_ass3DueClass)
    print(_ass3DueTitle)



    # DETERMINE SUBJECT STATS
    # DETERMINE STRONGEST SUBJECT MARKS
    cursor.execute(
        "SELECT MAX(finalmark), class.title FROM submission JOIN assignment on submission.assignment_assID = assignment.assID JOIN class on assignment.class_classID = class.classID JOIN user on submission.user_userID = user.userID WHERE user.userID='" + str(_userID) + "';")
    _strongMark = cursor.fetchall()
    _strongMarkSub = (_strongMark[0][1])
    _strongMark = (_strongMark[0][0])
    # DETERMINE AVERAGE MARKS
    cursor.execute(
        "SELECT CAST(AVG(finalmark) as int) FROM submission JOIN user on submission.user_userID = user.userID WHERE user.userID='" + str(_userID) + "';")
    _avgMark = cursor.fetchall()
    _avgMark = (_avgMark[0][0])
    print(_avgMark)
    # DETERMINE NUM OF COMPLETED ASSIGNMENTS WIHTIN PAST 9 MONTHS
    cursor.execute(
        "SELECT COUNT(*) FROM submission WHERE user_userID ='" + str(_userID) + "' AND submission.date > DATE_SUB(now(), INTERVAL 9 MONTH);")
    _totalComplete = cursor.fetchall()
    _totalComplete = (_totalComplete[0][0])
    print(_totalComplete)
    # DETERMINE STRONGEST SUBJECT MARKS
    cursor.execute(
        "SELECT finalmark, class.title FROM submission JOIN assignment on submission.assignment_assID = assignment.assID JOIN class on assignment.class_classID = class.classID JOIN user on submission.user_userID = user.userID WHERE user.userID='" + str(_userID) + "' ORDER BY finalmark DESC;")
    _strongMark = cursor.fetchall()
    _strongMarkSub = (_strongMark[0][1])
    print(_strongMarkSub)
    _strongMark = (_strongMark[0][0])
    # DETERMINE WEAKEST SUBJECT
    cursor.execute(
        "SELECT MIN(finalmark), class.title FROM submission JOIN assignment on submission.assignment_assID = assignment.assID JOIN class on assignment.class_classID = class.classID JOIN user on submission.user_userID = user.userID WHERE user.userID='" + str(_userID) + "';")
    _weakMark = cursor.fetchall()
    _weakMarkSub = (_weakMark[0][1])
    print(_weakMarkSub)
    print("WEAKEST MARK")
    _weakMark = (_weakMark[0][0])
    print(_weakMark)


    # Pass variables to main page
    # _due3name = _due3name, _due3class = _due3class, _due3mark = _due3mark, _due2name = _due2name, _due2class = _due2class, _due2mark = _due2mark, _due1name = _due1name, _due1class = _due1class, _due1mark = _due1mark,
    return render_template('tabletests2.html',_ass1Comm = _ass1Comm, _ass2Comm=_ass2Comm, _ass3Comm=_ass3Comm ,_ass1DueDate=_ass1DueDate,_ass2DueDate=_ass2DueDate,_ass3DueDate=_ass3DueDate, _ass3DueClass=_ass3DueClass, _ass3DueTitle=_ass3DueTitle, _ass3DueDetail=_ass3DueDetail, _ass3DueSub=_ass3DueSub, _ass3DueFile=_ass3DueFile, _ass2DueClass=_ass2DueClass, _ass2DueTitle=_ass2DueTitle, _ass2DueDetail=_ass2DueDetail, _ass2DueSub=_ass2DueSub, _ass2DueFile=_ass2DueFile, _ass1DueClass=_ass1DueClass, _ass1DueTitle=_ass1DueTitle, _ass1DueDetail=_ass1DueDetail, _ass1DueSub=_ass1DueSub, _ass1DueFile=_ass1DueFile,    _nextAssDueFile=_nextAssDueFile, _ass3file=_ass3file, _ass2file=_ass2file, _ass1file=_ass1file, _ass3mark=_ass3mark ,_ass3class =_ass3class ,_ass3name=_ass3name, _ass2mark=_ass2mark ,_ass2class =_ass2class ,_ass2name=_ass2name,_ass1mark=_ass1mark ,_ass1class =_ass1class ,_ass1name=_ass1name ,_class1=_class1, _class2=_class2, _class3=_class3, _class1Mark=_class1Mark,
                       _class2Mark=_class2Mark, _class3Mark=_class3Mark, _userFName=_userFName, _userLName=_userLName,
                       _userEmail=_userEmail, _userClass=_userClass, _nextAssDueDate=_nextAssDueDate,
                       _nextAssDueSub=_nextAssDueSub, _nextAssDueDetail=_nextAssDueDetail,
                       _nextAssDueTask=_nextAssDueTask, _avgMark=_avgMark, _weakMarkSub=_weakMarkSub,
                       _weakMark=_weakMark, _strongMarkSub=_strongMarkSub, _strongMark=_strongMark, _userType=_userType, _totalComplete=_totalComplete)

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
    # else:
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
    error = None
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
    # Pull User's Name
    # could use storedproc?
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
    global _userType

    _userDetails = cursor.fetchall()
    print(_userDetails)
    _userFName = (_userDetails[0][0])
    _userLName = (_userDetails[0][1])
    _userEmail = (_userDetails[0][2])
    _memberID = (_userDetails[0][3])
    _userID = (_userDetails[0][4])
    # _userFName = (str(_userFName).replace('(',"").replace("'","").replace(",","").replace(")",""))
    print(_userFName)
    # cursor.execute("SELECT lname from user where email ='" + _inputEmail + "';")
    # _userLName = cursor.fetchall()
    # _userLName = (str(_userLName).replace('(',"").replace("'","").replace(",","").replace(")",""))
    print(_userLName)
    # cursor.execute("SELECT email from user where email ='" + _inputEmail + "';")
    # global _userEmail
    # _userEmail = cursor.fetchall()
    # _userEmail = (str(_userEmail).replace('(',"").replace("'","").replace(",","").replace(")",""))
    print(_userEmail)

    # Determine user type:
    # RETURN DIFFERENT RENDER TEMPLATE BASED ON OUTCOME OF THIS ROUTINE
    if _memberID == 1:
        _userType = 'student'
    elif _memberID == 2:
        _userType = 'teacher'
    elif _memberID == 3:
        _userType = 'parent'

        # DETERMINE AVERAGE MARKS
        cursor.execute(
            "SELECT AVG(finalmark) FROM submission JOIN user on submission.user_userID = user.userID WHERE user.email='" + _inputEmail + "';")
        _avgMark = cursor.fetchall()
        print(_avgMark)
        # DETERMINE NUM OF COMPLETED ASSIGNMENTS WIHTIN PAST 9 MONTHS
        cursor.execute(
            "SELECT COUNT(*) FROM submission WHERE user_userID ='" + _userID + "' AND finalmark <>'' AND submission.date > DATE_SUB(now(), INTERVAL 9 MONTH);")
        _totalComplete = cursor.fetchall()
        print(_totalComplete)

        # DETERMINE STRONGEST SUBJECT MARKS
        cursor.execute(
            "SELECT MAX(finalmark), class.title FROM submission JOIN assignment on submission.assignment_assID = assignment.assID JOIN class on assignment.class_classID = class.classID JOIN user on submission.user_userID = user.userID WHERE user.userID='" + _userID + "';")
        _strongMark = cursor.fetchall()
        _strongMarkSub = (_strongMark[0][1])
        _strongMark = (_strongMark[0][0])

        # DETERMINE WEAKEST SUBJECT
        cursor.execute(
            "SELECT MIN(finalmark), class.title FROM submission JOIN assignment on submission.assignment_assID = assignment.assID JOIN class on assignment.class_classID = class.classID JOIN user on submission.user_userID = user.userID WHERE user.email='" + _inputEmail + "';")
        _weakMark = cursor.fetchall()
        _weakMarkSub = (_weakMark[0][1])
        _weakMark = (_weakMark[0][0])

        # Find list of all assignments without a mark assigned (INCOMPLETE SUBMISSIONS)
        cursor.execute(
            "SELECT inputFileName, inputFilePath, finalmark, teachcomment, assignment_assID, user_userID FROM submission WHERE user_userID ='" + _userID + "' AND finalmark ='';")
        _assignsDue = cursor.fetchall()
        print(_assignsDue)

        # Find list of all assignments with a mark assigned (COMPLETED SUBMISSIONS)
        cursor.execute(
            "SELECT inputFileName, inputFilePath, finalmark, teachcomment, assignment_assID, user_userID FROM submission WHERE user_userID ='" + _userID + "' AND finalmark <>'';")
        _assignsComplete = cursor.fetchall()
        print(_assignsComplete)

    # DETERMINE IF PASSWORD MATCHES PASSWORD STORED IN DATABASE
    if _inputpass == _verifiypass:
        if _memberID == 1:
            return showTableTest2()
        elif _memberID == 2:
            return showteachtables()
        elif _memberID == 3:
            error = 'Invalid username or password'
            return render_template('loginV3.html', error=error)
    elif _inputpass == '':
        error = 'Invalid username or password'
        return render_template('loginV3.html', error=error)
    elif _inputEmail != _verifiypass:
        error = 'Invalid username or password'
        return render_template('loginV3.html', error=error)




























# ADD Students to class(es) VIA NAMES AND CLASS NAME
# def return_user_details():
@app.route('/classManageAddName', methods=['GET', 'POST'])
def manageclasses():  # WORKS
    # GET DATA FROM FORMS

    _stuFname = request.form['stuFname']
    _stuLname = request.form['stuLname']
    _className = request.form['className']
    # GET STUDENT DATA FROM FORMS
    # cursor.execute("INSERT INTO classregister(users_userID, class_classID) values('" + (str(_userID)) + "','" + str((_classID)) + "');")
    cursor.execute(
        "INSERT INTO classregister(users_userID, class_classID) SELECT user.userID, class.classID FROM user, class WHERE user.fname=('" + _stuFname + "' ) AND user.lname =('" + _stuLname + "') AND class.title = ('" + _className + "' );")
    conn.commit()
    return render_template('tabletests2.html')


# REMOVE students from classes
# NO LONGER NEEDED
@app.route('/classManageRemove', methods=['GET', 'POST'])
def manageClassRemove():  # WORKS
    # GET DATA FROM FORMS
    _userID = request.form['userID']
    _classID = request.form['classID']
    # GET STUDENT DATA FROM FORMS
    cursor.execute(
        "DELETE FROM classregister WHERE users_userID =('" + (str(_userID)) + "') AND class_classID = ('" + str(
            (_classID)) + "');")
    conn.commit()
    return render_template('tabletests2.html')


# REMOVE students from classes VIA STUDENT NAME AND CLASS TITLE
@app.route('/classManageRemoveName', methods=['GET', 'POST'])
def manageClassRemoveName():  # WORKS
    # GET DATA FROM FORMS
    _userID = request.form['userID']
    _classID = request.form['classID']
    _stuFname = request.form['stuFname']
    _stuLname = request.form['stuLname']
    _className = request.form['className']
    # GET STUDENT DATA FROM FORMS
    # cursor.execute("DELETE FROM classregister WHERE users_userID =('" + (str(_userID)) + "') AND class_classID = ('" + str((_classID)) + "');")
    cursor.execute(
        "DELETE classregister FROM classregister JOIN user ON classregister.users_userID = user.userID JOIN class ON classregister.class_classID = class.classID WHERE user.fname=('" + _stuFname + "' ) AND user.lname =('" + _stuLname + "') AND class.title = ('" + _className + "' );")
    conn.commit()
    return render_template('tabletests2.html')


# REMOVE students from classes VIA STUDENT NAME AND CLASS TITLE
@app.route('/passManage' , methods=['GET', 'POST'])
def passManage():  # WORKS
    # GET DATA FROM FORMS
    _stuFname = request.form['stuFname']
    _stuLname = request.form['stuLname']
    _stuEmail = request.form['stuEmail']
    _stuNewPass = request.form['stuNewPass']
    print(_stuNewPass)
    # GET STUDENT DATA FROM FORMS
    #cursor.execute(
    #   "UPDATE user SET user.password = 'Example' WHERE user.email = 'a';")
    print("Successfully updated password")
    cursor.execute("UPDATE user SET user.password = ('" + _stuNewPass + "') WHERE user.email = ('" + _stuEmail + "');")
    #cursor.execute("UPDATE `project`.`user` SET `password` = '(" + _stuNewPass + "')' WHERE `lname` = '('" + _stuLname + "')' AND `fname` = '('" + _stuFname + "' )' AND `email` = '('" + _stuEmail + "' )';")
    conn.commit()
    return render_template('teachtables.html')


# TEACHERS VARIABLE SETTING
# def teachervar():

@app.route('/addSubmission2', methods=['GET', 'POST'])
#THIS WORKS FOR NEXT DUE ONLY
def addSubmission2():
    global _userID
    global _nextAssDueID
    print('FILE UPLOAD')
    print(_userID)
    print(_nextAssDueID)
    #Get data from form
    if 'inputfile' not in request.files:
        print("failed")
    else:
        print("Success")
        inputFile = request.files['inputfile']
        #if inputFile.filename == '':
        #    flash("No file selected")
        #    return (redirect('tableTests2'))
        if inputFile and allowed_files(inputFile.filename):
            filename = secure_filename(inputFile.filename)
            inputFile.save(os.path.join(app.config['UPLOAD_FOLDER_SUBMISSION'], filename))
            _inputFileName = filename
            _inputFilePath = os.path.join(app.config['UPLOAD_FOLDER_SUBMISSION'], filename)
            print(_inputFileName)
            print(_inputFilePath)
            # read the posted values from the UI (modal script)
            _assID = _nextAssDueID


            print(_assID)
            _userID = _userID
            print(_userID)
            cursor.callproc('addSubmission2', (_inputFileName, _inputFilePath, _assID, _userID))
            data = cursor.fetchall()
            print(data)
            conn.commit()
    return render_template('tabletests2.html')

@app.route('/addSubmission3', methods=['GET', 'POST'])
#THIS WORKS For assignment 2
def addSubmission3():
    global _userID
    global _nextAssDueID
    print('FILE UPLOAD')
    print(_userID)
    print(_nextAssDueID)
    #Get data from form
    if 'inputfile' not in request.files:
        print("failed")
    else:
        print("Success")
        inputFile = request.files['inputfile']
        #if inputFile.filename == '':
        #    flash("No file selected")
        #    return (redirect('tableTests2'))
        if inputFile and allowed_files(inputFile.filename):
            filename = secure_filename(inputFile.filename)
            inputFile.save(os.path.join(app.config['UPLOAD_FOLDER_SUBMISSION'], filename))
            _inputFileName = filename
            _inputFilePath = os.path.join(app.config['UPLOAD_FOLDER_SUBMISSION'], filename)
            print(_inputFileName)
            print(_inputFilePath)
            # read the posted values from the UI (modal script)
            _assID = _ass2DueID
            print(_assID)
            _userID = _userID
            print(_userID)
            cursor.callproc('addSubmission2', (_inputFileName, _inputFilePath, _assID, _userID))
            data = cursor.fetchall()
            print(data)
            conn.commit()
    return render_template('tabletests2.html')

@app.route('/addSubmission4', methods=['GET', 'POST'])
#THIS WORKS For assignment 3
def addSubmission4():
    global _userID
    global _nextAssDueID
    print('FILE UPLOAD')
    print(_userID)
    print(_nextAssDueID)
    #Get data from form
    if 'inputfile' not in request.files:
        print("failed")
    else:
        print("Success")
        inputFile = request.files['inputfile']
        #if inputFile.filename == '':
        #    flash("No file selected")
        #    return (redirect('tableTests2'))
        if inputFile and allowed_files(inputFile.filename):
            filename = secure_filename(inputFile.filename)
            inputFile.save(os.path.join(app.config['UPLOAD_FOLDER_SUBMISSION'], filename))
            _inputFileName = filename
            _inputFilePath = os.path.join(app.config['UPLOAD_FOLDER_SUBMISSION'], filename)
            print(_inputFileName)
            print(_inputFilePath)
            # read the posted values from the UI (modal script)
            _assID = _ass3DueID
            print(_assID)
            _userID = _userID
            print(_userID)
            cursor.callproc('addSubmission2', (_inputFileName, _inputFilePath, _assID, _userID))
            data = cursor.fetchall()
            print(data)
            conn.commit()
    return render_template('tabletests2.html')






if __name__ == "__main__":
    app.run(debug=True)
