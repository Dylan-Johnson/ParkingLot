from flask import Flask, render_template, redirect
import json

app = Flask(__name__)


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
