#!/bin/sh
month="March"
days=(01 02 03 04 05 06 07 08 09 10) # Specify array of days
MON=03
year=2017

for ((i=0; i<${#days[*]}; i++));
do
    url="http://nemweb.com.au/Reports/CURRENT/Operational_Demand/FORECAST_HH/"
    wget -q -O- "$url" | 
    sed 's/<br>/<br>\'$'\n/g' | 
    egrep -o "PUBLIC_FORECAST_OPERATIONAL_DEMAND_HH_$year$MON${days[i]}.+\.zip\"" | 
    sed "s/\"//g" > links.txt 
    while read line
    do
        echo "$url$line" 
        wget --directory-prefix=../ForecastedData/${days[i]}$month$year -i "$url$line"
    done < links.txt
done
