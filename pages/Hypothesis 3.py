import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import koreanize_matplotlib
import plotly.express as px
import numpy as np
from matplotlib.backends.backend_agg import RendererAgg
import requests
from streamlit_lottie import st_lottie
from streamlit_folium import st_folium
import folium
from PIL import Image
import json

# 가설 3 : 인구수 - 의료기관 개폐업
st.set_page_config(
    page_title="Hypothesis 3 : Other Infrastructures - Medical Institutions",
    page_icon="👴",
    layout="wide",
)

# Lottie Icon


@st.cache
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_url = "https://assets2.lottiefiles.com/packages/lf20_uwWgICKCxj.json"
lottie_json = load_lottieurl(lottie_url)
st_lottie(lottie_json, speed=1, height=300, key="initial")


# geo_info
geo_str_seoul = json.load(open('data/seoul.json'))

# Preparation to display plot
# matplotlib.use("agg")
_lock = RendererAgg.lock

# Title
st.title("Hypothesis 3 : Other Infrastructures - Medical Institutions")

st.subheader(
    '''
        **[ 가설 3 ]**  다른 분야의 인프라와 의료기관 수
        '''
)


# Introduction
row1_spacer1, row1_1, row1_spacer2 = st.columns([0.1, 3.2, 0.1])

with row1_1, _lock:
    st.markdown(
        '''
        의료인프라는 다른 분야의 인프라 수준과 상관관계가 있을 것이다.
        
        '''
    )

    st.markdown(
        '''
        '''
    )

    st.markdown(
        '''
        그 중에서도 **서울특별시** 25개구의
        지하철역 개수, 문화시설 수, 녹지면적, 녹지수, 공공도서관 수 등의 
        **문화, 환경, 교육, 교통** 분야의 인프라 데이터와 비교하였다. 
        '''
    )


@ st.cache
def get_hypo_data(hypo_name):
    file_name = f"data/{hypo_name}.csv"
    data = pd.read_csv(file_name)
    return data


data = get_hypo_data('df_seoul_final')

data_seoul_pdata = data.set_index('시군구명')
subway = get_hypo_data('subway').drop('Unnamed: 0', axis=1)

seoul_subway = subway[subway['시도명'] == '서울특별시']

# Display Data Set
row3_space1, row3_1, row3_space2 = st.columns(
    (0.01, 1, 0.01)
)

with row3_1, _lock:
    st.subheader("DataSet")
    with st.expander("DataSet 보기 👉"):
        st.markdown('**서울특별시 의료기관 수 현황**')
        st.dataframe(data)
        st.markdown('**지하철역 개수 현황**')
        st.dataframe(subway)

st.markdown('''
            ***
            ''')

# Hypothesis Verification
analysis_space1, analysis_1, analysis_space2 = st.columns(
    (0.01, 1, 0.01)
)

with analysis_1, _lock:
    st.subheader("Hypothesis Verification")

    st.markdown('''
                **❌ 서울특별시 25개 구의 경우 의료인프라와 문화, 환경, 교육 인프라간에 뚜렷한 상관관계를 보이지 않는다.**

                → 서울시 25개 구를 기준으로 구별로 교통, 문화, 환경, 교육인프라를 비교한 결과,
                다른 분야의 인프라와 유의미한 상관관계를 가지는 것 또한 총인구수 지표였다.
                ''')
    st.image(Image.open('img/elder_medical_corr.png'))  # mz_medical_corr


st.markdown('''
            ***
            ''')


# Map Visualization
m_space1, m_1, m_space2 = st.columns(
    (0.01, 1, 0.01)
)
with m_1, _lock:
    st.subheader("Map Visualization")

# Folium_population
map_space1, map_1, map_space2, map_2, map_space3 = st.columns(
    (0.1, 1, 0.05, 1, 0.1)
)


with map_1, _lock:
    st.markdown('👥 **서울특별시 인구 수 현황**')

    map_seoul_population = folium.Map(location=[37.5665, 127], zoom_start=10)

    choropleth = folium.Choropleth(geo_data=geo_str_seoul,
                                   data=data_seoul_pdata["인구수"],
                                   columns=[data_seoul_pdata.index,
                                            data_seoul_pdata["인구수"]],
                                   fill_color="PuRd", key_on='feature.properties.SIG_KOR_NM').add_to(map_seoul_population)
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(fields=['SIG_KOR_NM'],
                                       aliases=['SIG_KOR_NM'],
                                       labels=True,
                                       localize=True,
                                       sticky=False,
                                       style="""
                                    background-color: #F0EFEF;
                                    border: 2px solid black;
                                    border-radius: 3px;
                                    box-shadow: 3px;
                                    """)
    )
    st_folium(map_seoul_population, width=400, height=400)


with map_2, _lock:

    st.markdown('🏥 **서울특별시 의료기관 수 현황**')
    map_seoul_medical = folium.Map(
        location=[37.5665, 127], zoom_start=10)
    choropleth = folium.Choropleth(geo_data=geo_str_seoul,
                                   data=data_seoul_pdata['만명당_요양기관_수'],
                                   columns=[data_seoul_pdata.index,
                                            data_seoul_pdata['만명당_요양기관_수']],
                                   fill_color='PuRd',
                                   fill_opacity=0.7,
                                   line_opacity=0.5,
                                   key_on='feature.properties.SIG_KOR_NM').add_to(map_seoul_medical)

    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(fields=['SIG_KOR_NM'],
                                       aliases=['SIG_KOR_NM'],
                                       labels=True,
                                       localize=True,
                                       sticky=False,
                                       style="""
                                    background-color: #F0EFEF;
                                    border: 2px solid black;
                                    border-radius: 3px;
                                    box-shadow: 3px;
                                    """)
    )
    st_folium(map_seoul_medical, width=400, height=400)


# Folium_population
map2_space1, map2_1, map2_space2, map2_2, map2_space3 = st.columns(
    (0.1, 1, 0.05, 1, 0.1)
)


with map2_1, _lock:
    df_seoul_subway = seoul_subway.set_index("시군구명")

    st.markdown('🚆 **서울특별시 지하철역 개수**')
    map_seoul_subway = folium.Map(location=[37.5665, 127], zoom_start=10)

    choropleth = folium.Choropleth(geo_data=geo_str_seoul,
                                   data=df_seoul_subway["역 개수"],
                                   columns=[df_seoul_subway.index,
                                            df_seoul_subway["역 개수"]],
                                   fill_color="Purples", key_on='feature.properties.SIG_KOR_NM').add_to(map_seoul_subway)
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(fields=['SIG_KOR_NM'],
                                       aliases=['SIG_KOR_NM'],
                                       labels=True,
                                       localize=True,
                                       sticky=False,
                                       style="""
                                    background-color: #F0EFEF;
                                    border: 2px solid black;
                                    border-radius: 3px;
                                    box-shadow: 3px;
                                    """)
    )
    st_folium(map_seoul_subway, width=400, height=400)


with map2_2, _lock:

    st.markdown('🏥 **서울특별시 인구 1만 명 당 의료기관 수 현황**')
    map_seoul_10000 = folium.Map(location=[37.5665, 127], zoom_start=10)

    choropleth = folium.Choropleth(geo_data=geo_str_seoul,
                                   data=data_seoul_pdata["인구수"],
                                   columns=[data_seoul_pdata.index,
                                            data_seoul_pdata["인구수"]],
                                   fill_color="Purples", key_on='feature.properties.SIG_KOR_NM').add_to(map_seoul_10000)
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(fields=['SIG_KOR_NM'],
                                       aliases=['SIG_KOR_NM'],
                                       labels=True,
                                       localize=True,
                                       sticky=False,
                                       style="""
                                    background-color: #F0EFEF;
                                    border: 2px solid black;
                                    border-radius: 3px;
                                    box-shadow: 3px;
                                    """)
    )
    st_folium(map_seoul_10000, width=400, height=400)

analy_space1, analy_1, analy_space2 = st.columns(
    (0.1, 2, 0.1)
)
with analy_1, _lock:
    st.markdown('''
                → 서울시 25개 구와 인프라간의 상관관계는 없지만 강남구에는 대부분의 인프라가 몰려있는 것으로 확인할 수 있었다. 
                특히  교통 인프라중 하나인 지하철 인프라를 시각화 해보았을 때, 의료기관과 유사한 점을 볼 수 있었다. 
                ''')
    st.markdown('''
                ''')


st.markdown('''
            ***
            ''')


# Map Visualization
m1_space1, m1_1, m1_space2 = st.columns(
    (0.01, 1, 0.01)
)
# with m1_1, _lock:
# st.subheader("Map Visualization")


further_spacer1, further_1, further_spacer2 = st.columns((0.01, 1, 0.01))
with further_1, _lock:

    st.subheader('**Conclusion**')
    st.markdown(
        '''
        
        서울시 강남구에 의료기관이 제일 많이 집중되어 있는 이유로, 
        강남에는 미용목적 의료기관이 몰려있기 때문이 아닐까?
        
        '''
    )
    st.markdown(
        '''
        '''
    )
st.markdown(
    '''
    ***
    '''
)


# Footers
footer_space1, footer_1, footer_space2 = st.columns(
    (0.01, 1, 0.01)
)

with footer_1, _lock:
    st.markdown(
        '''
        🦁

        **성장발육엔텐텐** - 이재모, 조예슬, 임혜진, 김영민
        '''
    )

    st.markdown(
        "**멋쟁이사자처럼 AI 스쿨 7기 미드프로젝트** : 2022.10.19 - 2022.10.23"

    )
