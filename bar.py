import requests
import json
import numpy as np
import pandas as pd
from datetime import datetime
import re
import plotly.graph_objects as go

pd.options.mode.chained_assignment = None

res = requests.get('https://data.tradeui.com/tui_bt?idT=aa')

res = res.json() # convert to json
res = np.array(res['resultat'])

df = pd.DataFrame.from_dict(pd.json_normalize(res), orient='columns')

df['blocktotal'] = pd.to_numeric(df['blocktotal'])

for i in df.index.values:

    df['ticker'][i] = re.split(':',df['ticker'][i])[2]


df = df.sort_values('blocktotal', ascending=False).drop_duplicates(['ticker'])


df = df.head(15)

df = df.sort_values('blocktotal')

fig = go.Figure()

fig.add_trace(go.Bar(
                x=df['blocktotal'],
                y=df['ticker'],
                showlegend=False,
                marker_color = "rgb(115,181,221)",
                marker_line_color="rgb(115,181,221)",
                marker_line_width=1,
                orientation="h",
                text = df['blocktotal']
             )
)

fig.layout.images = [dict(
        source="https://i.ibb.co/y6PVjyn/logo.png",
        xref="paper", yref="paper",
        x=1.08, y=-0.2,
        sizex=0.1, sizey=0.1,
        xanchor="right", yanchor="bottom"
      )]


layout = go.Layout(
    title_text="Top Darkpool Trades",
    title_x=0.5,
    paper_bgcolor='#141d26',
    plot_bgcolor='#141d26',
    font_family='Monospace',
    font_color='white',
    font_size=32,
    margin=dict(
        l=200,
        r=150,
        t=150,
        b=150,
        pad=20
    ),
    xaxis=dict(title="Amount"),
    uniformtext_minsize=8, uniformtext_mode='hide'
)

fig.update_traces(texttemplate='$%{text:,.0f}', textposition='inside')
fig.update_layout(layout)
fig.update_xaxes(showgrid=False,zeroline=False)
fig.update_yaxes(showgrid=False,zeroline=False)

fig.show()
