import streamlit as st
import pandas as pd

# Sample row data
row_data = {
    'Day31': 'Sample Data',
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
Day31 = edited_df.at[0, 'Day31']
Day31Yes = edited_df.at[0, 'Day31Yes']
Day31No = edited_df.at[0, 'Day31No']
Day31Dosage = edited_df.at[0, 'Day31Dosage']
Day31Freq = edited_df.at[0, 'Day31Freq']
Day31Form = edited_df.at[0, 'Day31Form']
Day31Route = edited_df.at[0, 'Day31Route']

