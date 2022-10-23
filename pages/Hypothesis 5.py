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

st.set_page_config(
    page_title="Hypothesis 5 : Population - Ages ratio - Opening And Closing",
    page_icon="",
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
geo_str_korea = json.load(open('data/korea.json'))
geo_str_gg = json.load(open('data/gg.json'))
geo_str_seoul = json.load(open('data/seoul.json'))

# Preparation to display plot
# matplotlib.use("agg")
_lock = RendererAgg.lock

# Title
st.title("Hypothesis 5 : Population - Ages ratio - Opening And Closing")

st.subheader(
    '''
        **[ 가설 5 ]**  인구수, 연령별 인구 비율, 그리고 의료기관 분포
        '''
)


# Introduction
row1_spacer1, row1_1, row1_spacer2 = st.columns([0.1, 3.2, 0.1])


@ st.cache
def get_hypo_data(hypo_name):
    file_name = f"data/{hypo_name}.csv"
    data = pd.read_csv(file_name)
    return data


data = get_hypo_data('df_now_hos')
df_oc_gg = get_hypo_data('df_gg_final')
df_oc_seoul = get_hypo_data('df_seoul_final')

# Display Data Set
row3_space1, row3_1, row3_space2 = st.columns(
    (0.01, 1, 0.01)
)

with row3_1, _lock:
    st.subheader("DataSet")
    with st.expander("DataSet 보기 👉"):
        st.markdown('**연령대별 인구 비율와 의료기관 수 현황**')
        st.dataframe(data)

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
                **❌ 모든 연도와 시도별 데이터를 종합해서 봤을 때, 
                의료기관 개폐업수와 총인구수, 연령층 비율은 뚜렷한 상관관계를 보이지 않았다.**

                → 의료기관 수와 중장년 비율, 노년 비율 사이에 유의미한 상관관계는 없었다.
    ''')
    st.markdown('')
    st.image(Image.open('img/df_hos_now_corr.png'))
    st.markdown('')
    st.markdown('***')
    st.markdown('')
    st.markdown('''                
                **❗️ 연도의 범위를 최근으로 한정할 수록 의료기관의 개업 폐업과 청년비율과의 상관계수가 점점 높아진다.**
                ''')
    st.markdown('')
    st.markdown('''
                **2012 - 2021 (세종특별자치시 출범 이후)**
                ''')
    st.image(Image.open('img/2012_2021.png'))
    st.markdown('')
    st.markdown('''
                **2017 - 2021 (최근 5년)**
                ''')
    st.image(Image.open('img/2017_2021.png'))
    st.markdown('')
    st.markdown('''
                **2017 - 2019 (코로나 발생 이전 3년)**
                ''')
    st.image(Image.open('img/2012_2021.png'))
    st.markdown('')
    st.markdown('''
                **2020 - 2021 (코로나 발생 이후 2년)**
                ''')
    st.image(Image.open('img/2012_2021.png'))
    st.markdown('''
                ***
                ''')
    st.subheader('Data Analysis')
    st.markdown('''
                `청년비율 (%)`= 20~39세 인구수 / 총인구수

                → 코로나 이후로 한정하면 개업폐업과 청년비율의 상관계수가 0.5로 올라간다.
                ''')
    st.markdown('')
    st.markdown('')
    st.markdown('''
                **❗️ 서울, 경기를 제외한 지역에서, 개업 폐업과 아동비율, 청소년비율간에는 음의 상관관계를 보여준다. 
                중장년비율은 폐업데이터와 양의 상관관계를 보여준다.**
                ''')
    st.markdown('''
                `아동비율 (%)`= 0~9세 인구수 / 총인구수

                `청소년비율 (%)`= 10~19세 인구수 / 총인구수
                ''')
    st.markdown('')
    st.markdown('')
    st.markdown('''
                **❗️ 의료기관 개업과 폐업 간의 상관관계는 매우 밀접하다.**
                ''')
    st.image(Image.open('img/open_close.png'))
    st.markdown('''
                `개업순위`  화성시, 성남시 분당구, 평택시, 남양주시

                `폐업순위` 성남시 분당구, 남양주시, 화성시, 평택시

                `현재 의료기관 순위` 남양주시, 성남시 분당구, 화성시, 평택시

                `인구수 순위` 화성시, 남양주시, 부천
                ''')
    st.markdown('')
    st.markdown('')
    st.markdown('')

# Folium_population
map1_space1, map1_1, map1_space2, map1_2, map1_space3 = st.columns(
    (0.01, 1, 0.05, 1, 0.01)
)

data_sigun = df_oc_seoul.set_index('시군구명')

with map1_1, _lock:
    st.markdown('🙆‍♀️ **서울 행정시별 개업지도 (2000년 이후)**')
    map_seoul_open = folium.Map(location=[37.5665, 127], zoom_start=10)

    choropleth = folium.Choropleth(geo_data=geo_str_seoul,
                                   data=data_sigun["개업"],
                                   columns=[data_sigun.index,
                                            data_sigun["개업"]],
                                   fill_opacity=0.8,
                                   line_opacity=0.8,
                                   fill_color="PuRd", key_on='feature.properties.SIG_KOR_NM').add_to(map_seoul_open)
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(fields=['SIG_KOR_NM'],
                                       aliases=['SIG_KOR_NM'],
                                       labels=False,
                                       localize=True,
                                       sticky=False,
                                       style="""
                                    background-color: #F0EFEF;
                                    border: 2px solid black;
                                    border-radius: 3px;
                                    box-shadow: 3px;
                                    """)
    )
    st_folium(map_seoul_open, width=400, height=400)


with map1_2, _lock:
    st.markdown('🙅‍♀️ **서울 행정시별 폐업지도 (2000년 이후)**')
    map_seoul_close = folium.Map(location=[37.5665, 127], zoom_start=10)

    choropleth = folium.Choropleth(geo_data=geo_str_seoul,
                                   data=data_sigun["폐업"],
                                   columns=[data_sigun.index,
                                            data_sigun["폐업"]],
                                   fill_opacity=0.8,
                                   line_opacity=0.8,
                                   fill_color="PuBuGn", key_on='feature.properties.SIG_KOR_NM').add_to(map_seoul_close)
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(fields=['SIG_KOR_NM'],
                                       aliases=['SIG_KOR_NM'],
                                       labels=False,
                                       localize=True,
                                       sticky=False,
                                       style="""
                                    background-color: #F0EFEF;
                                    border: 2px solid black;
                                    border-radius: 3px;
                                    box-shadow: 3px;
                                    """)
    )
    st_folium(map_seoul_close, width=400, height=400)


# Folium_population
map_space1, map_1, map_space2, map_2, map_space3 = st.columns(
    (0.01, 1, 0.05, 1, 0.01)
)


data_sigun = df_oc_gg.set_index('시군구명')

with map_1, _lock:
    st.markdown('🙆‍♀️ **경기도 행정시별 개업지도 (2000년 이후)**')
    map_gg_open = folium.Map(location=[37.5665, 127], zoom_start=8)

    choropleth = folium.Choropleth(geo_data=geo_str_gg,
                                   data=data_sigun["개업"],
                                   columns=[data_sigun.index,
                                            data_sigun["개업"]],
                                   fill_opacity=0.8,
                                   line_opacity=0.8,
                                   fill_color="PuRd", key_on='feature.properties.name').add_to(map_gg_open)
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(fields=['name'],
                                       aliases=['name'],
                                       labels=False,
                                       localize=True,
                                       sticky=False,
                                       style="""
                                    background-color: #F0EFEF;
                                    border: 2px solid black;
                                    border-radius: 3px;
                                    box-shadow: 3px;
                                    """)
    )
    st_folium(map_gg_open, width=400, height=400)
with map_2, _lock:
    st.markdown('🙅‍♀️ **경기도 행정시별 폐업지도 (2000년 이후)**')
    map_gg_close = folium.Map(location=[37.5665, 127], zoom_start=8)

    choropleth = folium.Choropleth(geo_data=geo_str_gg,
                                   data=data_sigun["폐업"],
                                   columns=[data_sigun.index,
                                            data_sigun["폐업"]],
                                   fill_opacity=0.8,
                                   line_opacity=0.8,
                                   fill_color="Greens", key_on='feature.properties.name').add_to(map_gg_close)
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(fields=['name'],
                                       aliases=['name'],
                                       labels=False,
                                       localize=True,
                                       sticky=False,
                                       style="""
                                    background-color: #F0EFEF;
                                    border: 2px solid black;
                                    border-radius: 3px;
                                    box-shadow: 3px;
                                    """)
    )
    st_folium(map_gg_close, width=400, height=400)


# Hypothesis Verification
a_space1, a_1, a_space2 = st.columns(
    (0.01, 1, 0.01)
)

with a_1, _lock:
    # st.subheader("Hypothesis Verification")

    st.markdown('')
    st.markdown('')
    st.markdown('''
                **❗️ 2000년도 이후 서울특별시는 의료기관 개업 대비 높은 폐업률을 보이고, 
                경기도는 낮은 폐업률을 보인다.**
                ''')
    # st.image(Image.open('img/open_close.png'))
    st.markdown('''
                → 의료기관의 개업과 폐업의 비율은 총인구수를 따라가는 것은 아니다.

                → 2000년 이후, 서울은 폐업이 개업에 비해 많은 편인데, 
                경기도는 폐업이 개업에 비해 적다. 
                이는 서울의 밀집화로 인한 의료기관간의 경쟁의 영향으로 보인다. 
                나머지 행정구역에서는 대체적으로 폐업이 높은 것으로 나타나고 있다.
                ''')


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
