#Set up dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify
import datetime as dt

#create an engine and prevent it from checking the same thread if the data is changed in the query
engine = create_engine("sqlite:///Resources/hawaii.sqlite?check_same_thread=False")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Set up Flask
app = Flask(__name__)
session = Session(engine)

#Set up home page and show all available routes:
@app.route("/")
def home():
    
    return(
        """See precipitation data for the last year:<br/> """
        f"/api/v1.0/precipitation<br/><br/>"
        """See Stations:<br/>"""
        f"/api/v1.0/stations<br/><br/>"
        """See temperature data for the last year:<br/>"""
        f"/api/v1.0/tobs<br/><br/>"
        """Specifiy start date to see low, high and average temps through to last date collected:<br/> """
        f"/api/v1.0/start_date<br/><br/>" 
        """Specify start and end date to see low, high and average temps for specified date range:<br/>"""
        f" /api/v1.0/start_date/end_date"
    )

#set up precipiation page. 
@app.route("/api/v1.0/precipitation")
def precip():
    # find most recent_date
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    recent_date = dt.datetime.strptime(recent_date[0], "%Y-%m-%d").date()
    year_ago = recent_date - dt.timedelta(days=366)
    last_12 = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > year_ago).all()
    
    precip_dict = [{i[0]: i[1]} for i in last_12]
    return jsonify(precip_dict) 


# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    station_names = session.query(Station.station, Station.name).\
    group_by(Station.station).\
    all()

    station_dict = [{i[0]: i[1]} for i in station_names]
    return jsonify(station_dict)

# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def most_active():
    session = Session(engine)
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    recent_date = dt.datetime.strptime(recent_date[0], "%Y-%m-%d").date()
    year_ago = recent_date - dt.timedelta(days=366)
    station_num = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).\
        desc()).\
        all()

    station_names = session.query(Station.station, Station.name).\
        all()

    sel = [Station.station,
      func.min(Measurement.tobs),
      func.max(Measurement.tobs),
      func.avg(Measurement.tobs)]
    most_active_station_stats = session.query(*sel).\
       filter(Station.station == station_num[0][0]).\
        all()
    station_id = most_active_station_stats[0][0]
    lowest_temp = most_active_station_stats[0][1]
    highest_temp = most_active_station_stats[0][2]
    avg_temp = round(most_active_station_stats[0][3], 2)
    most_act_last_12 = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date > year_ago).\
    filter(Measurement.station == station_id).\
    all()
    
    result = (list(np.ravel(most_act_last_12)))
    return jsonify(result)
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.

@app.route('/api/v1.0/<start_date>')
def start(start_date):
    
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    recent_date = dt.datetime.strptime(recent_date[0], "%Y-%m-%d").date()
    start_date = dt.datetime.strptime(str(start_date), "%Y-%m-%d").date()

    sel = [Measurement.date,
        Measurement.station,
       func.min(Measurement.tobs),
       func.max(Measurement.tobs),
       func.avg(Measurement.tobs)]

    if start_date > recent_date:
        return(f"Error: The date entered: {start_date}, is before {recent_date}. Please spedify another date.")
    else:
        start_date_results = session.query(*sel).\
                       filter(func.strftime("%Y-%m-%d", Measurement.date) >= start_date).\
                       group_by(Measurement.date).\
                       all()
        dates = []                       
        for result in start_date_results:
            dates.append(result[0])
            dates.append(f" Station ID: {result[1]}")
            dates.append(f" Min Temp: {result[2]}")
            dates.append(f" Max Temp: {result[3]}")
            dates.append(f" Avg Temp: {result[4]}")
        return jsonify(dates)
      
            
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
     

@app.route('/api/v1.0/<start_date>/<end_date>')

def start_end(start_date, end_date):
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    recent_date = dt.datetime.strptime(recent_date[0], "%Y-%m-%d").date()
    start_date = dt.datetime.strptime(str(start_date), "%Y-%m-%d").date()
    end_date = dt.datetime.strptime(str(end_date), "%Y-%m-%d").date()

    sel = [Measurement.date,
        Measurement.station,
       func.min(Measurement.tobs),
       func.max(Measurement.tobs),
       func.avg(Measurement.tobs)]
    if start_date > recent_date or start_date > end_date :
        return(f"Error: Please check the dates. The start date needs to earlier than {end_date} and {recent_date}.")
    else:
        start_end_results = session.query(*sel).\
                        filter(func.strftime("%Y-%m-%d", Measurement.date) >= start_date).\
                        filter(func.strftime("%Y-%m-%d", Measurement.date) <= end_date).\
                        group_by(Measurement.date).\
                        all()
        dates = []                       
    
        for result in start_end_results:

            dates.append(result[0])
            dates.append(f" Station ID: {result[1]}")
            dates.append(f" Min Temp: {result[2]}")
            dates.append(f" Max Temp: {result[3]}")
            dates.append(f" Avg Temp: {result[4]}")
        return jsonify(dates)


if __name__ == '__main__':
    app.run(debug=True)
