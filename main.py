#!/usr/bin/env python
import io
import json
import datetime as dt
from pprint import pprint
from pathlib import Path

import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
import plotly.offline as pyo
import matplotlib.pyplot as plt

from src.plots import (
    plotly_graph,
    plotly_graph_dual_axis,
    multi_yaxis_plot,
    static_dual_axis_plot,
)
import src.data_capture as dc

pio.templates.default = "plotly_white"


def main():
    # variables
    plot_path = Path("plots/")
    data_path = Path("data_cron/")

    # DATA A) covid zürich data
    url_cov_zh = "https://raw.githubusercontent.com/openZH/covid_19/master/fallzahlen_kanton_alter_geschlecht_csv/COVID19_Fallzahlen_Kanton_ZH_alter_geschlecht.csv"
    cov_zh = dc.cov_zh_get_data(url_cov_zh)
    plot_data = dc.cov_zh_prep_plot_data(cov_zh, "D")
    # plotly_graph_dual_axis(plot_data, "Date", "NewConfCases", "NewDeaths", plot_path)

    # DATA B) zurich 'party barometer' zurich hardbruecke station
    ckan_url = "https://data.stadt-zuerich.ch/api/3/action/datastore_search?resource_id=5baeaf58-9af2-4a39-a357-9063ca450893"
    data = dc.ckan_get_all_recs(ckan_url)
    hardbr_df = dc.ckan_wrangle_records(data)
    hardbr_df_eastnorth = dc.ckan_prep_plot_data(
        hardbr_df, "Name", "Ost-Nord total", "Timestamp", "D"
    )
    # plotly_graph(hardbr_df_eastnorth, "datetime", ["pedestrians_hardbruecke_northeast"], "zh_hardbr", plot_path)

    # COMBINED interactive graph
    multi_yaxis_plot(
        plot_data,
        "Date",
        "NewConfCases",
        plot_data,
        "Date",
        "NewDeaths",
        hardbr_df_eastnorth,
        "datetime",
        "pedestrians_hardbruecke_northeast",
        "Zürich Covid19 data & Zürich Hardbrücke mobility trends",
        "zh_covid19_mobility",
        plot_path,
    )

    # COMBINED static graph for display in notebook and markdown file
    static_dual_axis_plot(
        hardbr_df_eastnorth,
        "datetime",
        "pedestrians_hardbruecke_northeast",
        plot_data,
        "Date",
        "NewDeaths",
        "zh_covid19_mobility_static",
        plot_path,
    )

    # Store data to csv files
    (data_path).mkdir(parents=True, exist_ok=True)
    today = dt.date.today().strftime("%Y-%m-%d")
    hardbr_df.to_csv(data_path / f"{today}_data_hardbr.csv")
    plot_data.to_csv(data_path / f"{today}_cov_zh.csv")


if __name__ == "__main__":
    main()
