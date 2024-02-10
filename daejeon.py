import pandas as pd
import streamlit as st
import streamlit_folium as sf
import folium as fl
import numpy as np
import plotly.express as px

st.title('대전은 노잼 도시가 아니다!')
df = pd.read_csv('학생수.csv')
# df.sort_values(by=['소분류 검색건수'], ascending=False, inplace=True)
# fig = px.bar(df, x='유형 소분류명', y='소분류 검색건수', title='소분류별 검색건수')

filter_option = st.selectbox('필터링 기준:', ['학생수', '학원수', '유학수'])

fig = px.bar(df, x='지역', y=filter_option, color='지역', labels={'value': filter_option}, title=f'지역별 {filter_option}')

st.plotly_chart(fig)

# st.plotly_chart(fig)

# chart_data = pd.DataFrame(index=df.columns, columns=["소분류 검색건수"])
# st.area_chart(chart_data)
