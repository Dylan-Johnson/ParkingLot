from flask import Flask, render_template, redirect, request, flash, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import json
import mysql.connector

app = Flask(__name__)
app.config.from_mapping(
        SECRET_KEY='dev'
    )

##################### Values #####################
#
#   0. Parking Lots: 1 Hardcoded Parking Lot (Maybe more in the future)
#       x, y, width, height, number, status
#   For index 5, I suggest we set things as;
#       -  If 0, it is green (Nobody is taking up the space)
#       -  If > 0, it is red; taken up by someone logged in (Their session user ID is what we insert into the lot table)
#       -  If -1, it is red; taken up by someone using the QR code, or not logged in (If they don't have a session user ID)
lot1 = [[20, 20, 150, 100, 1, 0], [250, 250, 150, 100, 2, 0],[20, 400, 150, 100, 3, 0]]
#
#   1. SQL Values (DB, User, Pass, etc. Hardcoded in Python)
mydb = mysql.connector.connect(
  host="parkinglotdb.crbn8ocjq7lr.us-east-2.rds.amazonaws.com",
  user="admin",
  password="group6csc440"
)
#   1a. Schema under Schema.sql in Github
#   2. Stored (Cookie) Data
#       2a. UserID  (Got to remember how to do this)

##################### Templates #####################
#
#   0. Base Template - Base HTML/CSS, Jinja2 blocks for other templates         (base.html)
#   1. Create Account / Sign In Template                                        (signinregister.html)
#   2. Settings Template                                                        (settings.html)
#   3. Parking Lot Template                                                     (lot.html)
#   4. Notifications Template                                                   (notifications.html)
#   5. QR Code Template(s)                                                      (qr.html) (qrresult.html)

##################### Static #####################
#
#   0. QR Code Backing Graphic                                                  (qr.png)
#   1. JavaScript files (If not stored in the templates)                        (Optional)
#   2. Placeholder QR images (Must be saved before being displayed              (Determined at run-time)

# Function 0: Check for admin powers
def adminCheck():
    if session:
        # Query with session['user_id']
        try:
            mycursor = mydb.cursor()

            executeString = "SELECT * FROM ParkingLotSite.Privileges WHERE ID = %s" % (session['user_id'])
            mycursor.execute(executeString)

            user = mycursor.fetchone()

            mycursor.close()
            print("User",user)
            if user is not None:
                return True

        except:
            return False
    return False

# Route 0:  Home Page                           (All)
@app.route('/index')
def index():
    ### Pseudocode ###
    #
    # Render the homepage template
    #
    ##################

    # Test for if the sessions hold
    if session:
        print("Session ID:",session['user_id'])
    else:
        print("No Session")

    return render_template('base.html')

# Route 0a: Load user session
#@app.before_app_request
#def load_session_user():
#    user_id = session.get('user_id')
#
#    if user_id is None:
#        g.user = None
#    else:
#        mycursor = mydb.cursor()
#        g.user = mycursor.execute(
#            'SELECT * FROM ParkingLotSite.Users WHERE ID = ?', (user_id,)
#        ).fetchone()
#        mycursor.close()

# Route 1:  Create Account                      (All)
@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None

        # Extra work here to make sure username is valid and sanitized
        if not username: error = 'Username is required.'
        # Extra work here to make sure passwords are relatively secure and sanitized
        elif not password: error = 'Password is required.'

        if error is None:
            try:
                mycursor = mydb.cursor()
                executeString = "INSERT INTO ParkingLotSite.Users (username, password) VALUES (%s, %s)"
                val = (username, generate_password_hash(password))
                mycursor.execute(executeString,val)
                mydb.commit()
                mycursor.close()

            except:
                error = "Username is already taken."
            else:
                return redirect(url_for("login"))

        flash(error)

    return render_template('register.html', condition = "Register")

# Route 2:  Log In                              (All)
@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        # Sanitize username and password

        mycursor = mydb.cursor()

        executeString = "SELECT * FROM ParkingLotSite.Users WHERE username = \"%s\"" % (username)
        mycursor.execute(executeString)

        user = mycursor.fetchone()

        print(user)

        mycursor.close()

        #user[]: 0, ID; 1, username; 2, password

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[2], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user[0]
            return redirect(url_for('index'))

        flash(error)

    return render_template('login.html', condition = "Login")

# Route 3:  Settings
#       3a: Give/Revoke Admin Privileges        (Owner)
#       3b: See Admin Privileges                (All)
@app.route('/settings')
def settings():
    ### Pseudocode ###
    #
    # Allow the route to handle POST and GET info
    # If POST (Adding/Removing Privileges):
    #   If the user is an admin:
    #       Get user to add or remove
    #       Perform operation in the database
    #       Render the settings template
    # Else if GET:
    #   Return a list of admin privileges from the Privilege table for this user
    #   Return a list of admins for parking lots a user owns
    #   Render the template for settings
    #
    ##################
    return None

# Route 4:  View Parking Lot(s)                 (All)
@app.route('/parkinglot')
def parkinglot():
    ### Pseudocode ###
    #
    # May need to do something here; Otherwise it's done
    #
    ##################
    return render_template('lot.html', list=lot1)

# Route 5:  View Notifications                  (Admin)
@app.route('/notifications')
def notifications():
    # We want to display all notifications for a parking lot if the user is an admin of that lot.
    # Once a notification is handled, then we can remove it from the database
    ### Pseudocode ###
    #
    # Allow the route to handle POST and GET info
    # If the user is an admin:
    #   If POST:
    #       Remove particular notification from database
    #       Render notifications template
    #   Else if GET:
    #       Return a list of notifications for the admins' lot
    #       Render notifications template
    #
    ##################
    return None

# Route 6a; 6c
#       6a. Claim Space                     (User) (Admin)
#       6c. Free Space                      (User) (Admin)
@app.route('/space/<space>/<action>')
def space(space, action):
    ### Pseudocode ###
    #
    # We need to work on the logic for this one; Shouldn't be too hard
    #
    ##################
    error = None
    # Standard Case: Claiming a Space
    # If they claim a space, check if it is occupied. If it is, the user must be an admin for anything to take place.
    #   - If the admin changes the space, it is a non-signed-in user
    #   - If a signed-in user claims a space, put their session id in there
    #   - If a QR user claims a space, put -1
    print("Action:",action)
    if int(action) == 1:
        print("A")
        mySpace = int(space)
        if lot1[mySpace-1][5] != 0 and adminCheck() is False:
            print("Ba")
            error = 'Error: Space already occupied. If there is a discrepancy, alert an admin'
        if error is None:
            print("B")
            if adminCheck():
                lot1[mySpace - 1][5] = -1
            try:
                lot1[mySpace-1][5] = session['user_id']
            except:
                lot1[mySpace-1][5] = -1
        print(lot1)
    # If they free a space, check if it is unoccupied. Flash an error if it is.
    #   - If a user wants to free a space, they must be signed-in, and it must be their claimed space
    #   - If the user is an admin they can overwrite any space
    elif int(action) == 2:
        mySpace = int(space)
        if lot1[mySpace-1][5] == 0:
            error = 'Error: Space is already free'
        try:
            #if session is None:
            #    error = 'Error: Users not signed in must contact admins to free their spaces'
            if lot1[mySpace-1][5] != session['user_id'] and adminCheck() is False:
                error = 'Error: Cannot free another users space. Alert an admin.'
            elif adminCheck():
                lot1[mySpace-1][5]=0
            elif lot1[mySpace-1][5] == session['user_id']:
                lot1[mySpace-1][5]=0
        except:
            error = 'Error: Users not signed in must contact admins to free their spaces'

    #return space
    flash(error)
    return redirect("/parkinglot")

# Route 6b: Report Space                        (User)
@app.route('/reportspace/<space>')
def reportspace(space):
    ### Pseudocode ###
    #
    # Attempt to add the space-lot combo to the Notifications table
    # Render parking lot template; alert user that a notification has been sent
    #
    ##################
    return None

# Route 7:  Generate QR Codes                   (Owner)
@app.route('/qrcreator')
def qrcreator():
    ### Pseudocode ###
    #
    # Allow the route to handle POST and GET info
    # If user is Owner:
    #   If POST:
    #       (QR Work...)
    #   Else if GET:
    #       Render QR template
    ##################
    return None

# Route 8:  Sign Out                            (All)
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# Route 9: Grabs JSON data of our parking lot for AJAX in our website
@app.route('/getdata')
def getdata():
    return (json.dumps(lot1))

if __name__ == '__main__':
    app.run()
