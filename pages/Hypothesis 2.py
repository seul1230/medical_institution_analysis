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
    page_title="Hypothesis 1 : Population - Healthcare Facilities",
    page_icon="👥",
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

# Preparation to display plot
# matplotlib.use("agg")
_lock = RendererAgg.lock

# Title
st.title("Hypothesis 1 : Population - Healthcare Facilities")

st.subheader(
    '''
        **[ 가설 1 ]**  인구 수와 의료기관 분포
        '''
)


# Introduction
row1_spacer1, row1_1, row1_spacer2 = st.columns([0.1, 3.2, 0.1])

with row1_1, _lock:
    st.markdown(
        '''
        총 인구 수가 적은 행정구역은 의료기관이 적을 것으로 예상한다.\n
        2022년 6월 기준 영업 중인 **의료기관 현황**과 
        행정안전부 주민등록 **인구 통계** 데이터를 받아와 전처리하여 분석하였다.
        '''
    )
    st.markdown(
        '''

        '''
    )


@ st.cache
def get_hypo_data(hypo_name):
    file_name = f"data/{hypo_name}.csv"
    data = pd.read_csv(file_name)
    return data


data = get_hypo_data('df_now_hos')


# Display Data Set
row3_space1, row3_1, row3_space2 = st.columns(
    (0.01, 1, 0.01)
)

with row3_1, _lock:
    st.subheader("DataSet")
    with st.expander("DataSet 보기 👉"):
        st.markdown('**연령대별 인구수와 의료기관 수 현황**')
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
                **⭕️ 행정구역의 총인구수와 의료기관수는 양의 상관관계가 있다.**

                → 행정구역의 `총인구수`와 `의료기관수`는 0.96 양의 상관관계를 가지기 때문에
                총인구수가 많을수록 의료 인프라가 잘 마련되어 있다고 볼 수 있다.
                ''')
    st.image(Image.open('img/df_pop_med_corr.png'))
    st.markdown('''
                ***
                ''')


# Display Visualization
visual_space1, visual_1, visual_space2 = st.columns(
    (0.01, 1, 0.01)
)

with visual_1, _lock:
    st.subheader("Data Visualization")

    st.markdown('''
                👥 **행정구역별 총 인구 수**
                ''')

    fig, ax = plt.subplots(figsize=(25, 5))
    sns.lineplot(data=data.sort_values(
        '의료기관수', ascending=False), x="시도명", y="총인구수")

    ax.set_title("행정구역별 총 인구 수")
    st.pyplot(fig)

    st.markdown('''
                ''')

    st.markdown('''
                🏥 **행정구역별 의료기관 수**
                ''')

    fig, ax = plt.subplots(figsize=(25, 5))
    sns.barplot(data=data.sort_values(
        '의료기관수', ascending=False), x="시도명", y="의료기관수")
    ax.set_title("행정구역별 의료기관 수")
    st.pyplot(fig)


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
    (0.01, 1, 0.05, 1, 0.01)
)

data_sido = data.set_index('시도명')

with map_1, _lock:
    st.markdown('👥 **행정구역별 총 인구 수 현황**')

    map_pop = folium.Map(
        location=[36.5861, 127], zoom_start=6)
    choropleth = folium.Choropleth(geo_data=geo_str_korea,
                                   data=data_sido['총인구수'],
                                   columns=[data_sido.index,
                                            data_sido['총인구수']],
                                   fill_color='PuRd',
                                   fill_opacity=0.7,
                                   line_opacity=0.5,
                                   #                   tooltip=folium.features.GeoJsonTooltip(fields=['neighbourhood_cleansed', 'price'],
                                   #                                                          labels=True,
                                   #                                                          sticky=False),
                                   key_on='feature.properties.CTP_KOR_NM').add_to(map_pop)

    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(fields=['CTP_KOR_NM'],
                                       aliases=['CTP_KOR_NM'],
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
    st_folium(map_pop, width=400, height=400)


with map_2, _lock:

    st.markdown('🏥 **행정구역별 의료기관 수 현황**')
    map_medical = folium.Map(
        location=[36.5861, 127], zoom_start=6)
    choropleth = folium.Choropleth(geo_data=geo_str_korea,
                                   data=data_sido['의료기관수'],
                                   columns=[data_sido.index,
                                            data_sido['의료기관수']],
                                   fill_color='PuRd',
                                   fill_opacity=0.7,
                                   line_opacity=0.5,
                                   key_on='feature.properties.CTP_KOR_NM').add_to(map_medical)

    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(fields=['CTP_KOR_NM'],
                                       aliases=['CTP_KOR_NM'],
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
    st_folium(map_medical, width=400, height=400)

st.markdown('''
            ***
            ''')

# Further Analysis
more_spacer1, more_1, more_spacer2 = st.columns((0.01, 1, 0.01))

with more_1, _lock:
    st.subheader('Further Analysis')
    st.markdown(
        '''
        총인구수가 많을수록(서울, 경기지역) 의료 인프라의 수준이 높다는 것은 접근하기 쉬운 관점이다. 
        따라서 `의료기관수`가 절대적인 지표라면, 총 인구수에 따라 상대적인 `인구 1만명당 의료기관 수` 
        지표를 구하여 분석을 해보았다.
        '''
    )
    st.markdown(
        '''
        '''
    )
    st.markdown(
        '''
        
        🔎 `1만명당의료기관수` = `의료기관수` / `총인구수` * 10000
        
        '''
    )
    st.markdown(
        '''
        '''
    )
    st.markdown(
        '''
        `의료기관수`가 절대적 차이를 보여주는 지표였다면, 
        인구 `1만명당의료기관수`는 행정구역의 총 인구수를 기준으로 가공한 지표이기 때문에, 
        상대적인 차이를 보여주는 지표라고 볼 수 있다.
        '''
    )

st.markdown('''
            ***
            ''')

# Map Visualization
m1_space1, m1_1, m1_space2 = st.columns(
    (0.01, 1, 0.01)
)
with m1_1, _lock:
    st.subheader("Map Visualization")

# Folium_population
map2_space1, map2_1, map2_space2, map2_2, map2_space3 = st.columns(
    (0.01, 1, 0.05, 1, 0.01)
)

with map2_1, _lock:
    st.markdown('🏥 **행정구역별 의료기관 수 현황**')
    map_medical_1 = folium.Map(
        location=[36.5861, 127.1], zoom_start=6)
    choropleth = folium.Choropleth(geo_data=geo_str_korea,
                                   data=data_sido['의료기관수'],
                                   columns=[data_sido.index,
                                            data_sido['의료기관수']],
                                   fill_color='PuRd',
                                   fill_opacity=0.7,
                                   line_opacity=0.5,
                                   key_on='feature.properties.CTP_KOR_NM').add_to(map_medical_1)

    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(fields=['CTP_KOR_NM'],
                                       aliases=['CTP_KOR_NM'],
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
    st_folium(map_medical_1, width=400, height=400)


with map2_2, _lock:

    st.markdown('🔍 **인구 1만 명 당 의료기관 수 현황**')

    # 행정구역별 인구 1만 명 당 의료기관 수
    map_10000_medical = folium.Map(
        location=[36.5861, 127], zoom_start=6)

    choropleth = folium.Choropleth(geo_data=geo_str_korea,
                                   data=data_sido['1만명당의료기관수'],
                                   columns=[data_sido.index,
                                            data_sido['1만명당의료기관수']],
                                   fill_color='PuRd',
                                   fill_opacity=0.7,
                                   line_opacity=0.5,
                                   #                   tooltip=folium.features.GeoJsonTooltip(fields=['neighbourhood_cleansed', 'price'],
                                   #                                                          labels=True,
                                   #                                                          sticky=False),
                                   key_on='feature.properties.CTP_KOR_NM').add_to(map_10000_medical)

    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(fields=['CTP_KOR_NM'],
                                       aliases=['CTP_KOR_NM'],
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
    st_folium(map_10000_medical, width=400, height=400)

further_spacer1, further_1, further_spacer2 = st.columns((0.01, 1, 0.01))
with further_1, _lock:
    st.markdown('''
                → `의료기관수`가 **상위권**에 속했던 **인천광역시**, **경상남도**, **경기도**가 
                인구 `1만명당의료기관수`에서는 **하위권**에 속한다.
                
                → **그 중 경기도의 변화가 눈에 띈다.**
                
                워낙 인구 수가 많아서  `인구 1만 명당 의료기관수`가 **하위권**으로 내려온 것으로 보인다.
                **경기도**는 `의료기관수`가 많은 행정구역이지만, 특정 시군구 별로 의료기관의 보급이 떨어지는 의료 사각지대가 존재할 것이다. 
                **인천** 또한 의료기관 부족에 관련한 기사를 쉽게 접할 수 있었다.


                ''')


# Footers
footer_space1, footer_1, footer_space2 = st.columns(
    (0.01, 1, 0.01)
)

with footer_1, _lock:
    st.markdown('''
                ***
                ''')
    st.markdown(
        "**성장발육엔텐텐** - 이재모, 조예슬, 임혜진, 김영민"
    )

    st.markdown(
        "**멋쟁이사자처럼 AI 스쿨 7기 미드프로젝트** : 2022.10.19 - 2022.10.23"

    )
