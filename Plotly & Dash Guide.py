import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
# Generate sample sales data
np.random.seed(42)
dates = pd.date_range('2023-01-01', periods=365, freq='D') 
df_sales = pd.DataFrame({
'date': dates,
'sales': np.random.randint(1000, 5000, 365),
'product': np.random.choice(['A', 'B', 'C', 'D'], 365),
'region': np.random.choice(['North', 'South', 'East', 'West'], 365)
})
# Initialize the app
app = dash.Dash(__name__)
# Define the layout
app.layout = html.Div([
html.H1("Sales Dashboard",
style={'textAlign': 'center', 'marginBottom': 30}),
# Controls row
html.Div([
html.Div([
html.Label("Select Product:"),
dcc.Dropdown(
id='product-dropdown',
options=[{'label': prod, 'value': prod}
for prod in df_sales['product'].unique()],
value=df_sales['product'].unique()[0]
)
], style={'width': '48%', 'display': 'inline-block'}),
html.Div([
html.Label("Select Region:"),
dcc.Dropdown(
id='region-dropdown',
options=[{'label': region, 'value': region}
for region in df_sales['region'].unique()],
value=df_sales['region'].unique()[0]
)
], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
]),
# Charts row
html.Div([
dcc.Graph(id='time-series-chart'),
dcc.Graph(id='bar-chart')
], style={'marginTop': 30})
])
# Callback for time series chart
@app.callback(
Output('time-series-chart', 'figure'),
[Input('product-dropdown', 'value'),
Input('region-dropdown', 'value')]
)
def update_time_series(selected_product, selected_region):
    filtered_df = df_sales[
    (df_sales['product'] == selected_product) &
    (df_sales['region'] == selected_region)
    ]
    fig = px.line(filtered_df, x='date', y='sales',
    title=f'Sales Trend - {selected_product} in {selected_region}')
    return fig
# Callback for bar chart
@app.callback(
Output('bar-chart', 'figure'),
[Input('product-dropdown', 'value')]
)
def update_bar_chart(selected_product):
    filtered_df = df_sales[df_sales['product'] == selected_product]
    region_sales = filtered_df.groupby('region')['sales'].sum().reset_index()

    fig = px.bar(region_sales, x='region', y='sales',
    title=f'Total Sales by Region - Product {selected_product}')
    return fig
# Run the app
if __name__ == '__main__':
    app.run(debug=True)