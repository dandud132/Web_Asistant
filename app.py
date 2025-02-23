from flask import Flask

app = Flask(__name__)

@app.route('/Sign_in')
def registration():

if __name__ == '__main__':
    app.run()