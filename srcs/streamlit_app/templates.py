from typing import List


def label_list_html(labels: List[str]) -> str:
    """ HTML scripts to display a list of labels. """
    html = """
            <div style="font-size:115%;font-weight:450;">
                Labels
            </div>
            <hr style="margin-top:0.5em;margin-bottom:0.5em;">
    """
    if len(labels) > 0:
        html += f"""
            <ul style="margin-bottom:1.1em;">
                {' '.join([f'<li> {label} </li>' for label in labels])}
            </ul>
        """
    else:
        html += """
            <div style="color:grey;font-size:90%;margin-bottom:1.1em;">
                Label has not been defined yet.
            </div>
        """
    return html


def no_label_html(labels: List[str]) -> str:
    """ HTML scripts to display current label and update label. """
    return """
    <div style="color:grey;font-size:90%;margin-top:1em">
        Please define a label to start labelling.
    </div>
    """


def create_date_html(date: str) -> str:
    """ HTML scripts to display the create date of a project. """
    return f"""
        <div style="color:grey;font-size:90%;">
            Created at {date}
        </div>
    """


def page_number_html(current_page: int, total_page_number: int) -> str:
    """ HTML scripts to display the page number. """
    html = '<div style="text-align:center;width:90%;margin-top:0.3em;margin-bottom:0.5em;">'
    if current_page > 0:
        html += f'<a href="?page={current_page}" style="display:inline;">&lt</a>'

    html += f"""
        <p style="display:inline;">
            &emsp;{current_page + 1}/{total_page_number}&emsp;
        </p>
    """
    if current_page < total_page_number - 1:
        html += f'<a href="?page={current_page + 2}" style="display:inline;">&gt</a>'

    html += '</div>'
    return html


def text_data_html(text: str) -> str:
    """ HTML scripts to display text to be labelled. """
    style = """
        border: none;
        margin-bottom: 1em;
        padding: 20px;
        height: auto;
        width: 90%;
        box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
    """
    return f"""
        <div style="{style}">
            {text}
        </div>
    """


def verified_datetime_html(date_time: str) -> str:
    """ HTML scripts to display the verification datetime. """
    return f"""
        <div style="color:grey;font-size:90%;">
            Verified at {date_time}
        </div>
    """
