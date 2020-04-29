#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import json
import datetime as dt

import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots

pio.templates.default = "plotly_white"


def plotly_graph(df, x_cname, y_cnames):

    x = df[x_cname]

    # create traces
    fig = go.Figure()

    for y in y_cnames:
        fig.add_trace(
            go.Scatter(
                x=df[x_cname],
                y=df[y],
                # fill="tonexty",
                mode="lines+markers",
                # line_color="lightgrey",
                showlegend=True,
                name=y,
                line=dict(width=2, shape="hv"),
                marker=dict(size=5,),
            )
        )

    fig.show()


def plotly_graph_dual_axis(df, x_name, y1_name, y2_name):
    """Plot a stepped line chart from two time series with
    dual y axes

    :param df: dataframe containing columns for x and both y axes
    :type df: pd.DataFrame
    :param x_name: name of column in df, which contains x-axis data
    :type x_name: string
    :param y1_name: name of column in df, which contains first y-axis data
    :type y1_name: string
    :param y2_name: name of column in df, which contains second y-axis data
    :type y2_name: string
    """

    # create traces
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    config = dict({"displayModeBar": False, "displaylogo": False,},)

    fig.add_trace(
        go.Scatter(
            x=df[x_name],
            y=df[y2_name],
            fill="tonexty",
            mode="lines+markers",
            # line_color="lightgrey",
            showlegend=True,
            name=y2_name,
            line=dict(
                width=2, shape="hv",
            ),  # [‘linear’, ‘spline’, ‘hv’, ‘vh’, ‘hvh’, ‘vhv’]
            marker=dict(size=5, color="red",),
        ),
        secondary_y=True,
    )

    fig.add_trace(
        go.Scatter(
            x=df[x_name],
            y=df[y1_name],
            fill="tonexty",
            mode="lines+markers",
            # line_color="lightgrey",
            showlegend=True,
            name=y1_name,
            line=dict(
                width=2, shape="hv",
            ),  # [‘linear’, ‘spline’, ‘hv’, ‘vh’, ‘hvh’, ‘vhv’]
            marker=dict(size=5, color="darkgrey",),
        ),
        secondary_y=False,
    )

    # Set y-axes titles
    fig.update_yaxes(title_text=y1_name, secondary_y=False)
    fig.update_yaxes(title_text=y2_name, secondary_y=True)

    fig.update_layout(
        shapes=[
            # 1st measures implemented in Feb 28
            dict(
                type="rect",
                # x-reference is assigned to the x-values
                xref="x",
                # y-reference is assigned to the plot paper [0,1]
                yref="paper",
                x0="2020-03-16",
                y0=0,
                x1="2020-04-20",
                y1=1,
                fillcolor="lightgrey",
                opacity=0.5,
                layer="below",
                line_width=0,
            ),
            # 2nd wave of measures implemented in Mar 16
            dict(
                type="rect",
                xref="x",
                yref="paper",
                x0="2020-04-20",
                y0=0,
                x1=dt.date.today().strftime("%Y-%m-%d"),
                y1=1,
                fillcolor="whitesmoke",
                opacity=0.5,
                layer="below",
                line_width=0,
            ),
        ]
    )

    fig.show(config=config, )
    #fig.write_html(f"images/plot_{y1_name}_vs_{y2_name}.html")
