import streamlit as st
import pandas as pd

# Sample data
row_data = {
    'Day1': 'Monday', 'Day1Yes': 'Yes', 'Day1No': 'No', 'Day1Dosage': '10mg', 'Day1Freq': 'Once', 'Day1Form': 'Tablet', 'Day1Route': 'Oral',
    'Day2': 'Tuesday', 'Day2Yes': 'Yes', 'Day2No': 'No', 'Day2Dosage': '20mg', 'Day2Freq': 'Twice', 'Day2Form': 'Capsule', 'Day2Route': 'Oral',
    'Day3': 'Wednesday', 'Day3Yes': 'Yes', 'Day3No': 'No', 'Day3Dosage': '30mg', 'Day3Freq': 'Thrice', 'Day3Form': 'Liquid', 'Day3Route': 'Oral'
}

# Convert the data to a DataFrame
data = {
    'Day': [row_data['Day1'], row_data['Day2'], row_data['Day3']],
    'Yes': [row_data['Day1Yes'], row_data['Day2Yes'], row_data['Day3Yes']],
    'No': [row_data['Day1No'], row_data['Day2No'], row_data['Day3No']],
    'Dosage': [row_data['Day1Dosage'], row_data['Day2Dosage'], row_data['Day3Dosage']],
    'Frequency': [row_data['Day1Freq'], row_data['Day2Freq'], row_data['Day3Freq']],
    'Form': [row_data['Day1Form'], row_data['Day2Form'], row_data['Day3Form']],
    'Route': [row_data['Day1Route'], row_data['Day2Route'], row_data['Day3Route']]
}

df = pd.DataFrame(data)

# Display the editable table
edited_df = st.experimental_data_editor(df)

# Display the edited data
st.write("Edited Data:")
st.write(edited_df)
