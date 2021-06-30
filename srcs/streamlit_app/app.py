import os
import yaml
import pandas as pd
import streamlit as st

from srcs.streamlit_app import app_utils, templates, widgets

CONFIG = './config.yaml'
st.set_page_config(page_title='labelStream', layout='wide')


def main():
    # load project config
    app_utils.load_config(CONFIG)
    # load list of available projects
    projects = app_utils.load_projects()
    with st.sidebar:
        st.sidebar.title('Projects')
        if len(projects) == 0:
            st.write('No available project. Please add a new project.')
            current_project = None
        else:
            current_project = st.radio('Select a project to work with:', projects)

        projects = widgets.add_project(projects)
        projects = widgets.delete_project(projects)

    _, left_column, right_column, _ = st.beta_columns([1, 50, 20, 1])
    with left_column:
        st.title('Text Classification Data')
        st.write('No data in this project. Please import data to start labeling.')

    if current_project is not None:
        project_info = app_utils.get_project_info(current_project)
        labels = project_info['label']
        description = project_info['description']
        create_date = project_info['createDate']
        with right_column:
            st.header(current_project)
            st.write(templates.create_date_html(create_date), unsafe_allow_html=True)
            # project description text box height if the description is changed
            text_area_height = (len(description) + 42 - 1) // 42 * 30
            new_description = st.text_area('', value=description, height=text_area_height)
            add_description = False
            # display a button to save new project description
            if new_description != description:
                add_description = st.button('Save', key='button_save_description')

            new_label, add_label = widgets.add_and_display_label(labels)
            # update description and labels
            app_utils.update_project_info(current_project, project_info, new_label,
                                          new_description, add_label, add_description)



if __name__ == '__main__':
    main()
