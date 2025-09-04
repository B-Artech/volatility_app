import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output, State, dash_table, no_update
import dash_bootstrap_components as dbc
from datetime import date
from plotly.subplots import make_subplots
from close_layout import close_return_output
from high_low_layout import high_low_return_output
from o_c_layout import open_close_return_output
from close_util import close_return_calc
from h_l_util import h_l_return_calc
from o_c_util import o_c_return_calc

# Initialize the Dash app
app = Dash(external_stylesheets=[dbc.themes.SUPERHERO])
server = app.server
# --- App Layout ---
app.layout = html.Div(
    style={'fontFamily': 'Arial, sans-serif', 
           'width':'100%',
           'maxHeigh':'100%', 
           'margin': 'auto', 
           'padding': '20px', 
           'backgroundColor': "#0f2537"},
    children=[
        
    # Header
    html.H1(
        children='Daily Return Distribution and Statistics (Indices-Stocks-FX-Rates-Commodities-Crypto)',
        style={'textAlign': 'center', 
               'fontSize':'20px', 
               'color': '#e7e8e6ff',
               'marginBottom': '20px',
              }
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
            start_date="2018-01-01",
            end_date="2025-08-30",
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
        style={'textAlign': 'left', 'marginTop': '20px','marginBottom': '40px', 'paddingLeft': 'inherit', 'fontSize': '1.2em' , 'color': "#d7f93eff"}),
    
    html.Div([
    close_return_output(),
    high_low_return_output(),
    open_close_return_output(),
    
    ], style={'display':'flex', 'justifyContent':'space-evenly', 'flexWrap':'wrap'})

])


# --- Callback to connect inputs to outputs ---
@app.callback(
    [Output('close-histogram', 'figure'),
     Output('high_low', 'figure'),
     Output('open_close', 'figure'),
     Output('close_stats-table', 'data'),
     Output('close_stats-table', 'columns'),
     Output('close_std-table', 'data'),
     Output('close_std-table', 'columns'),
     Output('h_l_stats-table', 'data'),
     Output('h_l_stats-table', 'columns'),
     Output('h_l_std-table', 'data'),
     Output('h_l_std-table', 'columns'),
     Output('o_c_stats-table', 'data'),
     Output('o_c_stats-table', 'columns'),
     Output('o_c_std-table', 'data'),
     Output('o_c_std-table', 'columns'),
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
     return go.Figure(), go.Figure(),go.Figure(), [],[],[],[],[],[]

    try:
        # Download stock data using yfinance
        data = yf.download(ticker_symbol, start=start_date, end=end_date, interval="1d")

        if data.empty:
            return go.Figure(),go.Figure(),go.Figure(), f"No data found for symbol '{ticker_symbol}'. Please check the ticker."
        
       
        # Close Return Module Import
        returns, close_stats_data, close_stats_columns, close_std_data, close_std_columns = close_return_calc(data)
        h_l_result = h_l_return_calc(data)
        o_c_result = o_c_return_calc(data)
        
        
        
        # Calculate Cumulative Return
        first_price = data['Close'].iloc[0].item()
        last_price = data['Close'].iloc[-1].item()
        cumulative_return = ((last_price / first_price) - 1) * 100
        cumulative_return_text = f"{ticker_symbol.upper()} Total Return : {cumulative_return:.2f}%"
      
       # Close fig
        close_fig = go.Figure()
        close_fig.add_trace(go.Histogram(
            x=returns * 100,
            marker_color='#007BFF',
            opacity=0.8,
            xbins=dict(start=-12, end=12, size=0.5),
            name="Daily Log Returns"
        ))
        close_fig.update_layout(
            template='plotly_white',
            bargap=0.05,
            margin=dict(l=20, r=20, t=30, b=20),
            xaxis=dict(dtick=2)
            ) 

        # High to Low fig
        h_l_fig = go.Figure()
        h_l_fig.add_trace(go.Histogram(
            x=h_l_result['h_l']*100,
            marker_color="#00FF59",
            opacity=0.8,
            xbins=dict(start=0, end=20, size=1),
            name="High Low"
        ))
        h_l_fig.update_layout(
            template='plotly_dark',
            bargap=0.05,
            margin=dict(l=20, r=20, t=30, b=20)
            )
        # Open to Close fig
        o_c_fig = go.Figure()
        o_c_fig.add_trace(go.Histogram(
            x=o_c_result['o_c']*100,
            marker_color="#00FF59",
            opacity=0.8,
            xbins=dict(start=-12, end=12, size=0.5),
            name="Open Close"
        ))
        o_c_fig.update_layout(
            template='plotly_dark',
            bargap=0.05,
            margin=dict(l=20, r=20, t=30, b=20),
            xaxis=dict(dtick=2)
            )
        

        return (close_fig, h_l_fig, o_c_fig,
                close_stats_data, close_stats_columns, close_std_data, close_std_columns,
                h_l_result['h_l_stats_data'],h_l_result['h_l_stats_columns'], h_l_result['h_l_std_data'],h_l_result['h_l_std_columns'],
                o_c_result['o_c_stats_data'],o_c_result['o_c_stats_columns'], o_c_result['o_c_std_data'],o_c_result['o_c_std_columns'],
                cumulative_return_text)
               
    except Exception as e:
        #error handling
        error_message = f"An error occurred: {e}"
        return go.Figure(),go.Figure(), go.Figure(), f"{error_message}: {e}"

# --- Run application ---
if __name__ == '__main__':
    app.run(debug=True)
