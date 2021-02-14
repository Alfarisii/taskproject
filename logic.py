def show_all_day(db):
    query = 'select name,allowed_hours from days; '
    #kenapa didefine kolomnya? biar tau indexnya apa saja karena fetchall itu jadi array 2D
    cursor = db.get_db().cursor()

    cursor.execute(query)
    query_result = cursor.fetchall()
    #ini dibuat fetchall supaya jadi array 2D atau array dalam array.
    # [
    #   [monday,12],
    #   [tuesday,8]
    # ]
    res = []
    for row in query_result:
        temp = {
            "day_name" : row[0],
            "allowed_hours" : row[1]
        }
        res.append(temp)
    cursor.close()
    #{{'name':'monday'}}
    return res

def show_all_task(db):
    query = 'select duration,name,id_day from task; '
    cursor = db.get_db().cursor()

    cursor.execute(query)
    query_result = cursor.fetchall()
    res = []
    for row in query_result:
        temp = {
            "duration" : row[0],
            "name" : row[1],
            "id_day" : row[2],
        }
        res.append(temp)
    cursor.close()
    return res

def insert_day(db, day, allowed_hours):
    cursor = db.get_db().cursor()
    query = 'insert into days(name,allowed_hours) values("{0}", {1})'.format(day, allowed_hours)
    print(query)
    cursor.execute(query)
    db.get_db().commit()

    cursor.close()
    #{{'name':'monday'}}
    return

def insert_task(db, duration, name, id_day):
    cursor = db.get_db().cursor()
    query = 'insert into task(duration, name, id_day) values({0},"{1}",{2})'.format(duration, name, id_day)
    print(query)
    cursor.execute(query)
    db.get_db().commit()

    cursor.close()
    return


def delete_day(db, id):
    cursor = db.get_db().cursor()
    query = 'delete from days where id = {0};'.format(id)
    #id adalah {0}.format(12) nanti jadi concenate string supaya bisa gabung.
    #id adalah 12, sama kaya {0} 
    print(query)
    cursor.execute(query)
    db.get_db().commit()

    cursor.close()
    #{{'name':'monday'}}
    return cursor.rowcount

def delete_task(db, id):
    cursor = db.get_db().cursor()
    query = 'delete from task where id = {0};'.format(id)
    #id adalah {0}.format(12) nanti jadi concenate string supaya bisa gabung.
    #id adalah 12, sama kaya {0} 
    print(query)
    cursor.execute(query)
    db.get_db().commit()

    cursor.close()
    #{{'name':'monday'}}
    return cursor.rowcount

def update_day(db, day, allowed_hours, id):
    cursor = db.get_db().cursor()
    query = 'update days set name = "{0}", allowed_hours = {1} where id = {2};'.format(day, allowed_hours, id)

    print(query)
    cursor.execute(query)
    db.get_db().commit()

    cursor.close()
    #{{'name':'monday'}}
    return

def update_task(db, duration, name, id_day, id):
    cursor = db.get_db().cursor()
    query = 'update task set duration = {0}, name = "{1}", id_day = "{2}"  where id = {3};'.format(duration, name, id_day, id)

    print(query)
    cursor.execute(query)
    db.get_db().commit()

    cursor.close()
    return


def get_duration_task(db,id_day):
    query = 'select SUM(duration),allowed_hours from task inner join days ON days.id=task.id_day where id_day = {0};'.format(id_day)
    cursor = db.get_db().cursor()

    cursor.execute(query)
    query_result = cursor.fetchall()
    res = []
    for row in query_result:
        temp = {
            "duration" : row[0],
            "allowed_hours" : row[1],
        }
        res.append(temp)
    cursor.close()
    return res

def Show_all_item(db):
    query = 'select duration,task.name,task.id_day,days.id,days.name,allowed_hours from task join days ON days.id=task.id_day ; '
    #kenapa didefine kolomnya? biar tau indexnya apa saja karena fetchall itu jadi array 2D
    cursor = db.get_db().cursor()

    cursor.execute(query)
    query_result = cursor.fetchall()
    res = []
    for row in query_result:
        temp = {
            "duration_task" : row[0],
            "name_task" : row[1],
            "id_task" : row[2],
            "id_day" : row[3],
            "day_name" : row[4],
            "allowed_hours" : row[5]
        }
        res.append(temp)
    cursor.close()
    #{{'name':'monday'}}
    return res

def All_task_day(db,id_day,res):  
    #returnnya array jadi dedefine
    final_result = []
    for row in res:
        temp = {
            "id_task" : row["id_task"],
            "duration_task" : row["duration_task"],
            "name_task" : row["name_task"]
        }
        if row["id_day"] == id_day:
           final_result.append(temp)
    return final_result

def Show_all(db):
    res = Show_all_item(db)
    final_result = []
    id_prev = []
    for row in res:
        temp = {
            "id_day" : row["id_day"],
            "day_name" : row["day_name"],
            "allowed_hours" : row["allowed_hours"],
            "task" : All_task_day(db,row["id_day"],res)
        }
        if row["id_day"] not in id_prev:
            id_prev.append(row["id_day"])
            final_result.append(temp)
        #kalo final result itu dictionary jadi tdk mudah dan code cleannya tidak baik, jadi mending lebih mudah dibaca kaya gini. self explanatory.
    return final_result