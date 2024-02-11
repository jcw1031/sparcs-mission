import pandas as pd
import streamlit as st
import folium
from folium import GeoJsonTooltip
from streamlit_folium import folium_static
import geopandas as gpd
import plotly.express as px

# Streamlit 페이지 설정
st.title('대전은 노잼 도시가 아니다!')

# 데이터 로딩
data_path = '학생수.csv'
df = pd.read_csv(data_path)

# 사용자 인터페이스 설정
filter_option = st.selectbox('필터링 기준:', ['학생수', '학원수', '유학수'])

fig = px.bar(df, x='지역', y=filter_option, color='지역', labels={'value': filter_option}, title=f'지역별 {filter_option}')
st.plotly_chart(fig)


# 지도 생성 함수
def create_map(df, geojson_path, centers, filter_option):
    m = folium.Map(location=[36.3504, 127.3845], zoom_start=11)

    # GeoJSON 레이어 추가
    folium.GeoJson(
        geojson_path,
        name="구",
        style_function=lambda feature: {'fillColor': get_color(feature['properties']['sggnm']),
                                        'color': 'grey',
                                        'weight': 1,
                                        'fillOpacity': 0.4},
        tooltip=GeoJsonTooltip(fields=['sggnm'], aliases=['구'], localize=True)
    ).add_to(m)

    # 원 추가
    for index, row in df.iterrows():
        district = row['지역']
        value = row[filter_option]

        folium.Circle(
            location=centers[district],
            radius=value,
            color=get_color(district),
            fill=True,
            fill_color=get_color(district),
            fill_opacity=0.6,
            tooltip=f"{district}: {filter_option} {value}",
        ).add_to(m)

    return m


# 색상 지정 함수
def get_color(district):
    colors = {
        '동구': 'blue',
        '중구': 'green',
        '서구': 'red',
        '유성구': 'purple',
        '대덕구': 'orange'
    }
    return colors.get(district, 'gray')


# GeoJSON 파일 로딩 및 각 구의 중심 계산
geojson_path = '대전광역시.geojson'
gdf = gpd.read_file(geojson_path)
gdf['center'] = gdf.geometry.centroid
centers = {row['sggnm']: [row['center'].y, row['center'].x] for index, row in gdf.iterrows()}

# 지도 생성 및 Streamlit에 표시
m = create_map(df, geojson_path, centers, filter_option)
folium_static(m)
