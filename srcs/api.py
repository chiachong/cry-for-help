import os
import pandas as pd
from datetime import datetime
from flask import Flask, request, jsonify, abort
from flask_cors import cross_origin
from flask_restful import Resource, Api, reqparse

from srcs import utils

CONFIG = utils.load_yaml('./config.yaml')
API_ENDPOINTS = CONFIG['API_ENDPOINTS']
PROJECT_DIR = CONFIG['PROJECT_DIR']

os.makedirs(PROJECT_DIR, exist_ok=True)
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)


@app.route(API_ENDPOINTS['LOAD_PROJECTS'], methods=['GET'])
@cross_origin()
def get_projects():
    """ Get and return list of projects. """
    try:
        df = pd.read_csv(os.path.join(PROJECT_DIR, 'projects.csv'))
        projects = df.projects.to_list()
    except FileNotFoundError:
        projects = []

    return {'projects': projects}


@app.route(f'{API_ENDPOINTS["CREATE_PROJECT"]}/<name>', methods=['PUT'])
@cross_origin()
def create_project(name):
    """ Get and return list of projects. """
    datetime_now = str(datetime.now()).split('.')[0]
    try:
        df = pd.read_csv(os.path.join(PROJECT_DIR, 'projects.csv'))
        to_append = {'projects': name, 'createDate': datetime_now}
        df = df.append(to_append, ignore_index=True)
    except FileNotFoundError:
        df = pd.DataFrame({'projects': [name], 'createDate': [datetime_now]})

    df.to_csv(os.path.join(PROJECT_DIR, 'projects.csv'), index=False)
    return {'success': True}, 200, {'ContentType': 'application/json'}


@app.route(f'{API_ENDPOINTS["DELETE_PROJECT"]}/<name>', methods=['DELETE'])
@cross_origin()
def delete_project(name):
    """ Delete an existing project. """
    df = pd.read_csv(os.path.join(PROJECT_DIR, 'projects.csv'))
    df = df[df['projects'] != name]
    df.to_csv(os.path.join(PROJECT_DIR, 'projects.csv'), index=False)
    return {'success': True}, 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    app.run(debug=True)
