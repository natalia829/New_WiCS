import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import sqlite3
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup
from datetime import datetime

#some code is based on CS50's Finance pSet
UPLOAD_FOLDER = 'static/'


#This code is based on a code sample found on https://pythonise.com/series/learning-flask/flask-uploading-files
app = Flask(__name__)
app.config["IMAGE_UPLOADS"] = "static/"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF", "jpg", "png", "jpeg"]
app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024

image=None

#checks if file is an acceptable image file
def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

#checks if image is an acceptable size
def allowed_image_filesize(filesize):

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///attendance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

#homepage
@app.route("/")
@login_required
def index():
    return render_template("index.html")

#shows coding resources/gender gap info
@app.route("/resources")
@login_required
def resources():
    return render_template("resources.html")

#Allows admin account to approve attendance log requests based on photo user inputted or other form of proof. Updates what user see on their account to whetherit was approved or not.
@app.route("/approve", methods=["GET", "POST"])
@login_required
def approve():
    if request.method == "GET":
        dlist = []
        #Shows a list of all the attendance requests that have not been decided on
        rows = (db.execute("SELECT user_id, name, event_name, category, photo1, other_proof, event_num, time FROM events WHERE approve IS NULL"))
        for row in rows:
            user_id = row['user_id']
            event_num = row['event_num']
            name = row['name']
            event_name = row['event_name']
            category = row['category']
            photo1 = row['photo1']
            time = row['time']
            other_proof = row['other_proof']
            dlist.append({'user_id': user_id, 'name': name, 'event_name': event_name, 'category': category, 'photo1': photo1, 'time': time, 'other_proof': other_proof, 'event_num': event_num})
        return render_template("approve.html", dlist = dlist)
    else:
        if not request.form.get("status"):
            return apology("must provide status", 403)
        #gets status from the user and updates that request to be approved or not approved in sql table.
        approve = request.form.get("status")
        event_num = request.form.get("event_num")
        '''UPDATE table_name SET column1 = value1, column2 = value2, ... WHERE condition;'''
        db.execute("UPDATE events SET approve = (:approve) WHERE event_num = (:event_num)", approve = approve, event_num = event_num)
        return redirect("/approve")

#This shows all of the users attendance logs, and whether they were approved or not
@app.route("/history")
@login_required
def history():
    username = session["user_id"]
    dlist = []
    '''gets all of that users attendance history'''
    rows = (db.execute("SELECT event_name, category, photo1, other_proof, time, approve FROM events WHERE user_id = :username", username = username))
    '''gets how many events the user has attended in each category that were not denied'''
    large_social_dict = (db.execute("SELECT COUNT(category) FROM events WHERE user_id = :username AND category = 'Large Social' AND (approve IS NULL OR approve = 'Approved')", username = username))
    ls = large_social_dict[0]['COUNT(category)']
    small_social_dict = (db.execute("SELECT COUNT(category) FROM events WHERE user_id = :username AND category = 'Small Social' AND (approve IS NULL OR approve = 'Approved')", username = username))
    ss = small_social_dict[0]['COUNT(category)']
    sponsorship_dict = (db.execute("SELECT COUNT(category) FROM events WHERE user_id = :username AND category = 'Sponsorship' AND (approve IS NULL OR approve = 'Approved')", username = username))
    sp = sponsorship_dict[0]['COUNT(category)']
    educational_dict = (db.execute("SELECT COUNT(category) FROM events WHERE user_id = :username AND category = 'Educational' AND (approve IS NULL OR approve = 'Approved')", username = username))
    ed = educational_dict[0]['COUNT(category)']
    total = int(ls) + int(ss) + int(sp) + int(ed)
    '''they need to attend at least 6 events, so this finds the percentage of events they've gone to'''
    progress = round((total/6) * 100)
    '''so that the progress bar does not say more than 100%'''
    if progress >= 100:
        progress = int(100)
    else:
        progress = progress
    print (progress)
    '''this is all properly formatting the senctence that tells the user how events in each category they have to attend and how many total events left'''
    response = []
    lst = 'one large social event'
    sst = 'one small social event'
    spt = 'one sponorship event'
    edt = 'one educational event'
    edu = ''
    edu2 = ''
    edul = ''
    check = True
    if ls == 0:
        response.append(lst)
        check = False
    if ss == 0:
        response.append(sst)
        check = False
    if sp == 0:
        response.append(spt)
        check = False
    if ed == 0:
        response.append(edt)
        check = False
    print (response)
    edu2 = 'You still need to attend ' + str(6 - total) + ' events.'
    '''this checks that they are missing at least one category, and formats it so that there is a period in between each category and an and before the last one'''
    if check == False:
        edu = ('You need '+', '.join(response[:-1]) + ',')
        edul = ('and ' + response[-1] + '.')
    num = 1
    approve = ''
    for row in rows:
        event_name = row['event_name']
        category = row['category']
        photo1 = row['photo1']
        time = row['time']
        other_proof = row['other_proof']
        if not row['approve']:
            approve = 'Pending'
        else:
            approve = row['approve']
        '''creates list of dictionaries to display data'''
        dlist.append({'event_name': event_name, 'category': category, 'photo1': photo1, 'time': time, 'other_proof': other_proof, 'num': num, 'approve': approve})
        num = num + 1
    return render_template("history.html", dlist = dlist, progress = progress, edu = edu, edu2 = edu2, check = check, total = total, edul = edul)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

#this code is based on sample code found on https://pythonise.com/series/learning-flask/flask-uploading-files
@app.route("/attendance", methods=["GET", "POST"])
@login_required
def attendance():
    if request.method == "POST":
        #getting information from submitted attendance form
        name = request.form.get("name")
        event_name = request.form.get("event_name")
        category = request.form.get("category")
        photo1 = request.form.get("image")
        other_proof =  request.form.get("other_proof")
        username = session["user_id"]
        now = datetime.now()
        time = now.strftime("%d/%m/%Y %H:%M:%S")
        fn = ''
        #saves image into static/ folder in CS50 IDE
        if request.files:
            if "filesize" in request.cookies:

                if not allowed_image_filesize(request.cookies["filesize"]):
                    print("Filesize exceeded maximum limit")
                    return redirect(request.url)

                image = request.files["image"]

                if image.filename == "":
                    print("No filename")
                    return redirect(request.url)

                if allowed_image(image.filename):
                    filename = secure_filename(image.filename)

                    image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))

                    print("Image saved")

                    fn = str(filename)

                    #return redirect(request.url)

                else:
                    print("That file extension is not allowed")
                    return redirect(request.url)

            print(fn)
        #puts all the info into sql table
        db.execute("INSERT INTO events(user_id, name, event_name, category, photo1, other_proof, time) VALUES (:username, :name, :event_name, :category, :fn, :other_proof, :time)",
        username=username, name = name, event_name = event_name, category = category, fn = fn, other_proof = other_proof, time = time)


    return render_template("attendance.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        elif not request.form.get("password2"):
            return apology("must re-enter password", 403)
        username = request.form.get("username")
        password= request.form.get("password")
        password1 = request.form.get("password2")
        if password1 == password:
            hash1 = generate_password_hash(request.form.get("password"))
            rows = db.execute("INSERT INTO users(username, hash) VALUES (:username, :hash)", username=username, hash=hash1)
            if not rows:
                return apology("username already exists", 403)
            session["user_id"] = rows
            print("got here")
            return redirect("/")
        else:
            return apology("passwords do not match", 403)
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")



def errorhandler(e):
#Handle error
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)