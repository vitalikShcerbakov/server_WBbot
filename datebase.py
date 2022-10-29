import sqlite3
from datetime import datetime
from unittest import result

# con = sqlite3.connect('db.sqlite', check_same_thread=False)
# cur = con.cursor()

lst = [52232480, 52233119, 52233721,
        52234352, 67578772, 67586679, 67591155, 82455840, 67588134, 38272884, 38272572, 38272793, 38272922, 34964682,
        31066345, 33147977, 33144939, 88107650, 88108097, 88108208, 113068831, 113068944]

#cur.execute('''DROP TABLE vendors_codes;''')
def write_to_database(list_vc: list) -> None:
    '''Write to value datebase.'''
    con = sqlite3.connect('db.sqlite', timeout=10)
    cur = con.cursor()
    cur.execute('DELETE FROM vendors_codes;')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS vendors_codes(
        codes INTEGER,
        status TEXT,
        error_type TEXT,
        date TEXT);
    ''')

    for line in list_vc:
        print(line)
        code, stutus, error_type = line
        cur.execute(f'''
        INSERT INTO vendors_codes(codes, status, error, date)
        VALUES ({code}, {error_type}, {stutus}, '{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")}');''')
    con.commit()
    con.close() 

def read_from_datebase():  # ToDo annotation
    con = sqlite3.connect('db.sqlite', timeout=10)
    cur = con.cursor()
    cur.execute('SELECT * FROM vendors_codes;')
    result = cur.fetchall()
    con.commit()
    con.close() 
    return result

# write_to_database(lst)
# print(read_from_datebase())

# if __name__ == '__main__':
#     print_hi('PyCharm')
