from flask_login import LoginManager, login_manager
from flask import Flask, render_template, json, request, url_for, redirect, flash
from flaskext.mysql import MySQL
from werkzeug.utils import secure_filename

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

app.secret_key=b'1234567v8fvfdvm'
conn = mysql.connect()
cursor = conn.cursor()

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/testtables')
def showTableTest():
    return render_template('tabletests.html')

@app.route('/tabletests2')
def showTableTest2():
    return render_template('tabletests2.html')

@app.route('/modaltest')
def showModalTest():
    return render_template('modaltest.html')





#USER SIGNUP#
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

#ADD NEW ASSIGNMENT#
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

#ADD NEW SUBMISSION#
@app.route('/addSub', methods=['POST', 'GET'])
def addSub():
    if 'inputfile' not in request.files:
        print("failed")
    else:
        print("Success")
        inputFile = request.files['inputfile']
        if inputFile.filename =='':
            flash("no file selected")
            return(redirect('tableTests2'))
        if inputFile and allowed_files(inputFile.filename):
            filename = secure_filename(inputFile.filename)
            inputFile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            _inputFileName = filename
            _inputFilePath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
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

            cursor.callproc('addSubmission', (_date, _inputFileName, _inputFilePath, _finalMark, _teachComment, _assignmentID, _userID))
            data = cursor.fetchall()
            print(data)
            conn.commit()

        return render_template('testing.html')

#USER SIGN IN#
#@bull.route("/loginV3", methods=["GET", "POST"])
#def login():
 #   """For GET requests, display the login form.
  #  For POSTS, login the current user by processing the form.
   # """
    #form = LoginForm()
    #if form.validate_on_submit():
     #   user = User.query.get(form.email.data)
      #  if user:
       #     if bcrypt.check_password_hash(user.password, form.password.data):
        #        user.authenticated = True
         #       db.session.add(user)
          #      db.session.commit()
           #     login_user(user, remember=True)
            #    return redirect(url_for("bull.reports"))
    #return render_template("loginV3.html", form=form)



@app.route('/login', methods=['POST', 'GET'])
def login():
    if "login" in request.form:
        return render_template('loginV3.html')
    elif "signup" in request.form:
        return render_template('signup.html')
    return render_template('loginV3.html')


if __name__ == "__main__":
    app.run(debug=True)


