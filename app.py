from flask import Flask, jsonify
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

# Use code below if we want to import our app.py file into another Python file named "example.py", the variable "__name__" would be set to "example".
# import app

#print("example __name__ = %s", __name__)

#if __name__ == "__main__":
#    print("example is being run directly.")
#else:
#    print("example is being imported")

# Code below will def welcome route.
@app.route('/')
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')




@app.route("/api/v1.0/precipitation")

# In code below the ".\" is used to signify we want our query to continue on the next line. It helps to shorten query line
# The last two lines of below code is format for "jsonify()". JSON files are used for cleaning, filtering, sorting, and visualizing data.
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)


# In code above, when creating routes we'll follow naming convention "/api/v1.0/".  This convention signifies this is version 1 of our application.
#if __name__ == '__main__':
#    app.run()

@app.route("/api/v1.0/stations")

def stations():
    results = session.query(Station.station).all()
    stations =list(np.ravel(results))
    return jsonify(stations=stations)

#if __name__ == '__main__':
#    app.run()

@app.route("/api/v1.0/tobs")
    
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

#if __name__ == '__main__':
#    app.run()

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    print(results,start,end)
    temps = list(np.ravel(results))
    return jsonify(temps)

if __name__ == '__main__':
    app.run()