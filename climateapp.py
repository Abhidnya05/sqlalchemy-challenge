import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station     = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Different Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation_list():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation and date"""
    # Query all passengers
    precipitation_q = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > query_date).order_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    precip =  []
    for date, prcp in precipitation_q:
        precipitation_dict       = {}
        precipitation_dict[date] = prcp
        precip.append(precipitation_dict)

    return jsonify(precip)

@app.route("/api/v1.0/stations")
def station_list():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations"""
    # Query all passengers
    station_q = session.query(Station.id,Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation).all()
    
    session.close()
    
    stat = []
    for id,station,name,latitude,longitude,elevation in station_q:
        station_dict              ={}
        station_dict['Id']        =id
        station_dict['station']   =station
        station_dict['name']      =name
        station_dict['latitude']  =latitude
        station_dict['longitude'] =longitude
        station_dict['elevation'] =elevation
        stat.append(station_dict)
    return jsonify(stat)

@app.route("/api/v1.0/tobs")
def tempartureobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of dates and temperature observations of the most-active station for the previous year of data """
    
    # Find the most recent date in the data set.
    latest_date     = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    latest_date1    = list(np.ravel(latest_date))[0]
    latest_date2    = dt.datetime.strptime(latest_date1,"%Y-%m-%d")
    query_date      = latest_date2 - dt.timedelta(days=365)

    query_s1 = session.query(Measurement.station).\
                         group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    query_s3 = list(np.ravel(query_s1))[0]

    # Perform a query to retrieve the data and precipitation scores
    tempdate_q  = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > query_date and Measurement.station == query_s3).\
                  order_by(Measurement.date).all()
    session.close()

    temp = []
    for date, tos in tempdate_q:
        date_dict={}
        date_dict['date'] = date
        date_dict['tobs'] = tobs
        temps.append(date_dict)
    return jsonify(temps)


if __name__ == '__main__':
    app.run(debug=True)



