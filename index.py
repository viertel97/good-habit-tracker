from dash import dcc, html
from dash.dependencies import Input, Output

from app import app
from components import callbacks  # noqa: F401

from pages import default

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content", children=[]),
    ]
)


# Create the callback to handle mutlipage inputs
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/daily/morning":
        return default.generate_layout()
    if pathname == "/daily/evening":
        return default.generate_layout()
    if pathname == "/weekly":
        return default.generate_layout()
    if pathname == "/monthly":
        return default.generate_layout()
    if pathname == "/quarterly":
        return default.generate_layout()
    if pathname == "/yearly":
        return default.generate_layout()
    else:  # if redirected to unknown link
        return html.Div(
            [
                dcc.Link("Daily - Morning", href="/daily/morning"),
                html.Br(),
                dcc.Link("Daily - Evening", href="/daily/evening"),
                html.Br(),
                html.Br(),
                dcc.Link("Weekly", href="/weekly"),
                html.Br(),
                dcc.Link("Monthly", href="/monthly"),
                html.Br(),
                dcc.Link("Quarterly", href="/quarterly"),
                html.Br(),
                dcc.Link("Yearly", href="/yearly"),
            ]
        )


# Run the app on localhost:8050
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=8050)
