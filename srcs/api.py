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


@app.route(f'{API_ENDPOINTS["GET_PROJECT_INFO"]}/<project_name>', methods=['GET'])
@cross_origin()
def get_project_info(project_name: str):
    """ Get and return project information in a dictionary. """
    df = pd.read_csv(os.path.join(PROJECT_DIR, 'projects.csv'))
    selected_df = df.loc[df.project == project_name].reset_index()
    label = selected_df.label[0]
    label = [] if str(label) == 'nan' else label.split(':sep:')
    return {
        'project': project_name,
        'createDate': selected_df.createDate[0],
        'description': selected_df.description[0],
        'label': label,
    }


@app.route(API_ENDPOINTS['LOAD_PROJECTS'], methods=['GET'])
@cross_origin()
def get_all_projects():
    """ Get and return list of projects. """
    try:
        df = pd.read_csv(os.path.join(PROJECT_DIR, 'projects.csv'))
        projects = df.project.to_list()
    except FileNotFoundError:
        projects = []

    return {'projects': projects}


@app.route(f'{API_ENDPOINTS["CREATE_PROJECT"]}/<project_name>', methods=['PUT'])
@cross_origin()
def create_project(project_name: str):
    """ Get and return list of projects. """
    to_append = {
        'project': [project_name],
        'createDate': [str(datetime.now()).split('.')[0]],
        'description': ['Add description at here.'],  # default description
        'label': None,  # default label
    }
    df_to_append = pd.DataFrame(to_append)
    try:
        df = pd.read_csv(os.path.join(PROJECT_DIR, 'projects.csv'))
        df = df.append(df_to_append, ignore_index=True)
    except FileNotFoundError:
        df = df_to_append

    df.to_csv(os.path.join(PROJECT_DIR, 'projects.csv'), index=False)
    return {'success': True}, 200, {'ContentType': 'application/json'}


@app.route(f'{API_ENDPOINTS["DELETE_PROJECT"]}/<project_name>', methods=['DELETE'])
@cross_origin()
def delete_project(project_name):
    """ Delete an existing project. """
    df = pd.read_csv(os.path.join(PROJECT_DIR, 'projects.csv'))
    df = df[df['project'] != project_name]
    df.to_csv(os.path.join(PROJECT_DIR, 'projects.csv'), index=False)
    return {'success': True}, 200, {'ContentType': 'application/json'}


@app.route(f'{API_ENDPOINTS["UPDATE_PROJECT_INFO"]}/<project_name>', methods=['POST'])
@cross_origin()
def update_project_info(project_name):
    """ Update information of an existing project. """
    new_info = request.get_json()
    new_description = new_info['description']
    new_label = ':sep:'.join(new_info['label'])
    df = pd.read_csv(os.path.join(PROJECT_DIR, 'projects.csv'))
    id = df.project == project_name
    df.loc[id, 'description'] = new_description
    df.loc[id, 'label'] = new_label
    df.to_csv(os.path.join(PROJECT_DIR, 'projects.csv'), index=False)
    return {'success': True}, 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    app.run(debug=True)
