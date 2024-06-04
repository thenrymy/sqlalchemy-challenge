# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with = engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route('/')
def homepage():
    '''List all available api routes'''
    return (
        f'Available routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs'
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    '''Dictionary of Date: prcp'''
    twelve_months_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= twelve_months_ago).\
        all()
    precipitation = {date: prcp for date, prcp in results}
    return jsonify (precipitation)

@app.route('/api/v1.0/stations')
def stations():
    '''List of all stations'''
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify (stations)

@app.route('/api/v1.0/tobs')
def temperature():
    '''List of temperatures for the busiest station for the whole of last year'''
    twelve_months_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    busiest_station = session.query(Measurement.tobs).\
        filter(Measurement.date >= twelve_months_ago).\
        filter(Measurement.station == 'USC00519281').all()
    results = list(np.ravel(busiest_station))
    return jsonify (results)

@app.route('/api/v1.0/<start>')
def specified_start(start):
    '''Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start'''
    specified_start = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    results = list(np.ravel(specified_start))
    return jsonify (results)

@app.route('/api/v1.0/<start>/<end>')
def specified_start_end(start, end):
    '''Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start and end'''
    specified_start_end = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).\
        all()
    results = list(np.ravel(specified_start_end))
    return jsonify (results)

if __name__ == "__main__":
    app.run(debug=True)