import psycopg2
from settings import host, user, password, db_name
from datetime import datetime

def create_connection(db_name, db_user, db_password, db_host):
    """Database connection"""
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
        )
        print("Connection to PostgreSQL DB successful")
    except Exception as e:
        print(f"The error '{e}' occurred")
    return connection

connection = create_connection(db_name, user, password, host )


def added_to_database_users(connection, id_user, name, is_send_out=True, is_admin=False):
    users = [
        (id_user, name, is_send_out, is_admin),
        ]
    user_records = ", ".join(["%s"] * len(users))
    insert_query = (
        f"INSERT INTO users_redeem (id_user, name, is_send_out, is_admin) VALUES {user_records}"
    )       
    connection.autocommit = True
    try:
        cursor = connection.cursor()
        cursor.execute(insert_query, users)
    except Exception as e:
        print(f'[INFO] error writing to database: {e}' )

    print(f'[INFO] Write to database successful')

def execute_read_query(table_name, connection=connection,):
    select_querty = (
        f'SELECT * from {table_name}'
    )
    try:
        cursor = connection.cursor()
        cursor.execute(select_querty)
        result = cursor.fetchall()
    except Exception as e:
        print(f'[INFO] error while reading from database: {e}' )

    finally:
        return result
#def reading_from_database():
answer = execute_read_query(connection, 'vendor_code_db')
for line in answer:
    print(line)


def added_to_database(vc_list, connection=connection):
    data = []
    for value in vc_list:
        data.append((value))

    user_records = ", ".join(["%s"] * len(data))
    insert_query = (
         f"INSERT INTO vendor_code_db (vc, url, description, status, date) VALUES {user_records}"
     )       
    connection.autocommit = True
    try:
         cursor = connection.cursor()
         cursor.execute(insert_query, data)
         print(f'[INFO] Write to database successful')
    except Exception as e:
        print(f'[INFO] error writing to database: {e}' )

    

def execute_read_query(connection):

    select_querty = (
        'SELECT * from users_redeem'
    )
    try:
        cursor = connection.cursor()
        cursor.execute(select_querty)
        result = cursor.fetchall()
    except Exception as e:
        print(f'[INFO] error while reading from database: {e}' )

    finally:
        return result





data = [
    ( 554545, 'http://google.com', 'это просто тест', True, now),
    ( 000000, 'http://google.com', 'это просто тест', True, now),
    ( 999999, 'http://google.com', 'это просто тест', True, now),
    ( 333333, 'http://google.com', 'это просто тест', True, now),
    ( 777777, 'http://google.com', 'это просто тест', True, now),
    ( 777777, None, None, None, None),
]
# added_to_database(connection, data)



# print(execute_read_query(connection))




# def execute_query(connection, query):
#     connection.autocommit = True
#     cursor = connection.cursor()
#     try:
#         cursor.execute(query)
#         print("Query executed successfully")
#     except Exception as e:
#            print(f"The error '{e}' occurred")
# create_users_table = """
#     CREATE TABLE IF NOT EXISTS vendor_code_db (
#       id SERIAL PRIMARY KEY,
#       vc INTEGER, 
#       url TEXT,
#       description TEXT,
#       status boolean,
#       date timestamp
#     );
#     """

# execute_query(connection, create_users_table)