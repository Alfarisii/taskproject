from flask import Flask,render_template, jsonify
from db import init_db
from logic import show_all_day

app = Flask(__name__)
db = init_db(app)
#namenya harus sama kaya nama filenya.
#unopiniated framework (flask)

@app.route('/')
def index():
    return "hello world"
#define routenya also there is @app.route('/day', methods = ['GET','POST'])

@app.route('/day', methods = ['POST'])
def create_day():
    return "this is create endpoint"  

@app.route('/day/view')
def view_day():
    # ambil data dari DB
    # connect ke DB
    #{{'name':'monday'}}
    # yang bisa di return itu cuman, dict, array dan bbrp hal
    res = show_all_day(db)
    return jsonify(res)

@app.route('/day/delete')
def delete_day():
    return "this is view delete endpoint"  

if __name__ == '__main__':
    app.run(debug = True)