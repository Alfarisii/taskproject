from flask import Flask,render_template, jsonify, request
from db import init_db
#from logic import show_all_day, insert_day, delete_day, update_day, show_all_task, insert_task, delete_task, update_task, get_duration_task
from logic import *
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
db = init_db(app)
#namenya harus sama kaya nama filenya.
#unopiniated framework (flask)

@app.route('/')
def index():
    return "hello world"
#define routenya also there is @app.route('/day', methods = ['GET','POST'])

@app.route('/day/create', methods = ['POST'])
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
    res = insert_day(db,body["name"],body["allowed_hours"],)
    #4. balikin responnya
    result = {"Message" : "sukses ditambahkan"}
    print(type(request.get_json()))
    return result

@app.route('/task/create', methods = ['POST'])
def create_task():
    print(request.get_json())
    body = request.get_json()
    is_valid = create_task_validation(body)
    if not is_valid :
        return {"Message" : "Request tidak valid"},400
    #validasi untuk hoursnya
    duration = get_duration_task(db,body["id_day"])
    #kalo 1 itu jika ada 2 rows, 0,1
    durasi = duration[0]['duration']
    hours = duration[0]['allowed_hours']
    #and bukan && dan harus equal boolean 22nya.
    if durasi is None and hours is None:
        return {"Message" : "result not found"},400
    durasi += body["duration"]
    if durasi > hours :
        return {"Message" : "durasi melebihi jam"},400
    res = insert_task(db,body["duration"],body["name"],body["id_day"],)
    result = {"Message" : "sukses ditambahkan"}
    print(type(request.get_json()))
    return result

@app.route('/day/view')
def view_day():
    # ambil data dari DB
    # connect ke DB
    #{{'name':'monday'}}
    # yang bisa di return itu cuman, dict, array dan bbrp hal
    # here we want to get the value of user (i.e. ?user=some-value)
    min = request.args.get('min')
    max = request.args.get('max')
    #no need body because no JSON
    res = show_all_day(db,min,max)
    return jsonify(res)

@app.route('/task/view')
def view_task():
    res = show_all_task(db)
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

@app.route('/task/delete', methods = ['POST'])
def delete_task_handler():
    print(request.get_json())
    body = request.get_json()
    is_valid = delete_task_validation(body)
    if not is_valid :
        return {"Message" : "Request tidak valid"},400
    rowcount = delete_task(db,body["id"])
    if rowcount == 0:
        result = {"Message" : "ID tidak ada", "jumlah record terhapus" : rowcount}
    else:
        result = {"Message" : "sukses dihapus", "jumlah record terhapus" : rowcount}
    print(type(request.get_json()))
    return result
    
@app.route('/day/edit', methods = ['POST'])
def edit_day():
    #butuh info apa aja : name, allowed hours
    #Json
    #param = baca_param[], 1. Baca requestnya
    print(request.get_json())
    body = request.get_json()
    is_valid = update_day_validation(body)
    #kalau true or false if akan tetap jalan
    #2. validasi requestnya
    if not is_valid :
        return {"Message" : "Request tidak valid"},400
    #3. Laksanakan requestnya dan masukan request.
    res = update_day(db,body["name"],body["allowed_hours"],body["id"])
    #4. balikin responnya
    result = {"Message" : "sukses ditambahkan"}
    print(type(request.get_json()))
    return result

@app.route('/task/edit', methods = ['POST'])
def edit_task():
    print(request.get_json())
    body = request.get_json()
    is_valid = update_task_validation(body)
    if not is_valid :
        return {"Message" : "Request tidak valid"},400
    #validasi untuk hoursnya
    duration = get_duration_task(db,body["id_day"])
    #kalo 1 itu jika ada 2 rows, 0,1
    durasi = duration[0]['duration']
    hours = duration[0]['allowed_hours']
    #and bukan && dan harus equal boolean 22nya.
    if durasi is None and hours is None:
        return {"Message" : "result not found"},400
    durasi += body["duration"]
    if durasi > hours :
        return {"Message" : "durasi melebihi jam"},400
    
    res = update_task(db,body["duration"],body["name"],body["id_day"],body["id"])
    result = {"Message" : "sukses ditambahkan"}
    print(type(request.get_json()))
    return result

@app.route('/day/JSON', methods = ['GET'])
def JSON():
    # res = show_all_day(db)
    # res2 = show_all_task(db)
    # result = defaultdict(dict)
    # for sequence in (res, res2):
    #     for dictionary in sequence:
    #         result[dictionary['id']].update(dictionary)
    # for dictionary in result.values():
    #     dictionary.pop('id')
    res = Show_all(db)
    return jsonify(res)




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

def create_task_validation(body) -> bool:
    expected_field = ["duration", "name", "id_day"]
    sent_field = list(body.keys())

    result = True
    for body_field in sent_field:
        if body_field in expected_field:
            result = result and True
        else :
            result = result and False
    return result

def update_day_validation(body) -> bool:
    expected_field = ["name","allowed_hours","id"]
    #expected fieldnya berbentuk list maka harus dirubah ke list
    sent_field = list(body.keys())

    result = True
    for body_field in sent_field:
        if body_field in expected_field:
            result = result and True
        else :
            result = result and False
    return result


def update_task_validation(body) -> bool:
    expected_field = ["duration", "name", "id_day","id"]
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

def delete_task_validation(body) -> bool:
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