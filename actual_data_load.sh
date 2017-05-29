#!/bin/sh
month="June"
day=01
year=2017
MON=06
url="http://nemweb.com.au/Reports/CURRENT/Operational_Demand/FORECAST_HH/"
wget -q -O- "$url" | 
sed 's/<br>/<br>\'$'\n/g' | 
grep "$month $day" items.txt | 
egrep -o "PUBLIC_FORECAST_OPERATIONAL_DEMAND_HH_$year$MON$day.+\.zip\"" | 
sed "s/\"//g" > links.txt 
while read line
do
    echo "$url$line"
done < links.txt