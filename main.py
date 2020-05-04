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
    save_path = Path("plots/")

    # DATA A) covid zürich data
    url_cov_zh = "https://raw.githubusercontent.com/openZH/covid_19/master/fallzahlen_kanton_alter_geschlecht_csv/COVID19_Fallzahlen_Kanton_ZH_alter_geschlecht.csv"
    cov_zh = dc.cov_zh_get_data(url_cov_zh)
    plot_data = dc.cov_zh_prep_plot_data(cov_zh, "D")
    # plotly_graph_dual_axis(plot_data, "Date", "NewConfCases", "NewDeaths", save_path)

    # DATA B) zurich 'party barometer' zurich hardbruecke station
    ckan_url = "https://data.stadt-zuerich.ch/api/3/action/datastore_search?resource_id=5baeaf58-9af2-4a39-a357-9063ca450893"
    data = dc.ckan_get_all_recs(ckan_url)
    hardbr_df = dc.ckan_wrangle_records(data)
    hardbr_df_eastnorth = dc.ckan_prep_plot_data(
        hardbr_df, "Name", "Ost-Nord total", "Timestamp", "D"
    )
    # plotly_graph(hardbr_df_eastnorth, "datetime", ["pedestrians_hardbruecke_northeast"], "zh_hardbr", save_path)

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
        save_path,
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
        save_path,
    )


if __name__ == "__main__":
    main()
