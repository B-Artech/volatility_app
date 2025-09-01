from dash import Dash, html, dcc, Input, Output, State, dash_table, no_update

# Close Return module

def open_close_return_output():
    return html.Div(
        # Row with two graphs
        html.Div([
            html.Div([
                html.H2(children='Open to Close Daily Return',
                        style={'textAlign': 'center', 'fontSize':'18px', 'color': "#f9ec3eff"}),
                dcc.Graph(
                    id='open_close',
                    style={'width': '450px', 'height': '400px'}
            )
            ]),
            # Statistics Table Close Return
            html.H2(children='Return Statistics',
                    style={'textAlign': 'center', 'fontSize':'18px', 'color': "#f9ec3eff", 'marginTop':'5px'}),
            dash_table.DataTable(
                id='o_c_stats-table',
                columns=[
                    {"name": " ", "id": "Label"},
                    {"name": "Mean", "id": "Mean"},
                    {"name": "Count", "id": "Count"},
                    {"name": "Frequency %", "id": "Frequency %"},
                    {"name": "Adj Return", "id": "Adj Return"},
                ],
                data=[
                    {"Label": "Positive", "Mean": "", "Count": "", "Frequency %": "", "Adj Return": ""},
                    {"Label": "Negative", "Mean": "", "Count": "", "Frequency %": "", "Adj Return": ""},
                ],
                style_table={'marginTop': '1px'},
                style_cell={'textAlign': 'center', 'padding': '8px','backgroundColor': "#20374c", 'color': "#FAF25A",'fontSize':'15px'},
                style_header={'backgroundColor': "#0f2537", 'color': "#ff933b", 'fontWeight': 'bold'}
            ),
            # Standard Deviation Table Close Return
            html.H2(children='σ-Levels',
                    style={'textAlign': 'center','marginTop': '10px', 'fontSize':'18px', 'color': "#f9ec3eff"}),
            dash_table.DataTable(
                id='o_c_std-table',
                columns = [
                    {"name": "", "id": "label"},
                    {"name": "Upper Bound", "id": "Upper Bound"},
                    {"name": "Lower Bound", "id": "Lower Bound"},
                    {"name": "Count", "id": "Count"},
                    {"name": "Count %", "id": "Count %"},
                ],
                data=[
                    {"label": "Std_1","Upper Bound":"", "Lower Bound":"","Count":"","Count %":""},
                    {"label": "Std_2","Upper Bound":"", "Lower Bound":"","Count":"","Count %":""},
                    {"label": "Std_3","Upper Bound":"", "Lower Bound":"","Count":"","Count %":""},
                    
                ],
                style_table={'marginTop': '1px', 'width': '45%'},
                style_cell={'textAlign': 'center', 'padding': '8px','backgroundColor': '#20374c','color': "#FAF25A",'fontSize':'15px'},
                style_header={'backgroundColor': "#0f2537", 'color': "#ff933b", 'fontWeight': 'bold'}
                    )
            ], style={'display':'flex', 'flexDirection':'column','alignItems':'center'})
    )