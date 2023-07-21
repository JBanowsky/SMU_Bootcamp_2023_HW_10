# Import the dependencies.
import pandas as pd
from sqlalchemy import create_engine, text
from flask import Flask
import json

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///resources/hawaii.sqlite")

#################################################
# Flask Routes
#################################################
@app.route("/")
def Home():
    """List all available api routes."""
    return (
        f"""<h1>Hawaii Climate Analysis</h1>
        <h2>Available Routes:</h2>
        Copy the desired route from below and add it to the end of this page's url.</br></br>
        /api/v1.0/precipitation<br/>
        /api/v1.0/stations<br/>
        /api/v1.0/tobs<br/></br>
        For Min, Max and Average Temperatures based on dates use:</br>
        /api/v1.0/temp/'start'<br/>
        /api/v1.0/temp/'start'&'end'<br/>
        <p>'start' and 'end' date should be in the format YYYY-MM-DD.</p></br>
        Earliest start date: 2010-01-01</br>
        Most recent end date: 2017-08-23</br>"""
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Get Precipitation from previous year"""
    query = text("""
                SELECT
                    date,
                    station,
                    prcp
                FROM
                    measurement
                WHERE
                    date >= '2016-08-23'
            """)

# Save the query results as a Pandas DataFrame. Explicitly set the column names
    prcp_df = pd.read_sql(query, engine)
    data = json.loads(prcp_df.to_json(orient="records"))
    return(data)

@app.route("/api/v1.0/stations")
def stations():
    """Get stations"""
    query = text("""
                SELECT
                    station,
                    count(*) as activity
                FROM
                    measurement
                GROUP BY
                    station
                ORDER BY
                    activity desc;
            """)

    stn_df = pd.read_sql(query, engine)
    data = json.loads(stn_df.to_json(orient="records"))
    return(data)

@app.route("/api/v1.0/tobs")
def temperature():
    """Get most active station by temp"""
    query = text("""
                SELECT
                    date,
                    station,
                    tobs                    
                FROM
                    measurement
                WHERE
                    station = 'USC00519281'
                    AND date >= '2016-08-23'                
            """)

    tobs_by_date = pd.read_sql(query, engine)
    data = json.loads(tobs_by_date.to_json(orient="records"))
    return(data)

@app.route("/api/v1.0/temp/<start>")
def temperature_start(start):
    """Get stations"""
    query = text(f"""
                SELECT
                    station,
                    date as earliest_date,
                    min(tobs) as tmin,
                    avg(tobs) as tmean,
                    max(tobs) as tmax
                FROM
                    measurement
                WHERE
                    date >= '{start}'
                GROUP BY
                    station;
            """)
    
    start_df = pd.read_sql(query, engine)
    data = json.loads(start_df.to_json(orient="records"))
    return(data)

@app.route("/api/v1.0/<start>&<end>")
def temperature_start_end(start, end):
    """Get stations"""
    query = text(f"""
                SELECT
                    station,
                    date as earliest_date,
                    min(tobs) as tmin,
                    avg(tobs) as tmean,
                    max(tobs) as tmax
                FROM
                    measurement
                WHERE
                    date >= '{start}'
                    and date <= '{end}'
                GROUP BY
                    station;
            """)

    start_end_df = pd.read_sql(query, engine)
    data = json.loads(start_end_df.to_json(orient="records"))
    return(data)

# run the website
if __name__ == '__main__':
    app.run()(debug=True)