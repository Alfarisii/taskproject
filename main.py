from flask import Flask,render_template, jsonify, request
from db import init_db
from logic import show_all_day, insert_day, delete_day


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
    #butuh info apa aja : name, allowed hours
    #Json
    #param = baca_param[], 1. Baca requestnya
    print(request.get_json())
    body = request.get_json()
    is_valid = create_day_validation(body)
    #kalau true or false if akan tetap jalan
    #2. validasi requestnya
    if not is_valid :
        return {"Message" : "Request tidak valid"},400
    #3. Laksanakan requestnya dan masukan request.
    res = insert_day(db,body["name"],body["allowed_hours"])
    #4. balikin responnya
    result = {"Message" : "sukses ditambahkan"}
    print(type(request.get_json()))
    return result

@app.route('/day/view')
def view_day():
    # ambil data dari DB
    # connect ke DB
    #{{'name':'monday'}}
    # yang bisa di return itu cuman, dict, array dan bbrp hal
    res = show_all_day(db)
    return jsonify(res)

@app.route('/day/delete', methods = ['POST'])
def delete_day_handler():
    #butuh info apa aja : id
    print(request.get_json())
    body = request.get_json()
    #2. validasi requestnya
    is_valid = delete_day_validation(body)
    if not is_valid :
        return {"Message" : "Request tidak valid"},400
    #3. Laksanakan requestnya dan masukan request.
    rowcount = delete_day(db,body["id"])
    #4. balikin responnya
    if rowcount == 0:
        result = {"Message" : "ID tidak ada", "jumlah record terhapus" : rowcount}
    else:
        result = {"Message" : "sukses dihapus", "jumlah record terhapus" : rowcount}
    print(type(request.get_json()))
    return result

def create_day_validation(body) -> bool:
    expected_field = ["name","allowed_hours"]
    #expected fieldnya berbentuk list maka harus dirubah ke list
    sent_field = list(body.keys())

    result = True
    for body_field in sent_field:
        if body_field in expected_field:
            result = result and True
        else :
            result = result and False
    return result

def delete_day_validation(body) -> bool:
    expected_field = ["id"]
    #expected fieldnya berbentuk list maka harus dirubah ke list
    sent_field = list(body.keys())

    result = True
    for body_field in sent_field:
        if body_field in expected_field:
            result = result and True
        else :
            result = result and False
    return result

#["name";"allowed_hours"] ==> 

if __name__ == '__main__':
    app.run(debug = True)