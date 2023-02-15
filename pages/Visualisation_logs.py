import streamlit as st
import pandas as pd 
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode



st.subheader("Load Logs")
df = pd.read_csv("log.csv")

st.dataframe(df.style.highlight_max(axis=0))
#st.write(df.head())
#st.write("---Interaction Log---")
#st.popup(df)
#st.dataframe(df)
#AgGrid(df,width=1000)


