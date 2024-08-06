import streamlit as st
import pandas as pd

# Sample row data
row_data = {
    'Day30': 'Sample Data',
    'Day30Yes': 'Yes',
    'Day30No': 'No',
    'Day30Dosage': '10mg',
    'Day30Freq': 'Once a day',
    'Day30Form': 'Tablet',
    'Day30Route': 'Oral',

    'Day31':'Sample Data',
    'Day31Yes': 'Yes',
    'Day31No': 'No',
    'Day31Dosage': '10mg',
    'Day31Freq': 'Once a day',
    'Day31Form': 'Tablet',
    'Day31Route': 'Oral'
}

# Convert row data to DataFrame
df = pd.DataFrame([row_data])

# Display the DataFrame in an editable table
edited_df = st.data_editor(df)

# Extract the edited values

Day30 = edited_df.at[0, 'Day30']
Day30Yes = edited_df.at[0, 'Day30Yes']
Day30No = edited_df.at[0, 'Day30No']
Day30Dosage = edited_df.at[0, 'Day30Dosage']
Day30Freq = edited_df.at[0, 'Day30Freq']
Day30Form = edited_df.at[0, 'Day30Form']
Day30Route = edited_df.at[0, 'Day30Route']
Day31 = edited_df.at[0, 'Day31']
Day31Yes = edited_df.at[0, 'Day31Yes']
Day31No = edited_df.at[0, 'Day31No']
Day31Dosage = edited_df.at[0, 'Day31Dosage']
Day31Freq = edited_df.at[0, 'Day31Freq']
Day31Form = edited_df.at[0, 'Day31Form']
Day31Route = edited_df.at[0, 'Day31Route']

