import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import numpy as np
from dash.dependencies import Input,Output

location="/Blobs/data/sensitivity-analysis/seq_proj_dir/merged_input_data/merged_rms.csv"

df=pd.read_csv(location)
print(df.head())

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# fig = px.bar(df, x="", y="", color="", barmode="group")


app.layout = html.Div(children=[
    html.H1(children='Slider Callback'),

    html.Div(children='''
       
    '''),

    dcc.Graph(
        id='streamer-graph',
        
    ),

    dcc.Slider(
        id='cable-slider',
        min=df['grnofr'].min(),
        max=df['grnofr'].max(),
        value=df['grnofr'].min(),
        marks={str(cable):str(cable) for cable in df['grnofr'].unique()},
        step=None
        )

])


@app.callback(
    Output('streamer-graph','figure'),
    Input('cable-slider','value'),
)
def update_figure_layout(slider_cable_value):
    filtered_df=df[df['grnofr']==slider_cable_value]
    fig=px.line(filtered_df,x='stas',y='cdpx')
    fig.update_layout(transition_duration=500)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)