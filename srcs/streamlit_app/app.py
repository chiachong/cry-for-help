import streamlit as st

from srcs.streamlit_app import app_utils, SessionState, templates, widgets

CONFIG = './config.yaml'
st.set_page_config(page_title='labelStream', layout='wide')
session_state = SessionState.get(projects=[], current_page=0, current_project=None,
                                 project_info=None, data=None, download=None)


def main():
    update_session_state(session_state)
    # load project config
    app_utils.load_config(CONFIG)
    # load list of available projects
    session_state.projects = app_utils.load_projects()
    with st.sidebar:
        st.sidebar.title('Projects')
        project_holder = st.empty()  # placeholder to show available projects
        widgets.add_project(session_state)
        widgets.delete_project(session_state)
        # display list of available projects
        if len(session_state.projects) == 0:
            project_holder.write('No available project. Please add a new project.')
        else:
            session_state.current_project = project_holder.radio(
                'Select a project to work with:', session_state.projects,
            )

    _, left_column, right_column, _ = st.beta_columns([1, 50, 20, 1])
    # display and update project info at the right column
    if session_state.current_project is not None:
        # get project info for the first time or when switching projects
        if session_state.project_info is None or \
                session_state.project_info['project'] != session_state.current_project:
            app_utils.get_project_info(session_state)

        with right_column:
            # display project name
            st.header(session_state.current_project)
            # display project creation datetime
            st.write(templates.create_date_html(session_state.project_info['createDate']),
                     unsafe_allow_html=True)
            updates = []
            # project description text area
            updates.append(widgets.project_description(session_state))
            # placeholder to display the labelling progress
            progress_holder = st.empty()
            # placeholder to display list of labels
            label_list_holder = st.empty()
            # expander to add label
            updates.append(widgets.add_label(session_state))
            # expander to delete label
            updates.append(widgets.delete_label(session_state))
            # update description and labels
            if any(updates):
                app_utils.update_project_info(session_state)

            # import data
            file, add_data, text_column = widgets.import_data()
            app_utils.add_texts(session_state, file, add_data, text_column)
            # export data
            download_placeholder = widgets.export_data(session_state)

    # display data and labelling at the left column
    with left_column:
        st.title('Text Classification Data')
        if session_state.current_project is not None:
            current_page = session_state.current_page
            data = app_utils.get_data(session_state)
            session_state.data = data
            if data['total'] > 0:
                st.write(templates.page_number_html(current_page, data['total']),
                         unsafe_allow_html=True)
                st.write(templates.text_data_html(data['text']), unsafe_allow_html=True)
                # display checkboxes for labeling
                if len(session_state.project_info['label']) > 0:
                    new_labels, verify_label = widgets.label_data(session_state)
                    if verify_label:
                        app_utils.update_label_data(session_state, new_labels)
                else:
                    st.write(templates.no_label_html(), unsafe_allow_html=True)
                # display the verification datetime
                if session_state.data['verified'] != '0':
                    st.write(templates.verified_datetime_html(session_state.data['verified']),
                             unsafe_allow_html=True)
            else:
                st.write('No data in this project. Please import data to start labeling.')
        else:
            st.write('No project. No data. No cry.')

    # update placeholders
    if session_state.current_project is not None:
        # display list of defined labels
        label_list_holder.write(
            templates.label_list_html(session_state.project_info['label']),
            unsafe_allow_html=True,
        )
        # display progress bar if there is data (not None)
        if session_state.project_info['progress'] is not None:
            progress = int(session_state.project_info["progress"])
            progress = f'{progress / session_state.data["total"] * 100:.2f}'
            progress_holder.write(
                templates.progress_bar_html(progress), unsafe_allow_html=True,
            )
        # display a download button upon clicking the export button
        if session_state.download is not None:
            download_placeholder.write(
                templates.save_csv_html(*session_state.download),
                unsafe_allow_html=True,
            )


def update_session_state(session_state):
    para = st.experimental_get_query_params()
    # clicked next or previous page
    if 'page' in para.keys():
        st.experimental_set_query_params()
        new_page = max(1, int(para['page'][0])) - 1  # make sure the min is 0
        session_state.current_page = new_page


if __name__ == '__main__':
    main()
