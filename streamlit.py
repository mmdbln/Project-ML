import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
import seaborn as sns
from datetime import datetime

# Sample data
path = st.text_input("Enter Path")
king_county_df =  pd.read_csv("/home/mohe/Desktop/notebooks/king_county_cleaned_data.csv", low_memory=False, dtype={"Violation Code": "object"})
king_county_df["Inspection Date"] = pd.to_datetime(king_county_df["Inspection Date"])
not_null = king_county_df[~(king_county_df['Longitude'].isnull()) & ~(king_county_df['Grade'].isnull())]
not_null['Grade Color'] = not_null['Grade'].map({1: 'red', 2: 'blue', 3: 'green', 4: 'purple'})
new_gp = not_null.groupby('City')[['City','Inspection Date','Latitude','Longitude','Grade Color']].head()
new_gp2 = not_null.groupby('Inspection Date')[['Inspection Date','City','Latitude','Longitude','Grade Color']].head()
new_gp2 = new_gp2[pd.notnull(new_gp2['Inspection Date'])]
dates_gp = new_gp2['Inspection Date'].nunique()
date = '2006-01-04'
city_gp = new_gp2.loc[new_gp2['Inspection Date']==date] 
date = '2023-09-10'
city_gp = new_gp2.loc[new_gp2['Inspection Date']==date] 
date = '2006-01-03'
city_gp = new_gp2.loc[new_gp2['Inspection Date']==date] 



# 

# Dropdown menu for selecting a date
selected_date = st.selectbox("Select Inspection Date", ["2006-1-1", "2007-1-1", "2008-1-1", "2009-1-1", "2010-1-1", "2011-1-1", "2012-1-1", "2013-1-1", "20014-1-1", "2015-1-1", "2016-1-1", "2017-1-1", "2018-1-1", "2019-1-1", "2020-1-1", "2021-1-1", "2022-1-1", "2023-1-1"])

# Function to create and display the map
def map_date(date, df):
    king_map = folium.Map(location=[47.5480, -121.9836], zoom_start=8)
    city_gp = df.loc[df['Inspection Date'] == date]
    for i in range(0, len(city_gp)):
        clr = city_gp.iloc[i]['Grade Color']
        folium.Marker(location=[city_gp.iloc[i]['Latitude'], city_gp.iloc[i]['Longitude']], icon=folium.Icon(color=clr), ).add_to(king_map)
    map_html = king_map.get_root().render()
    st.components.v1.iframe(map_html, width=700, height=500)\


st.title("Folium Map Example")
map_date(selected_date, new_gp2)

# ...........................

closed_business = king_county_df[king_county_df["Inspection Closed Business"] == 1]
s = pd.DataFrame(closed_business[["Violation Code", "Violation Description", "Violation Points", "Violation Type"]].value_counts())
st.write(s)


plt.figure(figsize=(20,5))
sns.countplot(data=closed_business, x="Violation Code", hue="Violation Type", palette=["red", "blue"], dodge=False, order=closed_business["Violation Code"].value_counts().index)
plt.rcParams.update({'font.size': 7})
plt.xticks(rotation=45)
st.pyplot(plt)




newking = king_county_df.sort_values('Inspection Date')
newking = newking[~(newking['Inspection Date'].isnull())]
st.write(newking)


resampled_dates = newking.loc[:,['Inspection Date','Inspection Closed Business']].copy()
st.write(resampled_dates)


resample_6M = resampled_dates.set_index('Inspection Date').resample('6M')['Inspection Closed Business'].agg(['count', 'sum'])
plt.figure()
ax1 = resample_6M['count'].plot(kind='bar')
ax1.set_title('Number of inspections per 6 months')
ax1.set_xlabel('Inspection Dates')
st.pyplot(plt)

plt.figure()
ax2 = resample_6M['sum'].plot(kind='bar')
ax2.set_title('Number of closed business per 6 months')
ax2.set_xlabel('Inspection Dates')
st.pyplot(plt)



resample_Y = resampled_dates.set_index('Inspection Date').resample('Y')['Inspection Closed Business'].agg(['count', 'sum'])
plt.figure()

ax1 = resample_Y['count'].plot(kind='bar')
ax1.set_title('Number of inspections per year')
ax1.set_xlabel('Inspection Dates')
st.pyplot(plt)


plt.figure()
ax2 = resample_Y['sum'].plot(kind='bar')
ax2.set_title('Number of closed business per year')
ax2.set_xlabel('Inspection Dates')
st.pyplot(plt)


table = king_county_df.groupby("Business_ID").agg({"City": "first", "Grade": "first", "Seating": "first", "Risk": "first", "Inspection Date": "nunique"}).sort_values("Inspection Date", ascending=False)
table.columns = ["City", "Grade", "Seating", "Risk", "Number of Inspections"]
st.write(table)



#t=table.head(50)
#plt.figure(figsize=(20,25))
#
#plt.subplot(411)
#sns.barplot(data=t, x=t.index, y="Number of Inspections", hue="City", dodge=False)
#plt.xticks(rotation=45)
#
#plt.subplot(412)
#sns.barplot(data=t, x=t.index, y="Number of Inspections", hue="Grade", dodge=False)
#plt.xticks(rotation=45)
#
#plt.subplot(413)
#sns.barplot(data=t, x=t.index, y="Number of Inspections", hue="Seating", dodge=False)
#plt.xticks(rotation=45)
#
#plt.subplot(414)
#sns.barplot(data=t, x=t.index, y="Number of Inspections", hue="Risk", dodge=False)
#plt.xticks(rotation=45)
#st.pyplot(plt)




r_name=["WENDY'S",'MCDONALD','SUBWAY','DOMINO','BURGER KING']

num=[]
for item in r_name:
    df2=king_county_df['Inspection Business Name'].str.find(item)
    list_index=df2[df2>-1].index
    num.append(king_county_df.iloc[list_index]['Business_ID'].nunique())
    print(king_county_df.iloc[list_index].groupby('Business_ID').first()['Risk'])
st.write(num)


num=[]
for item in r_name:
    df2=king_county_df['Inspection Business Name'].str.find(item)
    list_index=df2[df2>-1].index
    num.append(king_county_df.iloc[list_index]['Business_ID'].nunique())
    print(king_county_df.iloc[list_index].groupby('Business_ID').first()['Grade'].mean())
st.write(num)


num=[]
for item in r_name:
    df2=king_county_df['Inspection Business Name'].str.find(item)
    list_index=df2[df2>-1].index
    num.append(king_county_df.iloc[list_index]['Business_ID'].nunique())
    print(king_county_df.iloc[list_index].groupby('Business_ID').first()['Inspection Score'].mean())
    
st.write(num)


pop_df = pd.read_csv("/home/mohe/Desktop/notebooks/us-cities-table.csv")

king_county_df['City'] = king_county_df['City'].str.lower().str.capitalize()
pop_df['name'] = pop_df['name'].str.lower().str.capitalize()

king_county_df["City"] = king_county_df["City"].str.replace("Seatte" , "Seattle")
king_county_df["City"] = king_county_df["City"].str.replace("West seattle" , "Seattle")
king_county_df["City"] = king_county_df["City"].str.replace("Sea tac" , "Seatac")
king_county_df["City"] = king_county_df["City"].str.replace("Vashon island" , "Vashon")

merged_data = king_county_df.merge(pop_df[['name', 'pop2020']], left_on='City', right_on='name', how='left')
merged_data.rename(columns={'pop2020': 'population'}, inplace=True)

merged_data = merged_data.drop(['name'] ,axis='columns')
city_counts = merged_data['City'].value_counts()

city_counts_df = pd.DataFrame({'City': city_counts.index, 'Count': city_counts.values})

merged_data['City_Count'] = merged_data['City'].map(city_counts)



import plotly.express as px

plt.figure(figsize=(20,25))
sns.barplot(data=merged_data, x="population", y="City_Count", hue="City", dodge=False)plt.xticks(rotation=45)
st.write(plt)

