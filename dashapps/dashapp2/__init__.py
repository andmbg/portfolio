from flask import Flask
from dash import Dash, dcc, html
from dash.dependencies import Input, Output


def dashapp2_init(flask_app, route):
    dash_app = Dash(server=flask_app, routes_pathname_prefix=route)

    dash_app.layout = html.Div(
        [
            dcc.Input(id="my-input", value="initial value", type="text"),
            html.Div(id="my-output"),
        ]
    )

    @dash_app.callback(
        Output(component_id="my-output", component_property="children"),
        [Input(component_id="my-input", component_property="value")],
    )
    def update_output_div(input_value):
        return 'You\'ve entered "{}"'.format(input_value)

    return dash_app


if __name__ == "__main__":
    flask_app = Flask(__name__)
    dash_app = dashapp2_init(flask_app, "/")
    dash_app.run_server(debug=True)
