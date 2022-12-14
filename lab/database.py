import psycopg2
from psycopg2 import Error

DB_URL="postgres://rcbpriibskjppp:95715df182d18d4ae450268d5a914062276e41ef746ff45fba2eb1832ab5bc6a@ec2-34-199-68-114" \
       ".compute-1.amazonaws.com:5432/dapcvpsn47bj5i"
class DataBase:
    def __init__(self):
        try:
            self.db = psycopg2.connect(DB_URL, sslmode="require")
            self.cursor = self.db.cursor()
            if not self.check_table():
                self.create_table()
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)

    def check_table(self):
        self.cursor.execute("""SELECT table_name FROM information_schema.tables
                  WHERE table_schema = 'public'""")
        for table in self.cursor.fetchall():
            if table[0] == "persons":
                return True
        return False

    def create_table(self):
        create_table_query = '''CREATE TABLE persons
                                   (
                                       PersonID    SERIAL PRIMARY KEY,
                                       NAME        VARCHAR(20),
                                       ADDRESS     VARCHAR(40),
                                       WORK        VARCHAR(30),
                                       AGE         INTEGER
                                   ); '''
        self.cursor.execute(create_table_query)
        self.db.commit()

    def get_person(self, person_id):

        self.cursor.execute(f"SELECT * FROM persons WHERE PersonID={person_id};")
        self.db.commit()

        row = self.cursor.fetchone()
        d = dict()
        d["id"] = int(row[0])
        d["name"] = row[1]
        d["address"] = row[2]
        d["work"] = row[3]
        d["age"] = row[4]
        return d

    def get_all_persons(self):
        self.cursor.execute(f"SELECT * From persons;")
        # persons = self.cursor.()
        # self.db.commit()

        rows = self.cursor.fetchall()
        objects_list = []
        for row in rows:
            d = dict()
            d["id"] = row[0]
            d["name"] = row[1]
            d["address"] = row[2]
            d["work"] = row[3]
            d["age"] = row[4]
            objects_list.append(d)
        return objects_list

    def post_person(self, insert_data):

        insert_query = "INSERT INTO persons (NAME, ADDRESS, WORK, AGE) " \
                       "VALUES (%s,%s,%s,%s) RETURNING PersonID"
        self.cursor.execute(insert_query, insert_data)
        self.db.commit()
        return self.cursor.fetchone()

    def patch_person(self, person_id, update_data):
        params = ""
        for key in update_data.keys():
            params += f"{key}='{update_data[key]}',"

        tmp = list(params)
        tmp[-1] = " "
        params = "".join(tmp)

        update_query = f"UPDATE persons SET {params} WHERE PersonID={person_id} " \
                       f"RETURNING PersonID, NAME, ADDRESS, WORK, AGE "
        self.cursor.execute(update_query)
        self.db.commit()
        row = self.cursor.fetchone()
        d = dict()
        d["id"] = row[0]
        d["name"] = row[1]
        d["address"] = row[2]
        d["work"] = row[3]
        d["age"] = row[4]
        self.db.commit()
        return d

    def delete_person(self, person_id):
        self.cursor.execute(f"DELETE FROM persons WHERE personID={person_id};")
        self.db.commit()
        return

    def disconnect(self):
        self.cursor.close()
        self.db.close()