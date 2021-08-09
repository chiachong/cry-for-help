import os
import json
import base64
import requests
import pandas as pd
import streamlit as st
from typing import List
from datetime import datetime

from srcs import utils


def add_texts(df: pd.DataFrame, add_data: bool, text_column: str,
              url: str = None):
    """ Add text data. """
    headers = {
        'content-type': 'application/json',
        'Accept-Charset': 'UTF-8',
    }
    if url is None:
        url = os.environ['API_ADDRESS'] + os.environ['ADD_DATA']

    url = f'{url}/{st.session_state.current_project}'
    if add_data and df is not None and text_column is not None:
        new_data = {'texts': df[text_column].to_list()}
        r = requests.put(url, data=json.dumps(new_data), headers=headers)
        # update progress in session state if it is None
        if st.session_state.project_info['progress'] is None:
            st.session_state.project_info['progress'] = '0'


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


def download_csv(project_name: str, all_or_labeled: str, url: str = None):
    """ Download csv of all data or just labeled data. """
    if url is None:
        url = os.environ['API_ADDRESS'] + os.environ['DOWNLOAD_DATA']

    url = f'{url}/{project_name}/{all_or_labeled}'
    r = requests.get(url)
    df = pd.DataFrame(r.json())
    csv = df.to_csv(index=False)  # if no filename is given, a string is returned
    csv = base64.b64encode(csv.encode()).decode()  # convert the csv into base64
    return csv


def get_data(url: str = None):
    """ Get data of the given project. """
    if url is None:
        url = os.environ['API_ADDRESS'] + os.environ['GET_DATA']

    url = f'{url}/{st.session_state.current_project}/{st.session_state.current_page}'
    r = requests.get(url)
    return r.json()


def get_project_info(url: str = None):
    """ Get information of the given project. """
    if url is None:
        url = os.environ['API_ADDRESS'] + os.environ['GET_PROJECT_INFO']

    url = f'{url}/{st.session_state.current_project}'
    r = requests.get(url)
    st.session_state.project_info = r.json()


@st.cache(show_spinner=False)
def load_config(config: str):
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


def update_label_data(new_labels: List[str], url: str = None):
    """ Update the labels of the labeled data. """
    headers = {
        'content-type': 'application/json',
        'Accept-Charset': 'UTF-8',
    }
    if url is None:
        url = os.environ['API_ADDRESS'] + os.environ['UPDATE_LABEL_DATA']

    url = f'{url}/{st.session_state.current_project}/{st.session_state.current_page}'
    verified = str(datetime.now()).split('.')[0] if len(new_labels) > 0 else '0'
    progress_changes = 1 if len(new_labels) > 0 else -1
    new_progress = f'{int(st.session_state.project_info["progress"]) + progress_changes}'
    data = {'new_labels': new_labels, 'verified': verified}

    r = requests.put(url, data=json.dumps(data), headers=headers)
    # update label and progress status into session state
    st.session_state.data['label'] = new_labels
    st.session_state.data['verified'] = verified
    st.session_state.project_info['progress'] = new_progress


def update_project_info(url: str = None):
    """ Update project description and labels. """
    headers = {
        'content-type': 'application/json',
        'Accept-Charset': 'UTF-8',
    }
    if url is None:
        url = os.environ['API_ADDRESS'] + os.environ['UPDATE_PROJECT_INFO']

    url = f'{url}/{st.session_state.current_project}'
    r = requests.post(url, data=json.dumps(st.session_state.project_info),
                      headers=headers)


def rerun():
    """ A hack to rerun streamlit app. """
    raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))
