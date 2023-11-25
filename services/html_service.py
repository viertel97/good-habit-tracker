import os

import dash_bootstrap_components as dbc
from dash import dcc, html
from loguru import logger

logger.add(
    os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/logs/" + os.path.basename(__file__) + ".log"),
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    backtrace=True,
    diagnose=True,
)

PERSISTENCE = False


def generate_html(response, children):
    temp_list = []
    for entry in response:
        if entry["default_type"] == "boolean":
            children.append(create_radio_button(entry))
        elif entry["default_type"] == "slider":
            children.append(create_slider(entry, 5))
        elif entry["default_type"] == "big_slider":
            children.append(create_slider(entry, 10))
        elif entry["default_type"] == "radio_button":
            children.append(create_radio_buttons(entry))
        elif entry["default_type"] == "checklist":
            children.append(create_checklist(entry))
        elif entry["default_type"] == "textarea":
            children.append(create_textarea(entry))
        elif entry["default_type"] == "paragraph":
            children.append(create_paragraph(entry))
        elif entry["default_type"] == "h1":
            children.append(create_heading(entry, html.H1))
        elif entry["default_type"] == "h2":
            children.append(create_heading(entry, html.H2))
        elif entry["default_type"] == "h3":
            children.append(create_heading(entry, html.H3))
        elif entry["default_type"] == "h4":
            children.append(create_heading(entry, html.H4))
        elif entry["default_type"] == "h5":
            children.append(create_heading(entry, html.H5))
        else:
            children.append(create_text_box(entry))
        temp_list.append(entry)
    return temp_list


def get_image(code):
    path = f"assets/{code}.svg"
    if os.path.exists(path):
        return html.Img(src=path, className="img-fluid", style={"height": "30px", "width": "30px"})
    else:
        return None


def create_textarea(entry):
    return html.Div(
        [
            html.Br(),
            dbc.Label("{label}".format(label=entry["message"]), html_for=entry["code"]),
            html.Br(),
            dbc.Textarea(
                className="mb-3",
                id={"type": "temp", "index": entry["code"]},
                persistence=PERSISTENCE,
                persistence_type="session",
            ),
            html.Br(),
        ],
        className="mb-3",
    )


def create_slider(entry, number_of_values):
    options = [{"label": str(i), "value": i} for i in range(1, number_of_values + 1)]
    return html.Div(
        [
            html.Br(),
            get_image(entry["code"]),
            dbc.RadioItems(
                id={"type": "temp", "index": entry["code"]},
                inputClassName="btn-check",
                labelClassName="btn btn-outline-primary",
                labelCheckedClassName="active",
                options=options,
                inline=True,
                persistence=PERSISTENCE,
                persistence_type="session",
            ),
            dbc.Label("{label}".format(label=entry["message"]), html_for=entry["code"]),
            html.Br(),
            html.Br(),
        ],
        className="mb-3",
    )


def create_radio_buttons(entry):
    return html.Div(
        [
            html.Br(),
            dcc.RadioItems(
                id={"type": "temp", "index": entry["code"]},
                options=entry["message"].split(" | "),
                persistence=PERSISTENCE,
                persistence_type="session",
            ),
            html.Br(),
        ],
        className="mb-3",
    )


def create_checklist(entry):
    options = [{"label": x, "value": x} for x in entry["message"].split(" | ")]
    return html.Div(
        [
            html.Br(),
            dbc.Checklist(
                id={"type": "temp", "index": entry["code"]},
                options=options,
                persistence=PERSISTENCE,
                persistence_type="session",
                inline=False,
                style={"display": "grid"},
            ),
            html.Br(),
        ],
    )


def create_text_box(entry):
    return html.Div(
        [
            html.Br(),
            dbc.Label("{label}".format(label=entry["message"]), html_for=entry["code"]),
            dbc.Textarea(id={"type": "dynamic-input", "index": entry["code"]}, persistence=PERSISTENCE),
            dbc.FormText("Empty: {default}".format(default=entry["default_type"])),
            html.Div(id={"type": "dynamic-output", "index": entry["code"]}, style={'whiteSpace': 'pre-line'}),
            html.Br(),

        ],
        className="mb-3",
    )


def create_radio_button(entry):
    splitted = entry["notation"].split(" / ")
    return html.Div(
        [
            html.Br(),
            dbc.Label(entry["message"], html_for=entry["code"]),
            dbc.RadioItems(
                id={"type": "temp", "index": entry["code"]},
                options=[
                    {
                        "label": splitted[0],
                        "value": True,
                        "label_id": "label-positive" if "positive" in splitted[0] else "label-negative",
                    },
                    {
                        "label": splitted[1],
                        "value": False,
                        "label_id": "label-positive" if "positive" in splitted[1] else "label-negative",
                    },
                ],
                value=False,
                inline=True,
            ),
            html.Br(),
        ],
    )


def create_paragraph(entry):
    return html.Div(
        [
            html.Br(),
            html.P(entry["message"]),
            html.Br(),
        ]
    )


def create_heading(entry, heading_type):
    return html.Div(
        [
            html.Br(),
            heading_type(entry["message"]),
            html.Br(),
        ]
    )


def generate_layout_html():
    return html.Div(
        [
            dcc.Store(id="memory"),
            dcc.Store(id="output-js"),
            html.Div(id="container", children=[]),
            html.Br(),
            dbc.Button("Submit", id="submit-form", n_clicks=0),
            html.Br(),
            html.Div(id="output"),
        ]
    )


def get_auto_close_callback_old():
    return """
   function placeholder(n_clicks) {
       if(n_clicks > 0) {
           console.log(n_clicks);
           setTimeout(function(){
               window.close();
           }, 4000);
           return null;

       }
       return null;

   }

   """

def get_auto_close_callback():
    return """
   function close_window() {
       console.log("close window: " + response);
       setTimeout(function(){
           window.close();
       }, 5000);
       return "worked";
   }
   """
