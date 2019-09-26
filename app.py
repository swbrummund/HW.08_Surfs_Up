from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

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
        f"/api/v1.0/tobs"
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
    active = session.query(station.name).group_by(station.name).all()
    x = [list(row) for row in active]
    session.close()

    # columns = inspector.get_columns('station')
    # for column in columns:
    #     print('hello')
    #     print(column["name"], column["type"]) 

    return jsonify(x)

# Obsserved Temps


if __name__ == '__main__':
    app.run(debug=True)