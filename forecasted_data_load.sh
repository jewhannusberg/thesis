#!/bin/sh

# SCRAPE FORECASTED OPERATIONAL DEMAND DATA 

# The following is for a daily implementation
# gets the date and downloads that day's data
# note that this can only be run between 11:30pm to 11:59pm to work
# now=`date`
# day=`date +%d`
# month=$(echo $now | cut -d' ' -f3)
# MON=`date +%m`
# year=$(echo $now | cut -d' ' -f4)
# case $month in 
#     Jan) month=January ;;
#     Feb) month=February ;;
#     Mar) month=March ;;
#     Apr) month=April ;;
#     May) month=May ;;
#     Jun) month=June ;;
#     Jul) month=July ;;
#     Aug) month=August ;;
#     Sep) month=September ;;
#     Oct) month=October ;;
#     Nov) month=November ;;
#     Dec) month=December ;;
# esac
#echo "$month $day"

# depends on a list of urls to the download link in items.txt
# these are cleaned up and stored in links.txt
# downloaded and saved in a folder in ForecastedData, e.g. 08February2017
# currently requires manual input of date
# eventually should take user input of any number of days (e.g. 08/02/17 - 31/02/17)

month="February"
day=10
year=2017
MON=02
url="http://nemweb.com.au/Reports/CURRENT/Operational_Demand/FORECAST_HH/"
wget -q -O- "$url" | 
sed 's/<br>/<br>\'$'\n/g' | 
# grep "$month $day" items.txt | 
egrep -o "PUBLIC_FORECAST_OPERATIONAL_DEMAND_HH_$year$MON$day.+\.zip\"" | 
sed "s/\"//g" > links.txt 
while read line
do
    echo "$url$line" 
    wget --directory-prefix=/Users/youhancheery/Documents/Thesis/ForecastedData/$day$month$year -i "$url$line"
done < links.txt