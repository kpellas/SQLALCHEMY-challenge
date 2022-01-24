SQLAlchemy Homework - Surf's Up!

This project was completed based on the following criteria: 
You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii! To help with your trip planning, you need to do some climate analysis on the area. The following outlines what you need to do.

## Climate Analysis and Exploration

Precipitation Analysis
* Find the most recent date in the data set.

* Using this date, retrieved the last 12 months of precipitation data by querying the 12 preceding months of data. 

* Selected only the date and prcp values.

* Loaded the query results into a Pandas DataFrame and set the index to the date column.

* Sorted the DataFrame values by date.

* Plotted the results using the DataFrame plot method.

## Station Analysis

* Designed a query to calculate the total number of stations in the dataset.

* Designed a query to find the most active stations (i.e. which stations have the most rows?).

* Listed the stations and observation counts in descending order.

* Identified which station id has the highest number of observations.

* Using the most active station id, calculated the lowest, highest, and average temperature.

* Designed a query to retrieve the last 12 months of temperature observation data (TOBS).

* Filtered by the station with the highest number of observations.

* Queried the last 12 months of temperature observation data for this station.

* Plotted the results as a histogram with bins=12.

## Climate App
Desigedn a Flask API based on the queries above.

Creating the following routes in Flask:

* /

Home page.

List all routes that are available.

* /api/v1.0/precipitation

Converted the query results to a dictionary using date as the key and prcp as the value.

Returned the JSON representation of your dictionary.

* /api/v1.0/stations

Returne a JSON list of stations from the dataset.

* /api/v1.0/tobs

Queried the dates and temperature observations of the most active station for the last year of data.

Returned a JSON list of temperature observations (TOBS) for the previous year.

* /api/v1.0/<start> and /api/v1.0/<start>/<end>

Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.

When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

## Temperature Analysis I

* Hawaii is reputed to enjoy mild weather all year. Is there a meaningful difference between the temperature in, for example, June and December?

* Use pandas to perform this portion.

* Convert the date column format from string to datetime.

* Set the date column as the DataFrame index

* Drop the date column

* Identify the average temperature in June at all stations across all available years in the dataset. Do the same for December temperature.

* Use the t-test to determine whether the difference in the means, if any, is statistically significant. Will you use a paired t-test, or an unpaired t-test? Why?

## Temperature Analysis II

* Using historical data in the dataset find out what the temperature has previously looked like.

* The starter notebook contains a function called calc_temps that will accept a start date and end date in the format %Y-%m-%d. The function will return the minimum, average, and maximum temperatures for that range of dates.

* Use the calc_temps function to calculate the min, avg, and max temperatures for your trip using the matching dates from a previous year (i.e., use "2017-08-01").

* Plot the min, avg, and max temperature from your previous query as a bar chart.

* Use "Trip Avg Temp" as the title.

* Use the average temperature as the bar height (y value).

* Use the peak-to-peak (TMAX-TMIN) value as the y error bar (YERR).