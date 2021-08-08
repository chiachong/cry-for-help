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


def no_label_html() -> str:
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
    current_page = min(total_page_number - 1, current_page)
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


def progress_bar_html(labeled_proportion: str) -> str:
    """ HTML scripts to display progress of labelling in percentage. """
    sub_header_style = """
        font-size: 115%;
        font-weight: 450;
        margin-top: 0.3em;
        margin-bottom: 0.3em;
    """
    container_style = """
        background-color: rgb(240, 240, 240);
        border-radius: 5px;
        width: 100%;
    """
    progress_bar_style = f"""
        background-color: rgb(246, 51, 102);
        height: 10px;
        border-radius: 5px;
        width: {labeled_proportion}%;
    """
    percent_style = f"""
        text-align: right;
        margin-bottom: 0.8em;
        font-size: 90%;
        width:{labeled_proportion}%;
    """
    return f"""
        <div style="{sub_header_style}">
            Verified
        </div>
        <div style="{container_style}">
            <div style="{progress_bar_style}">
            </div>
        </div>
        <div style="{percent_style}">
            {labeled_proportion}%
        </div>
    """


def save_csv_html(filename: str, csv: str) -> str:
    """ HTML scripts to display button to save exported data in csv file. """
    return f"""
        <style>
            #save_csv {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                background-color: rgb(255, 255, 255);
                color: rgb(38, 39, 48);
                padding: .25rem .75rem;
                position: relative;
                text-decoration: none;
                border-radius: 4px;
                border-width: 1px;
                border-style: solid;
                border-color: rgb(230, 234, 241);
                border-image: initial;
                margin-bottom: 1em;
            }}
            #save_csv:hover {{
                border-color: rgb(246, 51, 102);
                color: rgb(246, 51, 102);
            }}
            #save_csv:active {{
                box-shadow: none;
                background-color: rgb(246, 51, 102);
                color: white;
                }}
        </style>
        <a download="{filename}" id="save_csv" href="data:file/csv;base64,{csv}">
            Save to folder
        </a>
    """


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
