from flask import Flask
app = Flask(__name__)
@app.route('/')
def home():
    return '<html><body><h1><strong><i>There is no news</i></strong></h1></body></html>'
if __name__ == '__main__':
    app.run(port=int("3000"),debug = True)