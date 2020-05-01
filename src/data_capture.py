#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import json
import datetime as dt
from pprint import pprint

import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots


def ckan_get_datasample(ckan_url):
    url_3_recs = f"{ckan_url}&limit=3"
    fileobj = requests.get(url_3_recs)
    data_sample = fileobj.json()
    return data_sample


def ckan_get_num_recs(ckan_url):
    num_recs = ckan_get_datasample(ckan_url)["result"]["total"]
    return num_recs


def ckan_get_all_recs(ckan_url):
    num_recs = ckan_get_num_recs(ckan_url)
    url_all_recs = f"{ckan_url}&limit={num_recs}"
    data = requests.get(url_all_recs).json()
    assert data["success"] == True, "result did NOT return 'success': True"
    return data


def ckan_wrangle_records(data):
    df = pd.DataFrame(data["result"]["records"])
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], infer_datetime_format=True)
    df.set_index("Timestamp", inplace=True, drop=False)
    df.In, df.Out = pd.to_numeric(df.In), pd.to_numeric(df.Out)
    df["total_counts"] = df["In"] + df["Out"]
    return df


def ckan_prep_plot_data(df, id_col, meter_name, datetime_col, resample_freq):
    df = df.loc[df[id_col] == meter_name, ["In", "Out", "total_counts"]].sort_values(
        datetime_col
    )
    df = df.resample(resample_freq).sum()
    df["datetime"] = df.index
    return df



def apple_mobility_data():
    URL = "https://www.apple.com/covid19/mobility"
    pass



def cov_zh_get_data(url):
    """Wrapper function: Call get_raw_csv() and clean_cov_zh() functions
    to capture and clean the covid Zürich dataset. 

    :param url: url to githubusercontent where csv is published 
    :type url: string
    :return: dataframe with covid Zürich data
    :rtype: pd.DataFrame
    """
    df = get_raw_csv(url)
    df = cov_zh_wrangle_data(df)
    return df


def get_raw_csv(url):
    """Capture raw data from url, return dataframe

    :param url: url to githubusercontent where csv is published 
    :type url: string
    :return: dataframe with raw covid Zürich data
    :rtype: pd.DataFrame
    """
    raw = requests.get(url).content
    df = pd.read_csv(io.StringIO(raw.decode("utf-8")))
    return df


def cov_zh_wrangle_data(df):
    """Format "Date" column into "datetime". Set "Date" column as index

    :param df: raw dataframe containing covid Zürich data
    :type df: pd.DataFrame
    :return: wrangled dataframe
    :rtype: pd.DateFrame
    """
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True, drop=False)
    return df


def cov_zh_prep_plot_data(df, resample_freq: str):
    """Prepare cov_zh dataframe for plotting, 
    select relevant columns "Date", "NewConfCases", "NewDeaths". 
    resampling to interval e.g. days or weeks

    :param df: cov_zh dataframe, wrangled
    :type df: pd.DataFrame
    :param resample_freq: resample to days ("D"), or weeks ("W")
    :type resample_freq: str
    :return: prepared dataframe for plotting
    :rtype: pd.DataFrame
    """
    df = df[["Date", "NewConfCases", "NewDeaths"]].resample(resample_freq).sum()
    df["Date"] = df.index
    return df