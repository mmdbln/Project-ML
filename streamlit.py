import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
import seaborn as sns
from datetime import datetime
from folium import Icon
from streamlit_folium import folium_static

# Sample data
king_county_df =  pd.read_csv("/home/mohe/Documents/Data/kc_clean.csv", low_memory=False, dtype={"Violation Code": "object"})
king_county_df["Inspection Date"] = pd.to_datetime(king_county_df["Inspection Date"])
not_null = king_county_df[~(king_county_df['Longitude'].isnull()) & ~(king_county_df['Grade'].isnull())]


# 

def map_score_to_color(row):
    score = row['Inspection Score']
    closed = row['Inspection Closed Business']

    if closed == 1:
        return 'black'
    elif 0 <= score <= 49:
        return 'green'
    elif 50 <= score <= 99:
        return 'orange'
    elif 100 <= score <= 149:
        return 'pruple'
    elif 150 <= score <= 180:
        return 'red'
    else:
        return 'unknown'


def map_date(start_date, end_date, df):
    # Create a map centered on a location
    king_map = folium.Map(location=[47.5480, -121.9836], zoom_start=8)
    
    # Filter the DataFrame based on date range
    date_mask = (df['Inspection Date'] >= str(start_date)) & (df['Inspection Date'] <= str(end_date))
    filtered_df = df[date_mask]
    
    for index, row in filtered_df.iterrows():
        # Extract data for each marker
        location = [row['Latitude'], row['Longitude']]
        color = row['grading_by_color']

        
        # Add markers to the map
        folium.Marker(location=location, icon=Icon(color=color)).add_to(king_map)
    
    # map_html = king_map.get_root().render()
    # st.components.v1.iframe(map_html, width=700, height=500)
    st.write("black: closed")
    st.write("green: 0 to 50")
    st.write("orange: 50 to 100")
    st.write("purple: 100 to 150")
    st.write("red: 150 to 180")

    folium_static(king_map)

    st.write("count of inspections :", len(filtered_df.groupby(by='Inspection_Serial_Num')))
    st.write("count of closed businesses :", len(filtered_df[filtered_df['Inspection Closed Business'] == 1].groupby(by='Inspection_Serial_Num')))

    filtered_df_closed_business = filtered_df[filtered_df["Inspection Closed Business"] == 1]
    show_most_closed_viol = pd.DataFrame(filtered_df_closed_business[["Violation Code", "Violation Description", "Violation Points", "Violation Type"]].value_counts())
    st.dataframe(show_most_closed_viol)
    
    show_most_viol_record = pd.DataFrame(filtered_df[["Violation Code", "Violation Description", "Violation Points", "Violation Type"]].value_counts())
    st.dataframe(show_most_viol_record)


not_null['grading_by_color'] = not_null.apply(map_score_to_color, axis=1)
gp = not_null.groupby('Inspection Date')[['Inspection Date','City','Latitude','Longitude','grading_by_color', 'Inspection Closed Business', 'Inspection_Serial_Num',"Violation Code", "Violation Description", "Violation Points", "Violation Type"]].head()
gp = gp[pd.notnull(gp['Inspection Date'])]
start_date = st.sidebar.date_input("Start Date", pd.to_datetime('2023-01-01'))
end_date = st.sidebar.date_input("End Date", pd.to_datetime('2023-01-31'))
map_date(start_date,end_date ,gp)
# Dropdown menu for selecting a date

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


# pop_df = pd.read_csv("/home/mohe/Desktop/notebooks/us-cities-table.csv")

# king_county_df['City'] = king_county_df['City'].str.lower().str.capitalize()
# pop_df['name'] = pop_df['name'].str.lower().str.capitalize()

# king_county_df["City"] = king_county_df["City"].str.replace("Seatte" , "Seattle")
# king_county_df["City"] = king_county_df["City"].str.replace("West seattle" , "Seattle")
# king_county_df["City"] = king_county_df["City"].str.replace("Sea tac" , "Seatac")
# king_county_df["City"] = king_county_df["City"].str.replace("Vashon island" , "Vashon")

# merged_data = king_county_df.merge(pop_df[['name', 'pop2020']], left_on='City', right_on='name', how='left')
# merged_data.rename(columns={'pop2020': 'population'}, inplace=True)

# merged_data = merged_data.drop(['name'] ,axis='columns')
# city_counts = merged_data['City'].value_counts()

# city_counts_df = pd.DataFrame({'City': city_counts.index, 'Count': city_counts.values})

# merged_data['City_Count'] = merged_data['City'].map(city_counts)



# import plotly.express as px

# plt.figure(figsize=(20,25))
# sns.barplot(data=merged_data, x="population", y="City_Count", hue="City", dodge=False)
# plt.xticks(rotation=45)
# st.write(plt)

