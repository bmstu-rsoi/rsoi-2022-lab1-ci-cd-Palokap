from flask import Flask, request, Response
from database import DataBase

app = Flask(__name__)

@app.route("/api/v1/persons/", methods=['GET'])
def get_all():
    person = DataBase()
    result = person.get_all_persons()
    return result, 200


@app.route("/api/v1/persons/<int:personID>", methods=['GET'])
def get(personID):
    person = DataBase()
    try:
        result = person.get_person(person_id=personID)[0]
    except IndexError:
        return Response(status=404)
    print(request.host)
    return result, 200


@app.route("/api/v1/persons/", methods=['POST'])
def post():
    insert_data = request.json

    person = DataBase()

    insert_data_tuple = (insert_data['name'], insert_data['address'], insert_data['work'], insert_data['age'])
    new_person_id = person.post_person(insert_data_tuple)
    return app.redirect(f"{request.host}/api/v1/persons/{new_person_id[0]}", code=201)


@app.route("/api/v1/persons/<int:personID>", methods=['PATCH'])
def patch(personID):
    person = DataBase()
    try:
        result = person.patch_person(personID, request.json)
    except TypeError:
        return Response(status=404)
    print(result)
    return result, 200


@app.route("/api/v1/persons/<int:personID>", methods=['DELETE'])
def delete(personID):
    person = DataBase()
    try:
        person.delete_person(personID)
    except TypeError:
        return Response(status=404)
    return Response(status=204)

if __name__ == '__main__':
    app.run()
