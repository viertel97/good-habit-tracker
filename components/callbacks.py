import os

from dash import ALL, Input, Output, State, MATCH, ClientsideFunction
from dash import dcc
from dash.exceptions import PreventUpdate
from loguru import logger

from app import app
from services.html_service import generate_html, get_auto_close_callback
from services.proxy_service import get_questions, send_inputs

logger.add(
    os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/logs/" + os.path.basename(__file__) + ".log"),
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    backtrace=True,
    diagnose=True,
)


@app.callback(
    [Output("container", "children"), Output("memory", "data")],
    [Input("submit-form", "n_clicks"), Input("url", "pathname")],
    State("container", "children"),
)
def display_form(n_clicks, path, children):
    if not n_clicks > 0:
        questions = get_questions(path[1:])
        temp_list = generate_html(questions, children)
        return children, temp_list
    else:
        return None, None


special_characters = "!@#$%^&*()-+?_=,<>/~"


@app.callback(
    Output({'type': 'dynamic-output', 'index': MATCH}, 'children'),
    Input({'type': 'dynamic-input', 'index': MATCH}, 'value'),
)
def update_output(value):
    if value is not None:
        if any(c in special_characters for c in value):
            print(value)
            return dcc.Markdown(value)
    return PreventUpdate


@app.callback(
    Output("output", "children"),
    Input("submit-form", "n_clicks"),
    State({"type": "temp", "index": ALL}, "value"),
    State({"type": "dynamic-input", "index": ALL}, "value"),
    State("memory", "data"),
)
def display_output(n_clicks, inputs, dynamic_inputs, list_of_entries):
    if n_clicks > 0:
        combined_inputs = inputs + dynamic_inputs
        return send_inputs(combined_inputs, list_of_entries)
    else:
        return PreventUpdate


def generate_outputs(inputs):
    outputs = []
    for input_element in inputs:
        if input_element == "yes" or input_element == "no":
            outputs.append("")
        elif input_element:
            outputs.append(False)
        elif type(input_element) == int:
            outputs.append(None)
        else:
            outputs.append(None)
    return outputs


app.clientside_callback(
    ClientsideFunction(namespace="my_clientside_library", function_name="close_window"),
    [
        Output("output-js", "data"),
    ],
    [
        Input("output", "children"),
    ],
)