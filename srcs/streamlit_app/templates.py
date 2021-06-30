from typing import List


def label_list_html(labels: List[str]) -> str:
    """ HTML scripts to display a list of labels. """
    if len(labels) > 0:
        html = f"""
            <ul style="margin-bottom:1.1em;">
                {' '.join([f'<li> {label} </li>' for label in labels])}
            </ul>
        """
    else:
        html = """
            <div style="color:grey;font-size:90%;margin-bottom:1.1em;">
                Label has not been defined yet.
            </div>
        """
    return html


def create_date_html(date: str) -> str:
    """ HTML scripts to display the create date of a project. """
    return f"""
        <div style="color:grey;font-size:90%;">
            Created at {date}
        </div>
    """
