import os
from pathlib import Path

from app import app
from dash import ALL, Input, Output, State
from dash.exceptions import PreventUpdate
from loguru import logger
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


@app.callback(
    Output("output", "children"),
    Input("submit-form", "n_clicks"),
    State({"type": "temp", "index": ALL}, "value"),
    State("memory", "data"),
)
def display_output(n_clicks, inputs, list_of_entries):
    if n_clicks > 0:
        return send_inputs(inputs, list_of_entries)
    else:
        PreventUpdate


def generate_outputs(inputs):
    outputs = []
    for input in inputs:
        if input == "yes" or input == "no":
            outputs.append("")
        elif input == True:
            outputs.append(False)
        elif type(input) == int:
            outputs.append(None)
        else:
            outputs.append(None)
    return outputs


app.clientside_callback(
    get_auto_close_callback(),
    [
        Output("output-js", "data"),
    ],
    [
        Input("submit-form", "n_clicks"),
    ],
)
