from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)
stations = pd.read_csv("data_small/stations.txt", skiprows=17)
stations = stations[["STAID", "STANAME                                 ", "CN"]]


@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())


@app.route("/api/v1/<station>")
def station_data(station):
    filenum = str(station).zfill(6)
    station_data_filepath = "data_small/TG_STAID" + filenum + ".txt"
    df = pd.read_csv(station_data_filepath, skiprows=20, parse_dates=['    DATE'])
    result = df.to_dict(orient="records")
    return result


@app.route("/api/v1/yearly/<station>/<year>")
def yearly_station_data(station, year):
    filenum = str(station).zfill(6)
    station_data_filepath = "data_small/TG_STAID" + filenum + ".txt"
    df = pd.read_csv(station_data_filepath, skiprows=20)
    df['    DATE'] = df['    DATE'].astype(str)
    result = df[df['    DATE'].str.startswith(str(year))].to_dict(orient="records")
    return result


@app.route("/api/v1/<station>/<date>/")
def api(station, date):
    # read station csv
    filenum = str(station).zfill(6)
    station_data_filepath = "data_small/TG_STAID" + filenum + ".txt"
    df = pd.read_csv(station_data_filepath, skiprows=20, parse_dates=['    DATE'])

    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10

    return {"station": station,
            "date": date,
            "temperature": temperature}


if __name__ == "__main__":
    app.run(debug=True, port=5002)
