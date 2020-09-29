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
    f"/api/v1.0/<'start'><br/>"
    f"/api/v1.0/<'start'><'end'>"
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

if __name__ == "__main__":
    app.run(debug=True)



