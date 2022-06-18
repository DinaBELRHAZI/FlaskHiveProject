import json

import flask

import requests


def read_all():
    return flask.redirect('/getall')


def read_one(id):
    return flask.redirect('/get/' + id)


def create(entreprise):
    _name = entreprise.get("name", None)
    _country = entreprise.get("country", None)
    _activity = entreprise.get("activity", None)
    _id = entreprise.get("id", None)

    params = {"id": _id, "name": _name, "country": _country, "activity": _activity}
    response = requests.post('http://127.0.0.1:5000/add', json=params)
    return flask.redirect('/getall')


def update(id, entreprise):
    _name = entreprise.get("name", None)
    _country = entreprise.get("country", None)
    _activity = entreprise.get("activity", None)

    params = {"name": _name, "country": _country, "activity": _activity}
    response = requests.post('http://127.0.0.1:5000/update/' + id, json=params)
    return flask.redirect('/get/' + id)


def delete(id):
    return flask.redirect('/delete/' + id)
