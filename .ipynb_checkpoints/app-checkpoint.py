import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify
import datetime as dt


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Set up Flask
session = Session(engine)


# Home page.
# List all routes that are available.
app = Flask(__name__)

@app.route("/")
def home():
    """List all avialable api routes."""
    return(
        f"/api/v1.0/precipitation:<br/>"
        f"/api/v1.0/stations:<br/>"
        f"/api/v1.0/tobs:<br/>"
        f"/api/v1.0/<start> and /api/v1.0/<start>/<end>"
    )


# Convert the query results to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.
# Perform a query to retrieve the data and precipitation scores

# +
 
recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
recent_date = dt.datetime.strptime(recent_date[0], "%Y-%m-%d").date()
year_ago = recent_date - dt.timedelta(days=366)
last_12 = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > year_ago).all()


# -

precip_dict = [{i[0]: i[1]} for i in last_12]
precip_dict

for i in last_12: 
     precipDict = {i[0]: i[1]}
print(precipDict)


@app.route("/api/v1.0/precipitation")
def precip():
    session = Session(engine)

    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    recent_date = dt.datetime.strptime(recent_date[0], "%Y-%m-%d").date()
    year_ago = recent_date - dt.timedelta(days=366)
    last_12 = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > year_ago).all()
    
    precip_dict = ({"Date": last_12[1]} for last in last_12)
    return(precip_dict)
@app.route("/jsonified")
def jsonified():
    return jsonify()




# Return a JSON list of stations from the dataset.
# @app.route("/api/v1.0/stations")

# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.

# @app.route("/api/v1.0/tobs")

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

# @app.route("/api/v1.0/<start>")

# @app.route("/api/v1.0/<end")

# /api/v1.0/precipitation
# /api/v1.0/stations
# /api/v1.0/tobs
# /api/v1.0/<start> and /api/v1.0/<start>/<end>

if __name__ == '__main__':
    app.run(debug=True)
