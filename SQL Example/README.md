This folder contains a Jupyter notebook containing an analysis of bay area bike share data stored in Google Big Query that I performed using SQL and Pandas at Berkeley.

**Problem Statement**  
You're a data scientist at Ford GoBike (https://www.fordgobike.com/), the company running Bay Area Bikeshare. You are trying to increase ridership, and you want to offer deals through the mobile app to do so.  
  
**How many Morning and Evening trips are there?:**  
`! bq query --use_legacy_sql=FALSE --format=csv 'SELECT EXTRACT(DAYOFWEEK from start_date), count(start_date), trunc(avg(duration_sec)/60,1) as duration_mins FROM `bigquery-public-data.san_francisco.bikeshare_trips` WHERE EXTRACT(HOUR from start_date) >= 4 and EXTRACT(HOUR from start_date) <= 9 and EXTRACT(HOUR from end_date) <= 10 and duration_sec > 120 GROUP BY EXTRACT(DAYOFWEEK from start_date) ORDER BY 1' > result1.csv`  
  
`! bq query --use_legacy_sql=FALSE --format=csv 'SELECT EXTRACT(DAYOFWEEK from start_date), count(start_date), trunc(avg(duration_sec)/60,1) as duration_mins FROM `bigquery-public-data.san_francisco.bikeshare_trips` WHERE EXTRACT(HOUR from start_date) >= 16 and EXTRACT(HOUR from start_date) <= 19 and EXTRACT(HOUR from end_date) <= 20 and duration_sec > 120 GROUP BY EXTRACT(DAYOFWEEK from start_date) ORDER BY 1' > result2.csv`  

<img src="https://github.com/CraigGo/Portfolio/blob/master/SQL%20Example/AM_Bike_Trips.PNG"><img src="https://github.com/CraigGo/Portfolio/blob/master/SQL%20Example/PM_Bike_Trips.PNG">
