import os
import yaml
import pandas as pd
import streamlit as st

from srcs.streamlit_app import app_utils, widgets

CONFIG = './config.yaml'
st.set_page_config(page_title='labelStream', layout='wide')

def main():
    # load project config
    app_utils.load_config(CONFIG)
    # load list of available projects
    projects = app_utils.load_projects()
    st.title('Label data')
    st.sidebar.title('Projects')
    with st.sidebar:
        if len(projects) == 0:
            st.write('No available project. Please add a new project.')
        else:
            current_project = st.radio('Select a project to work with:', projects)

        projects = widgets.add_project(projects)
        projects = widgets.delete_project(projects)


if __name__ == '__main__':
    main()
