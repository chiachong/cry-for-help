import pandas as pd
import streamlit as st
from typing import List

from srcs.streamlit_app import app_utils, templates


def add_and_display_label(labels: List[str]):
    """ An expander widgets to display labels and add label """
    with st.expander('Labels'):
        label_list_html = templates.label_list_html(labels)
        st.write(label_list_html, unsafe_allow_html=True)
        new_label = st.text_input('Define new label:')
        _add = st.button('Submit', key='button_submit_define_label')
    return new_label, _add


def add_label():
    """ An expander widget to add label. """
    def submit_add(expander, label):
        if new_label in st.session_state.project_info['label']:
            expander.warning(f'The label "{new_label}" is already exist.')
        else:
            st.session_state.project_info['label'].append(label)
            app_utils.update_project_info()

    expander = st.expander('Add label')
    with expander:
        new_label = st.text_input('Define new label:')
        st.button('Add', key='button_submit_define_label', on_click=submit_add,
                  args=(expander, new_label, ))


def add_project():
    """ An expander widgets to add new project """
    def submit_add(expander, project_name):
        if project_name in st.session_state.projects:
            expander.warning(f'The name "{project_name}" is already exist.')
        else:
            app_utils.create_project(project_name)
            st.session_state.projects.append(project_name)

    expander = st.expander('Add new project')
    with expander:
        new_project = st.text_input('New project name:',
                                    key='text_input_new_project_name')
        st.button('Add', key='button_submit_add_project', on_click=submit_add,
                  args=(expander, new_project, ))


def delete_label():
    """ An expander widget to delete a label. """
    def submit_delete(label):
        st.session_state.project_info['label'].remove(label)
        app_utils.update_project_info()

    labels = ['- Select -'] + st.session_state.project_info['label']
    with st.expander('Delete label'):
        to_delete = st.selectbox('Delete a label:', labels)
        if to_delete != '- Select -':
            st.button('Delete', key='button_submit_delete_label',
                      on_click=submit_delete, args=(to_delete, ))


def delete_project():
    """ Delete an existing project. """
    def submit_delete(project_name):
        app_utils.delete_project(project_name)
        st.session_state.projects.remove(project_name)

    if len(st.session_state.projects) > 0:
        with st.expander('Delete project'):
            project_to_delete = st.selectbox('Project to be deleted:',
                                             st.session_state.projects)
            st.button('Delete', key='button_submit_delete_project',
                      on_click=submit_delete, args=(project_to_delete, ))


def export_data():
    """
    An expander widget to export all data or just labeled data. This will return
    a streamlit placeholder to display download button after clicking the export
    button.
    """
    project_name = st.session_state.current_project
    format_dict = {
        'labeled': 'Labeled data',
        'all': 'All data',
    }
    with st.expander('Export data'):
        all_or_labeled = st.radio('Export all data or just labeled data',
                                  list(format_dict.keys()),
                                  format_func=lambda x: format_dict[x],
                                  key='button_all_or_labeled')
        export = st.button('Export', key='button_submit_export_data')
        if export:
            filename = f'{project_name}_{all_or_labeled}.csv'
            csv = app_utils.download_csv(project_name, all_or_labeled)
            st.session_state.download = (filename, csv)

        return st.empty()


def label_data():
    """ Checkboxes to label data. """
    labels = st.session_state.project_info['label']
    current_label = st.session_state.data['label']
    st.write('')  # an empty line to make spacing
    checkboxes = []
    for label in labels:
        pre_checked = True if label in current_label else False
        checkboxes.append(st.checkbox(label, pre_checked, f'label_{label}'))

    # capture any changes to the label checkboxes
    new_labels = [labels[i] for i in range(len(labels)) if checkboxes[i]]
    # display a submit button if any label checkboxes is changed
    if set(new_labels) != set(current_label):
        verify = st.button('Verify', key='button_submit_label_data')
    else:
        verify = None
    return new_labels, verify


def import_data():
    """ An expander widget to import data. """
    with st.expander('Import data'):
        file = st.file_uploader(label='Upload your csv file here.')
        if file is not None:
            df = pd.read_csv(file)
            # select the column containing the texts to be labelled
            column = st.radio('Column containing the texts', list(df.columns))
            _add = st.button('Import', key='button_submit_add_data')
            file = df
        else:
            _add, column = None, None

    return file, _add, column


def project_description():
    """ Text area for displaying and changing the project description. """
    def submit_save(text):
        st.session_state.project_info['description'] = text
        app_utils.update_project_info()

    description = st.session_state.project_info['description']
    # project description text area height
    text_area_height = (len(description) + 42 - 1) // 42 * 30
    new_description = st.text_area('', value=description, height=text_area_height)
    # display a button to save new description if the description is changed
    if new_description != description:
        st.button('Save', key='button_save_description', on_click=submit_save,
                  args=(new_description, ))
