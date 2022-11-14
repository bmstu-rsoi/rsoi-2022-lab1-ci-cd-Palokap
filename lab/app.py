import os
from flask import Flask, request, Response
from database import DataBase

app = Flask(__name__)

@app.route("/api/v1/persons/", methods=['GET'])
def get_all():
    person = DataBase()
    result = person.get_all_persons()
    person.disconnect()
    return result, 200


@app.route("/api/v1/persons/<int:personID>", methods=['GET'])
def get(personID):
    person = DataBase()
    try:
        result = person.get_person(person_id=personID)
    except IndexError:
        person.disconnect()
        return Response(status=404)
    person.disconnect()
    print(request.host)
    return dict(result), 200


@app.route("/api/v1/persons/", methods=['POST'])
def post():
    insert_data = request.json

    person = DataBase()

    insert_data_tuple = (insert_data['name'], insert_data['address'], insert_data['work'], insert_data['age'])
    new_person_id = person.post_person(insert_data_tuple)
    person.disconnect()
    return app.redirect(f"{request.host}/api/v1/persons/{new_person_id[0]}", code=201)


@app.route("/api/v1/persons/<int:personID>", methods=['PATCH'])
def patch(personID):
    person = DataBase()
    try:
        result = person.patch_person(personID, request.json)
    except TypeError:
        person.disconnect()
        return Response(status=404)
    person.disconnect()
    print(result)
    return result, 200


@app.route("/api/v1/persons/<int:personID>", methods=['DELETE'])
def delete(personID):
    person = DataBase()
    try:
        person.delete_person(personID)
    except TypeError:
        person.disconnect()
        return Response(status=404)
    person.disconnect()
    return Response(status=204)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port, host="0.0.0.0")
