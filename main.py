import json

import flask
from pyhive import hive
from flask import Flask, jsonify, Response, request, flash, redirect, render_template, make_response
from entreprises import entreprises
import connexion

# Création de  l'instance de l'application
app = connexion.App(__name__, specification_dir='./')

# Lecture du fichier swagger.yml pour définir les points d'arrivée (endpoints)
app.add_api('swagger.yml')

connection = hive.connect(host="192.168.246.128", username="cloudera",
                          port=10000)


# Get list of all entreprises
@app.route('/getall')
def getallentreprises():
    cursor = connection.cursor()
    query = "SELECT * FROM entreprises"
    cursor.execute(query)
    listRow = []
    for row in cursor.fetchall():
        print(row[0], row[1], row[2], row[3])
        entreprise = entreprises(row[0], row[1], row[2], row[3])
        jsonStr = json.dumps(entreprise.__dict__)
        print(jsonStr)
        listRow.append(entreprise)
        print(listRow)
    return Response(json.dumps([ob.__dict__ for ob in listRow]), mimetype='application/json')


# Get 1 entreprise by id
@app.route('/get/<id>')
def getone(id):
    print(id)
    cursor = connection.cursor()
    query = "SELECT * FROM entreprises WHERE id =" + id
    cursor.execute(query)
    test = cursor.fetchall()
    if (len(test) > 0):
        print(test)
        entreprise = entreprises(test[0][0], test[0][1], test[0][2], test[0][3])
        jsonStr = json.dumps(entreprise.__dict__)
        return Response(jsonStr, mimetype='application/json')
    else:
        return make_response(
            "the company don't exist. Please, change the id".format(lname=id), 200
        )


# Add 1 entreprise
@app.route('/add', methods=['GET', 'POST'])
def addone():
    try:
        _json = request.json
        _name = _json["name"]
        _country = _json['country']
        _activity = _json['activity']
        _id = _json['id']

        print(_name, _country)
        # validate the received values
        if _id and _name and _country and _activity and request.method == 'POST':
            cursor = connection.cursor()
            query = "INSERT INTO default.entreprises (id, name, country, activity) VALUES (%s, %s, %s, %s)"
            data = (_id, _name, _country, _activity)

            cursor.execute(query, data)

            # flash('User updated successfully!')
            return flask.redirect('/getall')
        else:
            return 'Error while adding company'

    finally:
        return flask.redirect('/getall')


# Update 1 entreprise
@app.route('/update/<id>', methods=['POST'])
def updateone(id):
    # print(id)

    try:
        _json = request.json
        _name = _json["name"]
        _country = _json['country']
        _activity = _json['activity']
        _id = id

        print(id, _country)
        # validate the received values
        if _name and _country and _activity and request.method == 'POST':
            cursor = connection.cursor()
            query = "UPDATE entreprises SET  name=%s, country=%s, activity=%s WHERE id=%s"
            data = (_name, _country, _activity, _id)

            cursor.execute(query, data)

            # flash('User updated successfully!')
            return flask.redirect('/get/' + id)
        else:
            return 'Error while adding entreprise'

    finally:
        return flask.redirect('/get/' + id)


@app.route('/delete/<id>', methods=['DELETE'])
def deleteone(id):
    try:
        cursor = connection.cursor()
        query = "DELETE FROM entreprises WHERE id =%s"
        cursor.execute(query, (id,))
        return flask.redirect('/getall')

    finally:
        return make_response(
            "the company successfully deleted".format(lname=id), 200
        )


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
