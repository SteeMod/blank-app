import streamlit as st

# Example data for row_data
row_data = {
    'Day29': '2024-08-05',
    'Day29Yes': 'Yes',
    'Day29No': 'No',
    'Day29Dosage': '5ml',
    'Day29Freq': '1 time(s) daily',
    'Day29Form': 'Tablet',
    'Day29Route': 'Oral',
    'Day30': '2024-08-06',
    'Day30Yes': 'Yes',
    'Day30No': 'No',
    'Day30Dosage': '10ml',
    'Day30Freq': '2 time(s) daily',
    'Day30Form': 'Liquid',
    'Day30Route': 'Oral',
    'Day31': '2024-08-07',
    'Day31Yes': 'Yes',
    'Day31No': 'No',
    'Day31Dosage': '15ml',
    'Day31Freq': '3 time(s) daily',
    'Day31Form': 'Capsule',
    'Day31Route': 'Oral'
}

# Define the data for each day
days = [
    {'Day': 'Day29', 'Yes': 'Day29Yes', 'No': 'Day29No', 'Dosage': 'Day29Dosage', 'Frequency': 'Day29Freq', 'Form': 'Day29Form', 'Route': 'Day29Route'},
    {'Day': 'Day30', 'Yes': 'Day30Yes', 'No': 'Day30No', 'Dosage': 'Day30Dosage', 'Frequency': 'Day30Freq', 'Form': 'Day30Form', 'Route': 'Day30Route'},
    {'Day': 'Day31', 'Yes': 'Day31Yes', 'No': 'Day31No', 'Dosage': 'Day31Dosage', 'Frequency': 'Day31Freq', 'Form': 'Day31Form', 'Route': 'Day31Route'}
]

# Create a 7x3 table
for day in days:
    cols = st.columns(7)
    cols[0].text_input(day['Day'], value=str(row_data.get(day['Day'], '')))
    cols[1].text_input(day['Yes'], value=str(row_data.get(day['Yes'], '')))
    cols[2].text_input(day['No'], value=str(row_data.get(day['No'], '')))
    cols[3].text_input(day['Dosage'], value=str(row_data.get(day['Dosage'], '')))
    cols[4].text_input(day['Frequency'], value=str(row_data.get(day['Frequency'], '')))
    cols[5].text_input(day['Form'], value=str(row_data.get(day['Form'], '')))
    cols[6].text_input(day['Route'], value=str(row_data.get(day['Route'], '')))
