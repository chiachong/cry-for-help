import os
import copy
import json
import requests
import pandas as pd
import streamlit as st
from typing import List

from srcs import utils


def add_texts(project_name: str, df: pd.DataFrame, add_data: bool,
              text_column: str, url: str = None):
    """ Add text data. """
    headers = {
        'content-type': 'application/json',
        'Accept-Charset': 'UTF-8',
    }
    if url is None:
        url = os.environ['API_ADDRESS'] + os.environ['ADD_DATA']

    url = f'{url}/{project_name}'
    if add_data and df is not None and text_column is not None:
        new_data = {'texts': df[text_column].to_list()}
        r = requests.put(url, data=json.dumps(new_data), headers=headers)


def create_project(project_name: str, url: str = None):
    """ Create a new project """
    if url is None:
        url = os.environ['API_ADDRESS'] + os.environ['CREATE_PROJECT']

    url = f'{url}/{project_name}'
    r = requests.put(url)


def delete_project(project_name: str, url: str = None):
    if url is None:
        url = os.environ['API_ADDRESS'] + os.environ['DELETE_PROJECT']

    url = f'{url}/{project_name}'
    r = requests.delete(url)


def get_data(project_name: str, current_page: int, url: str = None):
    """ Get data of the given project. """
    if url is None:
        url = os.environ['API_ADDRESS'] + os.environ['GET_DATA']

    url = f'{url}/{project_name}/{current_page}'
    r = requests.get(url)
    return r.json()


def get_project_info(project_name: str, url: str = None):
    """ Get information of the given project. """
    if url is None:
        url = os.environ['API_ADDRESS'] + os.environ['GET_PROJECT_INFO']

    url = f'{url}/{project_name}'
    r = requests.get(url)
    return r.json()


@st.cache(show_spinner=False)
def load_config(config: str) -> dict:
    """ Load project configurations from a .yaml file. """
    config = utils.load_yaml(config)
    os.environ['PROJECT_DIR'] = config['PROJECT_DIR']
    os.environ['API_ADDRESS'] = config['API_ADDRESS']
    for name, value in config['API_ENDPOINTS'].items():
        os.environ[name] = value


@st.cache(allow_output_mutation=True, show_spinner=False)
def load_projects(url: str = None) -> List[str]:
    """ Load list of available projects. """
    if url is None:
        url = os.environ['API_ADDRESS'] + os.environ['LOAD_PROJECTS']

    r = requests.get(url)
    return r.json()['projects']


def update_label_data(project_name: str, current_page: int, new_labels: List[str],
                      url: str = None):
    """ Update the labels of the labeled data. """
    headers = {
        'content-type': 'application/json',
        'Accept-Charset': 'UTF-8',
    }
    if url is None:
        url = os.environ['API_ADDRESS'] + os.environ['UPDATE_LABEL_DATA']

    url = f'{url}/{project_name}/{current_page}'
    data = {'new_labels': new_labels}
    r = requests.put(url, data=json.dumps(data), headers=headers)


def update_project_info(project_name: str, project_info: dict, new_label: str,
                        new_description: str, label_to_delete: str,
                        url: str = None):
    """ Update project description and labels. """
    headers = {
        'content-type': 'application/json',
        'Accept-Charset': 'UTF-8',
    }
    if url is None:
        url = os.environ['API_ADDRESS'] + os.environ['UPDATE_PROJECT_INFO']

    url = f'{url}/{project_name}'
    new_project_info = copy.deepcopy(project_info)
    if new_label is not None and new_label not in project_info['label']:
        new_project_info['label'].append(new_label)

    if label_to_delete is not None:
        new_project_info['label'].remove(label_to_delete)

    if new_description is not None:
        new_project_info['description'] = new_description

    if new_project_info['label'] != project_info['label'] or \
        new_project_info['description'] != project_info['description']:
        r = requests.post(url, data=json.dumps(new_project_info), headers=headers)
        rerun()


def rerun():
    """ A hack to rerun streamlit app. """
    raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))
