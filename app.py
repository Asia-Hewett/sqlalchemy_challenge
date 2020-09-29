import numpy as np
import datetime as dt
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flaskm jsonify

engine = create_enging("sqlite:///hawaii.sqlite", echo=False)
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    return (
    f"Welcome to the Justice League API!<br/>"
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

    all_measurments = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        all_measurments.append(all_measurments)
    return jsonify(all_measurments)

# We are currently setting up the endpoints
# About and Home are the endpoints
# When a user makes a "get" request they will be make calls to your endpoints

# This is where the actual action occurs in a Python page
# We're going to take the app that we've created above
# and run it down here
if __name__ == "__main__":
    app.run(debug=True)


