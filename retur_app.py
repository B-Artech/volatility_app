import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output, State, dash_table, no_update
import dash_bootstrap_components as dbc
from datetime import date
from plotly.subplots import make_subplots

# Initialize the Dash app
app = Dash(external_stylesheets=[dbc.themes.SUPERHERO])
server = app.server

# --- App Layout ---
app.layout = html.Div(
    style={'fontFamily': 'Arial, sans-serif', 
           'width':'100%',
           'minHeigh':'100%', 
           'margin': 'auto', 
           'padding': '20px', 
           'backgroundColor': "#0f2537"},
    children=[
        
    # Header
    html.H1(
        children='Stock Daily Return Distribution',
        style={'textAlign': 'center', 
               'fontSize':'20px', 
               'color': "#e7e8e6ff"}
    ),  

    html.Div(style={'display': 'flex', 
                    'alignItems': 'center', 
                    'justifyContent': 'space-between', 
                    'padding': '10px', 
                    'width':'600px',
                    'heigh':'100%', 
                    'backgroundColor': "#20374c", 
                    'borderRadius': '3px', 
                    'marginBottom':'10px'}, 
             
             children=[
        # Ticker Symbol Input
        dcc.Input(
            id='stock-ticker-input',
            type='text',
            value='Ticker',  # Default value
            style={'padding': '10px 15px', 
                   'fontSize': '18px', 
                   'border':'none', 
                   'borderRadius': '3px',
                   'width':'150px'}
        ),

        # Date Range Picker
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date="2020-04-10",
            end_date="2025-08-26",
            display_format='YYYY-MM-DD',
            style={'fontSize': '10px', 'borderRadius': '3px'}
        ),

        # Submit Button
        html.Button('FIND', id='submit-button', n_clicks=0, style={
            'backgroundColor': "#df6919",
            'color': 'white',
            'border': 'none',
            'padding': '10px 15px',
            'borderRadius': '3px',
            'cursor': 'pointer',
            'fontSize': '15px'
        }),
        
    ]),
    # Symbol Return Output 
    html.Div(id='cumulative-return-output',
        style={'textAlign': 'left', 'marginTop': '20px', 'paddingLeft': 'inherit', 'fontSize': '1.2em' , 'color': "#d7f93eff"}),
    

    # Row with two graphs
    html.Div([
        html.Div([
            html.Div([
            html.H2(children='Log Close Daily Histogram',
                    style={'textAlign': 'center', 'fontSize':'20px', 'color': "#f9ec3eff"}),
            dcc.Graph(
                id='return-histogram',
                style={'width': '500px', 'height': '400px'}
            )
            ]),
            html.Div([
                html.H2(children='High to Low Daily Histogram',
                        style={'textAlign': 'center', 'fontSize':'20px', 'color': "#f9ec3eff"}),
                dcc.Graph(
                    id='close',
                    style={'width': '500px', 'height': '400px', 'marginLeft': '10px'}
                )
            ])
            
        ], style={'display':'flex','flex-wrap':'wrap','width': 'auto'}),

        # Tables 
        html.Div([
            # Statistics Table
            html.H2(children='Daily Return Statistics',
                    style={'textAlign': 'center', 'fontSize':'20px', 'color': "#f9ec3eff"}),
            dash_table.DataTable(
                id='stats-table',
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
                style_table={'marginTop': '0px', 'marginLeft': '10px'},
                style_cell={'textAlign': 'center', 'padding': '5px','backgroundColor': "#20374c", 'color': "#FAF25A"},
                style_header={'backgroundColor': "#0f2537", 'color': "#ff933b", 'fontWeight': 'bold'}
            ),
            # Standard Deviation Table
            html.H2(children='Daily Realize Volatility Levels',
                    style={'textAlign': 'center','marginTop': '10px', 'fontSize':'20px', 'color': "#f9ec3eff"}),
            dash_table.DataTable(
                id='std-table',
                columns = [
                    {"name": "", "id": "label"},
                    {"name": "Upper Bound", "id": "Upper Bound"},
                    {"name": "Lower Bound", "id": "Lower Bound"}
                ],
                data=[
                    {"label": "Std_Dev_1","Upper Bound":"", "Lower Bound":""},
                    {"label": "Std_Dev_2","Upper Bound":"", "Lower Bound":""},
                    {"label": "Std_Dev_3","Upper Bound":"", "Lower Bound":""},
                  
                ],
                style_table={'marginTop': '10px', 'width': '45%','marginLeft': '10px'},
                style_cell={'textAlign': 'center', 'padding': '10px','backgroundColor': '#20374c','color': "#FAF25A"},
                style_header={'backgroundColor': "#0f2537", 'color': "#ff933b", 'fontWeight': 'bold'}
                    )
        ])
    ], style={'display':'flex', 'flex-wrap':'wrap','width': '100%'})
])

# --- Callback to connect inputs to outputs ---
@app.callback(
    [Output('return-histogram', 'figure'),
     Output('close', 'figure'),
     Output('stats-table', 'data'),
     Output('stats-table', 'columns'),
     Output('std-table', 'data'),
     Output('std-table', 'columns'),
     Output('cumulative-return-output', 'children')],
    [Input('submit-button', 'n_clicks')],
    [State('stock-ticker-input', 'value'),
     State('date-picker-range', 'start_date'),
     State('date-picker-range', 'end_date')]
)


# --- Main Functions ---
def update_graph(n_clicks, ticker_symbol, start_date, end_date):
    """
    This function is triggered when the find button is clicked.
    It downloads stock data, calculates returns, and creates a histogram.
    """
    # Prevent the callback from firing on initial load
    if n_clicks == 0:
     return go.Figure(), go.Figure(),[],[]


    try:
        # Download stock data using yfinance
        data = yf.download(ticker_symbol, start=start_date, end=end_date, interval="1d")

        if data.empty:
            return go.Figure(),go.Figure(), f"No data found for symbol '{ticker_symbol}'. Please check the ticker."
        
        # Get Symbol information's 
        # volume_Last = ticker_symbol.info.get("volume", None)
        # volume_10Day_Average = ticker_symbol.info.get("averageDailyVolume10Day", None)
        # volume_3Month_Average = ticker_symbol.info.get("averageDailyVolume3Month", None)
        
        # Calculate logarithmic returns
        data['Returns'] = np.log(data['Close'] / data["Close"].shift(1))
        data['h_l'] = (data['High'] / data["Low"] - 1)
        log_returns = data['Returns'].dropna()
        
        # Stats
        avg_ret = log_returns.mean()
        std = log_returns.std()
        
        total_count = log_returns.count() # total count of all data points
        
        pos_count = (log_returns > 0).sum() # positive data
        neg_count = (log_returns < 0).sum()
        
        pos_perc = (pos_count / total_count) *100
        neg_perc = (neg_count / total_count) *100
        
        d_pos_mean = data.loc[data['Returns']> 0, 'Returns'].mean()
        d_neg_mean = data.loc[data['Returns']< 0, 'Returns'].mean()
        
        pos_adj_freq = d_pos_mean * pos_perc
        neg_adj_freq = d_neg_mean * neg_perc
        
        # Standard Deviation Calculations
        
        upper1 = (avg_ret + 1 * std)
        lower1 = (avg_ret - 1 * std)

        upper2 = (avg_ret + 2 * std)
        lower2 = (avg_ret - 2 * std)

        upper3 = (avg_ret + 3 * std)
        lower3 = (avg_ret - 3 * std)
        
         # Table 1 data
        stats_data = [
             # Positive Label
            {"Label": "Positive",
             "Mean": f"{d_pos_mean:.2%}",
             "Count": pos_count,
             "Frequency %": f"{pos_perc:.2f}%",
             "Adj Return": f"{pos_adj_freq:.2f}%"},
            
            # Negative Label
            {"Label": "Negative",
             "Mean": f"{d_neg_mean:.2%}",
             "Count": neg_count,
             "Frequency %": f"{neg_perc:.2f}%",
             "Adj Return": f"{neg_adj_freq:.2f}%"},
            ]
        
        stats_columns = [
            {"name": "", "id": "Label"},
            {"name": "Mean", "id": "Mean"},
            {"name": "Count", "id": "Count"},
            {"name": "Frequency %", "id": "Frequency %"},
            {"name": "Adj Return", "id": "Adj Return"}
            ]
        
       # Table 2 data
        std_data = [
            # Positive Label
            {"Label": "Std_Dev_1", "Upper Bound": f"{upper1:.2%}", "Lower Bound": f"{lower1:.2%}"},
            {"Label": "Std_Dev_2", "Upper Bound": f"{upper2:.2%}", "Lower Bound": f"{lower2:.2%}"},
            {"Label": "Std_Dev_3", "Upper Bound": f"{upper3:.2%}", "Lower Bound": f"{lower3:.2%}"},
        ]

        std_columns = [
            {"name": "", "id": "Label"},
            {"name": "Upper Bound", "id": "Upper Bound"},
            {"name": "Lower Bound", "id": "Lower Bound"},
        ]
       
        # Calculate Cumulative Return
        first_price = data['Close'].iloc[0]
        last_price = data['Close'].iloc[-1]
        cumulative_return = float(((last_price / first_price) - 1) * 100)
        cumulative_return_text = f"{ticker_symbol.upper()} Total Return : {cumulative_return:.2f}%"

        # Prepare data for histogram (convert to percentage and drop NAs)
        log_returns_percent = data['Returns'] *100
        h_l = data['h_l'] *100

       # Histogram fig
        hist_fig = go.Figure()
        hist_fig.add_trace(go.Histogram(
            x=log_returns_percent,
            marker_color='#007BFF',
            opacity=0.8,
            xbins=dict(start=-10, end=10, size=0.4),
            name="Daily Log Returns"
        ))
        hist_fig.update_layout(
            template='plotly_white',
            bargap=0.05,
            margin=dict(l=40, r=20, t=30, b=40)
            ) 

        # Close fig
        h_l_fig = go.Figure()
        h_l_fig.add_trace(go.Histogram(
            x=h_l,
            marker_color="#00FF59",
            opacity=0.8,
            xbins=dict(start=0, end=20, size=1),
            name="High Low"
        ))
        h_l_fig.update_layout(
            template='plotly_dark',
            bargap=0.05,
            margin=dict(l=40, r=20, t=30, b=40)
            )

        return hist_fig, h_l_fig, stats_data, stats_columns, std_data, std_columns, cumulative_return_text

    except Exception as e:
        #error handling
        error_message = f"An error occurred: {e}"
        return go.Figure(), error_message

# --- Run application ---
if __name__ == '__main__':
    app.run(debug=True)
