import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output,Input
import json
import plotly.express as px 

location="/Blobs/data/sensitivity-analysis/seq_proj_dir/merged_input_data/merged_rms.csv"

df=pd.read_csv(location)
external_sheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
print(df.head())
app=dash.Dash(__name__,external_stylesheets=external_sheets)
app.layout=html.Div([ 
    
    dcc.Graph(id="graph"),
    dcc.Dropdown(
            id='dropdown',
            options=[{'label':i,'value':i} for i in [8.5,12.5,16.5]]
        ),

    html.Div(id='hidden_div')
])

@app.callback(
    Output('hidden_div','children'),
    Input('dropdown','value')
)
def group_data_by(offset_bin_size):
    grouped_data=df.assign(
        offset_bin=lambda x:np.floor(x['offset']/offset_bin_size)
        ).groupby('offset_bin')['cdpx'].apply(np.mean)

    grouped_df=pd.DataFrame(grouped_data)
    return grouped_df.to_json()


@app.callback(
        Output('graph','figure'),
        Input('hidden_div','children')
    )
def update_figure(v):
    gdf=pd.read_json(v)
    fig=px.scatter(gdf,x=gdf.index,y='cdpx')
    return fig


if __name__=='__main__':
    app.run_server(debug=True)