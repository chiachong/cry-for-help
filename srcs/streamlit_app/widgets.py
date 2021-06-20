import os
import sys
import streamlit as st
from typing import List

from srcs.streamlit_app import app_utils


def add_project(projects: List[str]) -> List[str]:
    """ An expander widgets to add new project """
    with st.beta_expander('Add new project'):
        new_project = st.text_input('New project name:',
                                    key='text_input_new_project_name')
        _add = st.button('Add', key='button_submit_add_project')
        if _add:
            if new_project in projects:
                st.warning(f'The name "{new_project}" is already exist.')
            else:
                app_utils.create_project(new_project)
                projects.append(new_project)
                app_utils.rerun()

        return projects


def delete_project(projects: List[str]) -> List[str]:
    """ Delete an existing project. """
    if len(projects) > 0:
        with st.beta_expander('Delete project'):
            project_to_delete = st.selectbox('Project to be deleted:', projects)
            _delete = st.button('Delete', key='button_submit_delete_project')
            if _delete:
                app_utils.delete_project(project_to_delete)
                projects.remove(project_to_delete)
                app_utils.rerun()

            return projects
