import numpy as np
import datetime as dt
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite", echo=False)
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    return (
    f"Available Routes:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"For the opperations below please use date format yyyy-mm-dd</br>"
    f"/api/v1.0/start<br/>"
    f"/api/v1.0/start/end<br/>"
)

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    all_measurements = []
    
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        all_measurements.append(prcp_dict)
    return jsonify(all_measurements)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station, Station.name).all()
    session.close()

    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(func.strftime(Measurement.date) > "2016-08-23").\
            filter(Measurement.station == 'USC00519281').all()
    session.close()

    annual_tobs = list(np.ravel(results))
    return jsonify(annual_tobs)

@app.route("/api/v1.0/start")
def start_vaca(start):
    session = Session(engine)
    input_date = dt.datetime.strptime(start, '%y-%m-%d')
    start_date = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= input_date).all()
    session.close
    vaca_start = list(np.ravel(start_date))
    return jsonify(vaca_start)

@app.route("/api/v1.0/start/end")
def vaca_start_end(start, end):
    session = Session(engine)
    input_start = dt.datetime.strptime(start, '%y-%m-%d')
    input_end = dt.datetime.strptime(end, '%y-%m-%d')
    vaca_length = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= input_start).filter(Measurement.date <= input_end).all()
    all_days = list(np.ravel(vaca_length))
    return jsonify(all_days)

if __name__ == "__main__":
    app.run(debug=True)



