import psycopg2
from psycopg2 import Error

DB_URL="postgres://nwvzmcdjzclaxh:be877a3ee92c0212c530e7810f3de57f0743180da0a5bea2a"\
       "3a9f9a66f79e3c2@ec2-3-93-206-109.compute-1.amazonaws.com:5432/dfhpqakdtl0sv7"

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
                self.cursor.close()
                return True
        self.cursor.close()
        self.db.close()
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
        self.cursor.close()
        self.db.close()

    def get_person(self, person_id):

        self.cursor.execute(f"SELECT * From persons WHERE person_id={person_id};")
        self.db.commit()

        row = self.cursor.fetchone()
        d = dict()
        d["id"] = row[0]
        d["name"] = row[1]
        d["address"] = row[2]
        d["work"] = row[3]
        d["age"] = row[4]
        self.cursor.close()
        self.db.close()
        return d

    def get_all_persons(self):
        self.cursor.execute(f"SELECT * From persons;")
        persons = self.cursor.fetchall()
        self.db.commit()

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
        self.cursor.close()
        self.db.close()
        return persons

    def post_person(self, new_info):

        self.cursor.execute(
            f"INSERT INTO persons (person_id, name, address, work, age) VALUES (DEFAULT, '{new_info['name']}', "
            f"'{new_info['address']}', '{new_info['work']}', '{new_info['age']}') "
            f"RETURNING person_id;")
        self.db.commit()
        person = self.cursor.fetchone()
        self.cursor.close()
        self.db.close()
        return person[0]

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
        self.cursor.close()
        self.db.close()
        return d

    def delete_person(self, person_id):
        self.cursor.execute(f"DELETE FROM persons WHERE person_id={person_id};")
        self.db.commit()
        self.cursor.close()
        self.db.close()
        return