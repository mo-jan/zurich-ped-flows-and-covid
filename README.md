# traffic-flows
Monitor mobility and pedestrian flow during corona lockdown policies. 


## Notes: COVID-19 data and research links
- Pedestrian flow data Zurich Hardbrücke station, "party barometer" https://data.stadt-zuerich.ch/dataset/vbz_frequenzen_hardbruecke
- Covid19 Zürich data: https://raw.githubusercontent.com/openZH/covid_19/master/fallzahlen_kanton_alter_geschlecht_csv/COVID19_Fallzahlen_Kanton_ZH_alter_geschlecht.csv
- Apple data on mobility https://www.apple.com/covid19/mobility


Further:
- Google popular times
  - Scrape google popular times https://github.com/philshem/gmaps_popular_times_scraper
  - GooglePopularTimeGraph, Authors Katharina Kaelin & Philshem https://kalakaru.github.io/GooglePopularTimeGraphAnalysis/
- https://db.schoolofdata.ch/event/7#top
  - Overview repo to monitor measure success https://github.com/baffelli/covid-2019-measures
- Very good summary https://fkrauer.github.io/covid-measures/
- graphical covid summary https://rastrau.shinyapps.io/covidmonitor/
- Feinstaub
  - link: https://data.stadt-zuerich.ch/dataset/luftqualitaet-stunden-aktuelle-messungen/resource/c3a611fb-c26a-4970-95f0-586e5fc50aa3


## ToDo

### Zurich
- [ ] Create one plot comparing cov_zh and hardbrueke "barometer" in one graph. See here how to add multiple y-axes in plotly https://plotly.com/chart-studio-help/documentation/python/multiple-axes/
- [ ] Use `analysis.ipynb` as reporting notebook, plots should show in github output
- [ ] Implement scheduled runner to update `analysis.ipynb` notebook.
- [ ] Create scheduled runner
- [ ] Implement Apple mobility data

### Global
- [ ] Create similar sets comparing indicators for policy adaption for various cities around the world
