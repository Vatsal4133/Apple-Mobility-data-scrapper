import os
import requests
import csv
from pandas import *
from plotly.offline import download_plotlyjs,init_notebook_mode,plot,iplot
import plotly as py
import plotly.graph_objs as go
import matplotlib.pyplot as plt

url='https://covid19-static.cdn-apple.com/covid19-mobility-data/2210HotfixDev16/v3/en-us/applemobilitytrends-2022-03-26.csv'
response = requests.get(url)
with open(os.path.join("D:\\", "data.csv"), 'wb') as f:
    f.write(response.content)
f.close()

unw = []
data = pandas.read_csv("D:\\data.csv")
geo_type = data['geo_type'].tolist()
coun = data['country'].tolist()
for ele in range(len(geo_type)):
    if geo_type[ele] != "city":
        unw.append(ele)
for c in range(len(coun)):
    if coun[c] == "":
        coun.pop(c)
coun1 = set(coun)
newcoun = list(coun1)
newcoun.pop(0)
data.drop(unw,axis = 0, inplace=True)
data.drop("transportation_type",1)
data.drop("sub-region",1)
data.drop("alternative_name",1)
data.drop("country",1)
data.insert(810, column = "average", value = data.mean(axis = 1))
data.sort_values(by='average', ascending=False, inplace=True)
data.drop_duplicates(subset="region" , keep="first",inplace=True)
loca = []
avv = []
for i in range(0,50):
    city = data.iat[i, 1]
    avg = data.iat[i, 810]
    loca.append(city)
    avv.append(avg)
map = dict(type = 'choropleth',
locations = newcoun,
locationmode = 'country names',
colorscale= 'Hot',
z=[*range(1, 51, 1)],
colorbar = {'title':'Country Colours'})
chmap = go.Figure(data=[map])
iplot(chmap)
fig = plt.figure(figsize=(10, 15))
plt.bar(loca, avv, color='maroon',
        width=0.5)
plt.xlabel("Country")
plt.ylabel("Average mobility")
plt.title("Top 50 cities")
plt.xticks(rotation=90)
plt.show()