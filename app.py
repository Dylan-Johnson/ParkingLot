from flask import Flask, render_template, redirect
import json

app = Flask(__name__)

##################### Values #####################
#
#   0. Parking Lots: 1 Hardcoded Parking Lot (Maybe more in the future)
#       x, y, width, height, number, status
lot1 = [[20, 20, 150, 100, 1, 1], [250, 250, 150, 100, 2, -1],[20, 400, 150, 100, 3, 1]]
#
#   1. SQL Values (DB, User, Pass, etc. Hardcoded in Python)
db = None
dbUser = None
dbPass = None
#       Schema:
#       1a. User
#           int pk UserID
#           varchar(30) Username
#           varchar Password (Hashed)
#       1b. Privileges
#           int UserID
#           int LotID
#           int PrivilegeLevel      0 - None       1 - Admin        2 - Owner
#       1c. Notifications
#           int LotId
#           int ParkingSpace
#   2. Stored (Cookie) Data
#       2a. UserID  (Got to remember how to do this)

##################### Templates #####################
#
#   0. Base Template - Base HTML/CSS, Jinja2 blocks for other templates         (base.html)
#   1. Create Account / Sign In Template                                        (signinregister.html)
#   2. Settings Template                                                        (settings.html)
#   3. Parking Lot Template                                                     (lot1.html)
#   4. Notifications Template                                                   (notifications.html)
#   5. QR Code Template(s)                                                      (qr.html) (qrresult.html)

##################### Static #####################
#
#   0. QR Code Backing Graphic                                                  (qr.png)
#   1. JavaScript files (If not stored in the templates)                        (Optional)
#   2. Placeholder QR images (Must be saved before being displayed              (Determined at run-time)


# Route 0:  Home Page                           (All)
@app.route('/')
def homepage():
    ### Pseudocode ###
    #
    # Render the homepage template
    #
    ##################
    return None

# Route 1:  Create Account                      (All)
@app.route('/register')
def register():
    ### Pseudocode ###
    #
    # Allow the route to handle POST and GET info
    # If POST:
    #   Check if the username is valid
    #   Check if the password is valid
    #   If both are valid, sanitize data, place it into a database, return to login template
    #   Otherwise, return an error message to the user through the register template
    # Else if GET:
    #   Render the register template
    #
    ##################
    return None

# Route 2:  Log In                              (All)
@app.route('/login')
def login():
    ### Pseudocode ###
    #
    # Allow the route to handle POST and GET info
    # If POST:
    #   Check if the username-password combo exists in the database
    #   If it is, add userID to cache data, render home page template
    #   Otherwise, return an error message to the user through the login template
    # Else if GET:
    #   Render the register template
    #
    ##################
    return None

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
@app.route('/space/<space>')
def space(space):
    ### Pseudocode ###
    #
    # We need to work on the logic for this one; Shouldn't be too hard
    #
    ##################

    # Grabs the space and changes the status
    mySpace = int(space)
    lot1[mySpace-1][5] *= -1

    #return space
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
    ### Pseudocode ###
    #
    # Perform Flask logout work; Clear cache
    #
    ##################
    return None


# Route 9: Grabs JSON data of our parking lot for AJAX in our website
@app.route('/getdata')
def getdata():
    return (json.dumps(lot1))

if __name__ == '__main__':
    app.run()
