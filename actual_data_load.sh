#!/bin/sh

# SCRAPE THE ACTUAL DATA 

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
month="September"
day=10
year=2016
MON=09
url="http://nemweb.com.au/Reports/CURRENT/Operational_Demand/FORECAST_HH/"
wget -q -O- "$url" | 
sed 's/<br>/<br>\'$'\n/g' | 
grep "$month $day" items.txt | 
egrep -o "PUBLIC_FORECAST_OPERATIONAL_DEMAND_HH_$year$MON$day.+\.zip\"" | 
sed "s/\"//g" > links.txt 
while read line
do
    #Wget -i "$url$line"
    echo "$url$line"
done < links.txt