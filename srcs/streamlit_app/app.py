import streamlit as st

from srcs.streamlit_app import app_utils, templates, widgets

CONFIG = './config.yaml'
st.set_page_config(page_title='labelStream', layout='wide')


def main():
    set_session_state()
    # load project config
    app_utils.load_config(CONFIG)
    # load list of available projects
    st.session_state.projects = app_utils.load_projects()
    with st.sidebar:
        st.sidebar.title('Projects')
        project_holder = st.empty()  # placeholder to show available projects
        widgets.add_project()
        widgets.delete_project()
        # display list of available projects
        if len(st.session_state.projects) == 0:
            project_holder.write('No available project. Please add a new project.')
        else:
            st.session_state.current_project = project_holder.radio(
                'Select a project to work with:', st.session_state.projects,
            )

    left_column, _, right_column = st.columns([50, 2, 20])
    # display and update project info at the right column
    if st.session_state.current_project is not None:
        # get project info for the first time or when switching projects
        if st.session_state.project_info is None or \
                st.session_state.project_info['project'] != st.session_state.current_project:
            app_utils.get_project_info()

        with right_column:
            # display project name
            st.header(st.session_state.current_project)
            # display project creation datetime
            st.write(templates.create_date_html(st.session_state.project_info['createDate']),
                     unsafe_allow_html=True)
            # project description text area
            widgets.project_description()
            # placeholder to display the labelling progress
            progress_holder = st.empty()
            # placeholder to display list of labels
            label_list_holder = st.empty()
            # expander to add label
            widgets.add_label()
            # expander to delete label
            widgets.delete_label()

            # import data
            file, add_data, text_column = widgets.import_data()
            app_utils.add_texts(file, add_data, text_column)
            # export data
            download_placeholder = widgets.export_data()

    # display data and labelling at the left column
    with left_column:
        st.title('Text Classification Data')
        if st.session_state.current_project is not None:
            current_page = st.session_state.current_page
            data = app_utils.get_data()
            st.session_state.data = data
            if data['total'] > 0:
                st.write(templates.page_number_html(current_page, data['total']),
                         unsafe_allow_html=True)
                st.write(templates.text_data_html(data['text']), unsafe_allow_html=True)
                # display checkboxes for labeling
                if len(st.session_state.project_info['label']) > 0:
                    new_labels, verify_label = widgets.label_data()
                    if verify_label:
                        app_utils.update_label_data(new_labels)
                else:
                    st.write(templates.no_label_html(), unsafe_allow_html=True)
                # display the verification datetime
                if st.session_state.data['verified'] != '0':
                    st.write(templates.verified_datetime_html(st.session_state.data['verified']),
                             unsafe_allow_html=True)
            else:
                st.write('No data in this project. Please import data to start labeling.')
        else:
            st.write('No project. No data. No cry.')

    # update placeholders
    if st.session_state.current_project is not None:
        # display list of defined labels
        label_list_holder.write(
            templates.label_list_html(st.session_state.project_info['label']),
            unsafe_allow_html=True,
        )
        # display progress bar if there is data (not None)
        if st.session_state.project_info['progress'] is not None:
            progress = int(st.session_state.project_info["progress"])
            progress = f'{progress / st.session_state.data["total"] * 100:.2f}'
            progress_holder.write(
                templates.progress_bar_html(progress), unsafe_allow_html=True,
            )
        # display a download button upon clicking the export button
        if st.session_state.download is not None:
            download_placeholder.write(
                templates.save_csv_html(*st.session_state.download),
                unsafe_allow_html=True,
            )


def set_session_state():
    """ """
    para = st.experimental_get_query_params()
    # clicked next or previous page
    if 'page' in para.keys():
        st.experimental_set_query_params()
        new_page = max(1, int(para['page'][0])) - 1  # make sure the min is 0
        st.session_state.current_page = new_page

    # default values
    st.session_state.projects = []
    st.session_state.current_project = None
    st.session_state.project_info = None
    st.session_state.data = None
    st.session_state.download = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 0


if __name__ == '__main__':
    main()
