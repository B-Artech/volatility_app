import yfinance as yf
import pandas as pd
import numpy as np
from datetime import date, datetime
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output, State, dash_table, no_update
import dash_bootstrap_components as dbc
from datetime import date, datetime
from plotly.subplots import make_subplots
from close_layout import close_return_output
from high_low_layout import high_low_return_output
from o_c_layout import open_close_return_output
from close_util import close_return_calc
from h_l_util import h_l_return_calc
from o_c_util import o_c_return_calc

# Initialize the Dash app
app = Dash(external_stylesheets=[dbc.themes.SUPERHERO],suppress_callback_exceptions=True)
server = app.server

tab1_content = dbc.Card(
    
    dbc.CardBody(
        [
            # Header
            html.H1(
                children='Return Distribution Dashboard',
                style={'textAlign': 'center',
                    'fontSize':'18px',
                    'color': "#e7e8e6ff"}
            ),
             dcc.RadioItems(
                    id='calculation-mode',
                    options=[
                        {'label': html.Div(['Single'], style={'color': 'Yellow',
                                                                'fontSize': 18,
                                                                'display': 'inline-block',
                                                                'marginLeft': 8}), 'value': 'Single'},
                        
                        {'label': html.Div(['Pair'], style={'color': 'Yellow',
                                                            'fontSize': 18,
                                                            'display': 'inline-block',
                                                            'marginLeft': 8}), 'value': 'Spread'}
                    ],
                    value='Single',
                    style={ 'margin-bottom':'10px'}
                ),

            html.Div(style={'display': 'flex',
                            'alignItems': 'center',
                            'justifyContent': 'space-between',
                            'padding': '10px',
                            'width':'650px',
                            'heigh':'100%',
                            'backgroundColor': "#20374c",
                            'borderRadius': '3px',
                            'margin-bottom':'10px'},
                    
                    children=[
                # Ticker Symbol Input
                dcc.Input(
                    id='stock-ticker-input',
                    type='text',
                    value='Ticker',  # Default value
                    style={'padding': '10px 15px',
                        'fontSize': '15px',
                        'border':'none',
                        'borderRadius': '3px',
                        'width':'80px'}
                ),
                html.Div(
                    id='second-ticker-container',
                    children=[
                        dcc.Input(
                            id='stock-ticker-input-2',
                            type='text',
                            value='(Ticker)',
                            placeholder='Second Ticker',
                            style={
                                'padding': '10px 15px',
                                'fontSize': '15px',
                                'border':'none',
                                'borderRadius': '3px',
                                'width':'82px'
                            }
                        )
                    ],
                    style={'display': 'none'}  # Hidden by default
                ),

                # Date Range Picker
                dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date="2018-01-01",
                    end_date=date.today().isoformat(),
                    display_format='YYYY-MM-DD',
                    style={'border':'none'}
                ),

                # Data interval drop down
                dcc.Dropdown(
                id="interval-dropdown",
                options=[
                    {'label':"Daily", "value":'1d'},
                    {'label':"Weekly", "value":'1wk'},
                    {'label':"Monthly", "value":'1mo'}
                ],
                value='1d', # Default Set
                clearable=False,
                style={
                    'width': '82px',
                    'backgroundColor':"#f7f6c9ff",
                    'color':'black',
                    'borderRadius':'3px',
                    'fontSize':'15px'
                }),
                
                
                # Submit Button
                html.Button('LOAD', id='submit-button', n_clicks=0, style={
                    'backgroundColor': "#df6919",
                    'color': 'white',
                    'border': 'none',
                    'padding': '10px 10px',
                    'borderRadius': '3px',
                    'cursor': 'pointer',
                    'fontSize': '12px'
                }),

            ]),
            # Symbol Return Output 
            html.Div(id='cumulative-return-output',
                style={'textAlign': 'left', 'marginTop': '20px','marginBottom': '40px', 'paddingLeft': 'inherit', 'fontSize': '1.2em' , 'color': "#d7f93eff"}),

            html.Div([
            close_return_output(),
            high_low_return_output(),
            open_close_return_output(),

            ], style={'display':'flex', 'justifyContent':'space-evenly', 'flexWrap':'wrap','backgroundColor': '#0f2537'}),

            dbc.Container([
                dbc.Row(
                    [
                        dbc.Col(html.A(["B-Artech", html.Sup("®"), " | GitHub"], href='https://github.com/B-Artech',
                                                        className="text-secondary p-1 fw-bold text-decoration-none"))
                    ], style={
                                'width': '100%', 'marginTop': '20px', 'textAlign':'center'
                    }
                    )
            ])
        ]
    ),
    style={'backgroundColor': "#0f2537",'border':'1px','padding':'-5px'},
    class_name="mt-3"
)

tab2_content = dbc.Card(
    
    dbc.CardBody(
        [
            html.H1("Rolling Correlation Dashboard",
                style={'textAlign': 'center','fontSize':'18px','color': "#e7e8e6ff"}),
            
            html.Div(style={'display': 'flex', 
                    'alignItems': 'center', 
                    'justifyContent': 'space-between', 
                    'padding': '10px', 
                    'width':'650px',
                    'heigh':'100%', 
                    'backgroundColor': "#20374c", 
                    'borderRadius': '3px', 
                    'marginBottom':'10px'},children=[
            dcc.Input(
                id='ticker1',
                type='text',
                value='AAPL',
                placeholder="Ticker 1",
                style={'padding': '10px 15px',
                        'fontSize': '15px',
                        'border':'none',
                        'borderRadius': '3px',
                        'width':'80px'}
            ),

            dcc.Input(
                id='ticker2',
                type='text',
                value='MSFT',
                placeholder="Ticker 2",
                style={'padding': '10px 15px',
                        'fontSize': '15px',
                        'border':'none',
                        'borderRadius': '3px',
                        'width':'80px'}
            ),

            dcc.DatePickerRange(
                id='date',
                start_date="2022-01-01",
                end_date=date.today().isoformat(),
                display_format='YYYY-MM-DD',
                style={'fontSize': '30px', 'borderRadius': '3px'}
            ),

            dcc.Dropdown(
                id="interval",
                options=[
                    {'label': "Daily", "value": '1d'},
                    {'label': "Weekly", "value": '1wk'},
                    {'label': "Monthly", "value": '1mo'}
                ],
                value='1d',
                clearable=False,
                style={'width': '100px',
                    'backgroundColor':"#f7f6c9ff",
                    'color':'black',
                    'borderRadius':'3px',
                    'fontSize':'18px'}
            ),

            html.Button("Load",
                        id="corr-button",
                        n_clicks=0,
                        style={ 
                    'backgroundColor': "#df6919",
                    'color': 'white',
                    'border': 'none',
                    'padding': '10px 10px',
                    'borderRadius': '3px',
                    'cursor': 'pointer',
                    'fontSize': '15px'})
        ]),

        html.Br(),
        html.Div(
                [
                    html.Label(
                        "Correlation Window",
                        style={"textAlign": "center", "display": "block", "marginBottom": "10px"}
                    ),
                    dcc.Slider(
                        id="window-slider",
                        min=1,
                        max=100,
                        step=1,
                        value=30,
                        marks=None,
                        tooltip={"always_visible": True},
                        updatemode="drag",
                    )
                ],
                style={
                    "width": "40%",
                    "margin": "30px auto"
                }
        ),
       

        html.Br(),

        html.Div(
            dcc.Graph(
                id="correlation-chart",
                style={"height": "500px"}
                ),
                style={
                    "width": "50%",
                    "margin": "auto"
                    })
        ]
        
    ),
    style={'backgroundColor': '#0f2537'},
    class_name="mt-3"
)

tab3_content = dbc.Card(
    
    dbc.CardBody(
        [
            html.P("Coming soon...")
        ]
        
    ),
    class_name="mt-3"
),

tab4_content = dbc.Card(
    
    dbc.CardBody(
        [
            html.P("Coming soon...")
        ]
        
    ),
    class_name="mt-3"
),

tab5_content = dbc.Card(
    
    dbc.CardBody(
        [
            html.P("Coming soon...")
        ]
        
    ),
    class_name="mt-3"
),

tab6_content = dbc.Card(
    
    dbc.CardBody(
        [
            html.P("Coming soon...")
        ]
        
    ),
    class_name="mt-3"
),

app.layout = html.Div(
    style={'fontFamily': 'Arial, sans-serif', 
           'width':'100%',
           'heigh':'100vh',
           'margin': 'auto',
           'padding': '20px',
           'backgroundColor': "#0f2537"},
    children=[
        
        dbc.Tabs(
            [
                dbc.Tab(tab1_content, label="Return"),
                dbc.Tab(tab2_content, label="Correlation"),
                dbc.Tab(tab3_content, label="Rolling_Return"),
                dbc.Tab(tab4_content, label="ATR"),
                dbc.Tab(tab5_content, label="Z_Score"),
                dbc.Tab(tab6_content, label="Options_Flow"),
            ]
        )
    ]
)


# --- Toggle Callback ---
@app.callback(
    Output('second-ticker-container', 'style'),
    Input('calculation-mode', 'value')
)
# --- Toggle Function ---
def toggle_second_ticker(mode):
    if mode == 'Spread':
        return {
            'display': 'block',
            'marginLeft': '10px'
        }
    return {'display': 'none'}
# --- Return Tab Callback ---
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
     State('stock-ticker-input-2', 'value'),  # NEW
     State('calculation-mode', 'value'), # NEW
     State('date-picker-range', 'start_date'),
     State('date-picker-range', 'end_date'),
     State('interval-dropdown','value')]
)

# --- Return Function ---
def update_graph(n_clicks, ticker_symbol, ticker_symbol_2, mode,
                 start_date, end_date, interval):
    """
    This function is triggered when the find button is clicked.
    It downloads stock data, calculates returns, and creates a histogram.
    """
    # Prevent the callback from firing on initial load
    if n_clicks == 0:
     return go.Figure(), go.Figure(),go.Figure(), [],[],[],[],[],[]

    try:
        # Download stock data using yfinance
        data1 = yf.download(ticker_symbol, start=start_date,
                    end=end_date, interval=interval)
        
        if isinstance(data1.columns, pd.MultiIndex):
            data1.columns = data1.columns.get_level_values(0)

        if mode == "Spread":

            if not ticker_symbol_2:
                raise ValueError("Second ticker required")

            data2 = yf.download(
                ticker_symbol_2,
                start=start_date,
                end=end_date,
                interval=interval
            )

            if isinstance(data2.columns, pd.MultiIndex):
                data2.columns = data2.columns.get_level_values(0)

            data = pd.merge(
                data1[['Open','High','Low','Close']],
                data2[['Open','High','Low','Close']],
                left_index=True,
                right_index=True,
                suffixes=('', '_2')
            )

            if data.empty:
                raise ValueError("No overlapping dates between tickers")

            # Ratio spread
            data['Close'] = data['Close'] / data['Close_2']
            data['Open']  = data['Open']  / data['Open_2']
            data['High']  = data['High']  / data['High_2']
            data['Low']   = data['Low']   / data['Low_2']

            data = data[['Open','High','Low','Close']]

            data.replace([np.inf, -np.inf], np.nan, inplace=True)
            data.dropna(inplace=True)
        else:
            data = data1

        if data.empty:
            return go.Figure(),go.Figure(),go.Figure(), f"No data found for symbol '{ticker_symbol}'. Please check the ticker."
        
        # Close Return Module Import
        returns, close_stats_data, close_stats_columns, close_std_data, close_std_columns = close_return_calc(data)
        h_l_result = h_l_return_calc(data)
        o_c_result = o_c_return_calc(data)
        
        # Calculate Cumulative Return
        first_price = data['Close'].iloc[0].item()
        last_price = data['Close'].iloc[-1].item()
        first_date = data.index[0]
        last_date = data.index[-1]
        years = (last_date - first_date).days / 365
        cumulative_return = ((last_price / first_price) - 1) * 100
        cumulative_return_text = f"{ticker_symbol.upper()} Range Return: {cumulative_return:.2f}% " f"({years:.2f}Yr)"
        
        if mode == "Spread":
            cumulative_return_text = (
                f"Spread: {ticker_symbol.upper()} - "
                f"{ticker_symbol_2.upper()} | "
                f"Return: {cumulative_return:.2f}% ({years:.2f}Yr)"
            )
        else:
            cumulative_return_text = (
                f"{ticker_symbol.upper()} Range Return: "
                f"{cumulative_return:.2f}% ({years:.2f}Yr)"
            )
        
      
       # Close fig
        close_fig = go.Figure()
        close_fig.add_trace(go.Histogram(
            x=returns * 100,
            marker_color='#007BFF',
            opacity=0.8,
            # xbins=dict(start=-12, end=12, size=0.5),
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
            # xbins=dict(start=0, end=20, size=1),
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
            # xbins=dict(start=-12, end=12, size=0.5),
            name="Open Close"
        ))
        o_c_fig.update_layout(
            template='plotly_dark',
            bargap=0.05,
            margin=dict(l=20, r=20, t=30, b=20),
            xaxis=dict(dtick=2)
            )
        
        return (close_fig, h_l_fig, o_c_fig,
                close_stats_data, 
                close_stats_columns, 
                close_std_data, 
                close_std_columns,
                h_l_result['h_l_stats_data'],
                h_l_result['h_l_stats_columns'], 
                h_l_result['h_l_std_data'],
                h_l_result['h_l_std_columns'],
                o_c_result['o_c_stats_data'],
                o_c_result['o_c_stats_columns'], 
                o_c_result['o_c_std_data'],
                o_c_result['o_c_std_columns'],
                cumulative_return_text)
               
    except Exception as e:
        #error handling
        error_message = f"An error occurred: {e}"
        return go.Figure(),go.Figure(), go.Figure(), f"{error_message}: {e}"
    
# --- Correlation Callback ---
@app.callback(
    Output("correlation-chart", "figure"),
    Input("corr-button", "n_clicks"),
    Input("window-slider", "value"),
    State("ticker1", "value"),
    State("ticker2", "value"),
    State("date", "start_date"),
    State("date", "end_date"),
    State("interval", "value"),
)

# --- Correl Function ---
def update_correlation(n_clicks, window, ticker1, ticker2, start, end, interval):

    if n_clicks == 0:
        return go.Figure()

    try:
        # Download both tickers
        data = yf.download(
            [ticker1, ticker2],
            start=start,
            end=end,
            interval=interval
        )["Close"]

        data = data.dropna()

        # Log returns
        returns = np.log(data / data.shift(1)).dropna()

        # Rolling correlation
        rolling_corr = returns[ticker1].rolling(window).corr(returns[ticker2])

        current_corr = rolling_corr.iloc[-1]
        
        # Price Ration
        price_ratio = (data[ticker1] / data[ticker2]).loc[rolling_corr.index]

        # Build figure
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=rolling_corr.index,
            y=rolling_corr,
            mode="lines",
            name=f"{window}-Period Rolling Correlation",
            line=dict(width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=price_ratio.index,
            y=price_ratio,
            mode="lines",
            name=f"{ticker1}/{ticker2} Price Ratio",
            yaxis="y2",
            line=dict(width=2, dash="dot")
        ))


        fig.add_hline(y=0, line_dash="dash")

       
        fig.update_layout(
            template="plotly_dark",
            title=f"{ticker1.upper()} vs {ticker2.upper()} | Rolling Correlation & Price Ratio",
            yaxis=dict(
                title="Rolling Correlation",
                range=[-1, 1]
            ),
            yaxis2=dict(
                title="Price Ratio",
                overlaying="y",
                side="right",
                showgrid=False
            ),
            legend=dict(x=0.01, y=0.99),
            annotations=[
                dict(
                    x=rolling_corr.index[-1],
                    y=current_corr,
                    text=f"Current Corr: {current_corr:.2f}",
                    showarrow=True
                )
            ]
        )

        return fig

    except Exception as e:
        fig = go.Figure()
        fig.update_layout(
            template="plotly_dark",
            title=f"Error: {e}"
        )
        return fig
    
# --- Interval Callback ---
@app.callback(
    Output("close-title", "children"),
    Output("high-low-title", "children"),
    Output("open-close-title", "children"),
    Input("interval-dropdown", "value")
)

# --- Interval Update Function ---
def update_close_title(interval):
    interval_map = {
        "1d": "Daily",
        "1wk": "Weekly",
        "1mo": "Monthly"
    }
    lable = interval_map.get(interval, interval)

    return(
        f"Close Return ({lable})",
        f"High to Low Return ({lable})",
        f"Open to Close Return ({lable})"
           )
# --- Run application ---
if __name__ == '__main__':
    app.run(debug=True)
