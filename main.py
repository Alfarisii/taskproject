from flask import Flask,render_template, jsonify
from flaskext.mysql import MySQL
app = Flask(__name__)
#namenya harus sama kaya nama filenya.

@app.route('/')
def index():
    return "hello world"
#define routenya   

def init_db(app):
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
    app.config['MYSQL_DATABASE_DB'] = 'sholaccati'
    mysql = MySQL(app)


#@app.route('/day', methods = ['GET','POST'])

@app.route('/day', methods = ['POST'])
def create_day():
    return "this is create endpoint"  

@app.route('/day/view')
def view_day():
    # ambil data dari DB
    # connect ke DB
    return "this is view endpoint" 

@app.route('/day/delete')
def delete_day():
    return "this is view delete endpoint"  

if __name__ == '__main__':
    app.run(debug = True)