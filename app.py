import json

from flask import Flask, render_template

app = Flask(__name__)

Lot = [[101, -1],[102, -1], [103, -1], [104, -1], [105, -1]]

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/changeSpace/<spaceNo>')
def changeSpace(spaceNo):
    print(Lot)
    for x in Lot:
        if x[0] == int(spaceNo):
            x[1] = -(x[1])
    print(Lot)
    return render_template('base.html', num=200)

@app.route('/getParking')
def getParking():
    return render_template('lot.html', lotNo=Lot, num=200)

@app.route('/getdata')
def getdata():
    return (json.dumps(Lot))

if __name__ == '__main__':
    app.run()

