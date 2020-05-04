#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import json
import datetime as dt
from pathlib import Path

import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt

pio.templates.default = "plotly_white"


def plotly_graph(df, x_cname, y_cnames, file_name, save_path):
    """
    Stepped line chart for one or more lines

    :param df: data for x-axis and all y-axis data in separate columns
    :type df: pd.DataFrame
    :param x_cname: name of column for x
    :type x_cname: [type]
    :param y_cnames: [description]
    :type y_cnames: [type]
    :param file_name: [description]
    :type file_name: [type]
    :param save_path: path to directory for exporting html plot
    :type save_path: pathlib.Path object 
    """

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

    (save_path).mkdir(parents=True, exist_ok=True)
    fig.write_html(str(save_path / f"{file_name}.html"))


def plotly_graph_dual_axis(df, x_name, y1_name, y2_name, save_path):
    """
    Stepped line chart plot from two time series with
    dual y-axes

    :param df: dataframe containing columns for x and both y axes data
    :type df: pd.DataFrame
    :param x_name: name of df column with x-axis data
    :type x_name: string
    :param y1_name: name of df column with first y-axis data
    :type y1_name: string
    :param y2_name: name of df column with second y-axis data
    :type y2_name: string
    :param save_path: path to directory for exporting html plot
    :type save_path: pathlib.Path object 
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

    fig.update_layout(showlegend=False,)

    fig.show(config=config,)

    (save_path).mkdir(parents=True, exist_ok=True)
    fig.write_html(str(save_path / f"plot_{y1_name}_vs_{y2_name}.html"))


def multi_yaxis_plot(
    df1, x1, y1, df2, x2, y2, df3, x3, y3, plot_name, filename, save_path,
):
    """
    Stepped line chart plot with 3 y-axes.

    :param df1: data for line 1 x and y
    :type df1: pd.DataFrame
    :param x1: name of df column with line 1 x-axis data
    :type x1: string
    :param y1: name of df column with line 1 y-axis data
    :type y1: string
    :param df2: data for line 2 x and y
    :type df2: pd.DataFrame
    :param x2: name of df column with line 2 x-axis data
    :type x2: string
    :param y2: name of df column with line 2 y-axis data
    :type y2: string
    :param df3: data for line 3 x and y
    :type df3: pd.DataFrame
    :param x3: name of df column with line 2 x-axis data
    :type x3: string
    :param y3: name of df column with line 2 x-axis data
    :type y3: string
    :param plot_name: plot name i.e. plot title
    :type plot_name: string
    :param filename: html file name
    :type filename: string
    :param save_path: path to directory for exporting html plot
    :type save_path: pathlib.Path object
    """

    # create traces
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    config = dict({"displayModeBar": False, "displaylogo": False,},)

    fig.add_trace(
        go.Scatter(
            x=df1[x1],
            y=df1[y1],
            fill="tonexty",
            mode="lines+markers",
            # line_color="lightgrey",
            showlegend=True,
            name=y2,
            line=dict(
                width=2, shape="hv",
            ),  # [‘linear’, ‘spline’, ‘hv’, ‘vh’, ‘hvh’, ‘vhv’]
            marker=dict(size=5, color="darkgrey",),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df2[x2],
            y=df2[y2],
            fill="tonexty",
            mode="lines+markers",
            # line_color="lightgrey",
            showlegend=True,
            name=y2,
            line=dict(
                width=2, shape="hv",
            ),  # [‘linear’, ‘spline’, ‘hv’, ‘vh’, ‘hvh’, ‘vhv’]
            marker=dict(size=5, color="red",),
            yaxis="y2",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df3[x3],
            y=df3[y3],
            # fill="tonexty",
            mode="lines+markers",
            # line_color="lightgrey",
            showlegend=True,
            name=y3,
            line=dict(
                width=2, shape="hv",
            ),  # [‘linear’, ‘spline’, ‘hv’, ‘vh’, ‘hvh’, ‘vhv’]
            marker=dict(size=5, color="black",),
            yaxis="y3",
        )
    )

    # Set y-axes titles
    fig.update_layout(
        xaxis=dict(domain=[0.0, 0.91], showgrid=False),
        yaxis=dict(  # https://plotly.com/python/reference/#layout-yaxis
            title=y1,
            titlefont=dict(color="darkgrey"),
            tickfont=dict(color="darkgrey"),
            side="right",
            showgrid=False,
        ),
        yaxis2=dict(
            title=y2,
            titlefont=dict(color="red"),
            tickfont=dict(color="red"),
            anchor="free",  # "free"
            overlaying="y",
            side="right",
            position=1.0,
            showgrid=False,
        ),
        yaxis3=dict(
            title=y3,
            titlefont=dict(color="black"),
            tickfont=dict(color="black"),
            anchor="x",
            overlaying="y",
            side="left",
            showgrid=False,
            # position=0.2,
        ),
    )

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

    fig.update_layout(
        showlegend=False,
        xaxis_range=["2020-02-15", dt.datetime.now()],
        title=plot_name,
    )

    fig.show(config=config,)

    (save_path).mkdir(parents=True, exist_ok=True)
    fig.write_html(str(save_path / f"{filename}.html"))


def static_dual_axis_plot(df1, x1, y1, df2, x2, y2, filename, save_path):
    """
    Static, stepped line chart with dual axis. 

    :param df1: data for line 1 x and y
    :type df1: pd.DataFrame
    :param x1: name of df column with line 1 x-axis data
    :type x1: string
    :param y1: name of df column with line 1 y-axis data
    :type y1: string
    :param df2: data for line 2 x and y
    :type df2: pd.DataFrame
    :param x2: name of df column with line 2 x-axis data
    :type x2: string
    :param y2: name of df column with line 2 y-axis data
    :type y2: string
    :param plot_name: plot name i.e. plot title
    :type plot_name: string
    :param filename: html file name
    :type filename: string
    :param save_path: path to directory for exporting html plot
    :type save_path: pathlib.Path object
    """    
    fig, ax1 = plt.subplots(figsize=(20, 8))

    color = 'black'
    ax1.set_xlabel("time")
    ax1.set_ylabel(y1, color=color)
    ax1.plot(df1[x1], df1[y1], color=color, drawstyle="steps")
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'red'
    ax2.set_ylabel(y2, color=color)
    ax2.plot(df2[x2], df2[y2], color=color, drawstyle="steps")
    ax2.tick_params(labelcolor=color)
    
    (save_path).mkdir(parents=True, exist_ok=True)
    plt.savefig(str(str(save_path / f"{filename}.png")))