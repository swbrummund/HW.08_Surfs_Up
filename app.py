from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime as dt

import numpy as np

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

inspector = inspect(engine)

keys = Base.classes.keys()
print(keys)
measurement = Base.classes.measurement
station = Base.classes.station



app = Flask(__name__)

@app.route("/")
def home():
    print(keys)
    print(f"hello: {keys}")
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    results = session.query(measurement.prcp,measurement.date).all()

    session.close()

    prcp_list = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[prcp] = date
        prcp_list.append(prcp_dict)

    # columns = inspector.get_columns('Measurement')
    # for column in columns:
    #     return(column["name"], column["type"]) 

    return jsonify(prcp_list)



# Station
@app.route("/api/v1.0/station")
def station():

    session = Session(engine)
    active = session.query(measurement.station).distinct(measurement.station).all()
    session.close()

    names = list(np.ravel(active))

    return jsonify(names)

# Obsserved Temps
@app.route("/api/v1.0/tobs")
def tobs():

    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    print("Query Date: ", query_date)

    session = Session(engine)
    rain = session.query(measurement.date,measurement.tobs).filter(measurement.date > query_date).order_by(measurement.date).all()
    session.close()


    tobs_list = []
    for date, tobs in rain:
        tobs_dict = {}
        tobs_dict[tobs] = date
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

# start Date
@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    date = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).\
        filter(measurement.date >= start).all()

    session.close()

    temp_list = []
    for x,y,z in date:
        temp_dict = {}
        temp_dict["min_temp"] = x
        temp_dict["max temp"] = y
        temp_dict["avg temp"] = z
        temp_list.append(temp_dict)
    
    return jsonify(temp_list)

# start/end date 
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    session = Session(engine)
    date = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()

    session.close()

    
    temp_list = []
    for x,y,z in date:
        temp_dict = {}
        temp_dict["min_temp"] = x
        temp_dict["max temp"] = y
        temp_dict["avg temp"] = z
        temp_list.append(temp_dict)

    return jsonify(temp_list)






if __name__ == '__main__':
    app.run(debug=True)