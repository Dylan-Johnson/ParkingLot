from flask import Flask, render_template, redirect
import json

app = Flask(__name__)

##################### Values #####################
#
#   0. Parking Lots: 2 Hardcoded Parking Lots
#
#   1. SQL Values (DB, User, Pass, etc.)
#       1a. User
#           int pk UserID
#           varchar(30) Username
#           varchar Password (Hashed)
#       1b. Privileges
#           int UserID
#           int LotID
#           int PrivilegeLevel      0 - None       1 - Admin        2 - Owner
#   2. Stored (Cookie) Data
#       2a. UserID

##################### Routes #####################
#
#   0.  Home Page                           (All)
#   1.  Create Account                      (All)
#   2.  Log In                              (All)
#   3.  Settings
#       3a. Give/Revoke Admin Privileges    (Owner)
#       3b. See Admin Privileges            (All)
#   4.  View Parking Lot(s)                 (All)
#   5.  View Notifications                  (Admin)
#   6.  Parking Space Claims
#       6a. Claim Space                     (User) (Admin)
#       6b. Report Space                    (User)
#       6c. Free Space                      (User) (Admin)
#   7.  Generate QR Codes                   (Owner)

##################### Templates #####################
#
#   0. Base Template - Base HTML/CSS, Jinja2 blocks for other templates
#   1. Create Account / Sign In Template
#   2. Settings Template
#   3. Parking Lot Template
#   4. Notifications Template
#   5. QR Code Template(s)

##################### Static #####################
#
#   0. QR Code Backing Graphic
#   1. JavaScript files (If not stored in the templates)
#   2. Placeholder QR images (Must be saved before being displayed (Maybe...))

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/space/<space>')
def space(space):

    # Grabs the space and changes the status
    mySpace = int(space)
    testList[mySpace-1][5] *= -1

    #return space
    return redirect("/testCanvasLoad")

# Our parking lot data structure
# x, y, width, height, number, status
testList = [[20, 20, 150, 100, 1, 1], [250, 250, 150, 100, 2, -1],[20, 400, 150, 100, 3, 1]]


# Loads the parking lot
@app.route('/testCanvasLoad')
def testCanvasLoad():
    return render_template('lot.html', list=testList)

# Grabs JSON data of our parking lot for AJAX in our website
@app.route('/getdata')
def getdata():
    return (json.dumps(testList))

if __name__ == '__main__':
    app.run()
