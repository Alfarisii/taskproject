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

def insert_day(db, day, allowed_hours):
    cursor = db.get_db().cursor()
    query = 'insert into days(name,allowed_hours) values("{0}", {1})'.format(day, allowed_hours)
    print(query)
    cursor.execute(query)
    db.get_db().commit()

    cursor.close()
    #{{'name':'monday'}}
    return