import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

location="/Blobs/data/sensitivity-analysis/seq_proj_dir/merged_input_data/merged_rms.csv"

df=pd.read_csv(location)
print(df.head())

import numpy as np
offset_bin_size=12.5
df=df.assign(offset_bin=lambda x:np.floor(x['offset']/offset_bin_size))

ddf=pd.DataFrame(df.groupby('offset_bin')['cdpx','gelev'].apply(np.mean))


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# fig = px.bar(df, x="", y="", color="", barmode="group")
fig=px.line(ddf,x=ddf.index,y="cdpx")
fig_elev=px.line(ddf,x=ddf.index,y='gelev')


app.layout = html.Div(children=[
    html.H1(children='Sensitivity Dash'),

    html.Div(children='''
       
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),

    dcc.Graph(
        id='elev-graph',
        figure=fig_elev
    )

])

if __name__ == '__main__':
    app.run_server(debug=True)