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
    page_title="Hypothesis 2 : Ages ratio - Medical Institutions",
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
geo_str_korea = json.load(open('data/korea.json'))

# Preparation to display plot
# matplotlib.use("agg")
_lock = RendererAgg.lock

# Title
st.title("Hypothesis 2 : Ages ratio - Medical Institutions")

st.subheader(
    '''
        **[ 가설 2 ]**  연령별 인구 비율과 의료기관 분포
        '''
)


# Introduction
row1_spacer1, row1_1, row1_spacer2 = st.columns([0.1, 3.2, 0.1])

with row1_1, _lock:
    st.markdown(
        '''
        고령화가 많이 진행된 지역에 의료기관이 부족할 것으로 예상한다.
        '''
    )

    st.markdown(
        '''
        '''
    )
    st.markdown(
        '''
        🔍 `중장년 비율(%)`= 40~69세 인구수 / `총인구수`

        🔍 `노년 비율(%)`= 70세 이상 인구수 / `총인구수`
        
        '''
    )
    st.markdown(
        '''
        '''
    )

    st.markdown(
        '''
        각 연령 구분 별로 얻은 인구 비율(%)과 `의료기관수`와의 관계에 대해 알아보자.\n
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
                **❌ 고령화 비율과 의료기관수는 뚜렷한 상관관계를 보이지 않는다.**

                → 의료기관 수와 중장년 비율, 노년 비율 사이에 유의미한 상관관계는 없었다.
                ''')
    st.image(Image.open('img/elder_medical_corr.png'))  # mz_medical_corr
    st.markdown('''
                ***
                ''')


# Display Visualization
visual_space1, visual_1, visual_space2 = st.columns(
    (0.01, 1, 0.01)
)

pop_hos_now = data[(data['시도명'] != '서울특별시') & (
    data['시도명'] != '경기도')].sort_values('노년비율 (%)', ascending=False)


with visual_1, _lock:
    st.subheader("Data Visualization")

    st.markdown('''
                👴🏻 **노년층 비율 순위에 따른 의료기관 수 (전국)**
                ''')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    # fig, ax = plt.subplots(figsize=(25, 5))
    data.plot.bar(x="시도명", y="의료기관수",
                  figsize=(20, 5), rot=0)
    st.pyplot()

    st.markdown('''
                👴🏻 **노년층 비율 순위에 따른 의료기관 수 (서울, 경기 제외)**
                ''')

    # fig, ax = plt.subplots(figsize=(25, 5))
    pop_hos_now.plot.bar(x="시도명", y="의료기관수",
                         figsize=(20, 5), rot=0)
    st.pyplot()


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

with map_2, _lock:
    st.markdown('👥 **행정구역별 노년 비율**')

    # 행정구역별 노년비율
    map_elder = folium.Map(location=[36.5861, 127], zoom_start=6)

    choropleth = folium.Choropleth(geo_data=geo_str_korea,
                                   data=data_sido['노년비율 (%)'],
                                   columns=[data_sido.index,
                                            data_sido['노년비율 (%)']],
                                   fill_color='PuRd',
                                   fill_opacity=0.7,
                                   line_opacity=0.5,
                                   #                   tooltip=folium.features.GeoJsonTooltip(fields=['neighbourhood_cleansed', 'price'],
                                   #                                                          labels=True,
                                   #                                                          sticky=False),
                                   key_on='feature.properties.CTP_KOR_NM').add_to(map_elder)

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
    st_folium(map_elder, width=400, height=400)


with map_1, _lock:

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
    st.image(Image.open('img/mz_medical_corr.png'))
    st.markdown('')
    st.markdown(
        '''
        상관 계수를 구했을 때, 청년 비율과 의료기관 수의 상관관계가 **0.53** 정도로
        다른 연령층에 비해 높은 양의 상관관계가 있다는 것을 확인했다.
        '''
    )
    st.markdown(
        '''
        '''
    )

    st.markdown('''
                🧑🏻 **청년 비율 순위에 따른 의료기관 수 (전국)**
                ''')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    # fig, ax = plt.subplots(figsize=(25, 5))
    data.plot.bar(x="시도명", y="의료기관수",
                  figsize=(20, 5), rot=0)
    st.pyplot()
    st.markdown(
        '''
        '''
    )
    st.markdown('''
                🧑🏻 **청년 비율 순위에 따른 의료기관 수 (서울, 경기 제외)**
                ''')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    # fig, ax = plt.subplots(figsize=(25, 5))
    pop_hos_now.plot.bar(x="시도명", y="의료기관수",
                         figsize=(20, 5), rot=0)
    st.pyplot()


# Map Visualization
m1_space1, m1_1, m1_space2 = st.columns(
    (0.01, 1, 0.01)
)
# with m1_1, _lock:
# st.subheader("Map Visualization")

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

    st.markdown('🔍 **행정구역별 청년비율 현황**')

    # 행정구역별 인구 1만 명 당 의료기관 수
    map_mz_medical = folium.Map(
        location=[36.5861, 127], zoom_start=6)

    choropleth = folium.Choropleth(geo_data=geo_str_korea,
                                   data=data_sido['청년비율 (%)'],
                                   columns=[data_sido.index,
                                            data_sido['청년비율 (%)']],
                                   fill_color='PuRd',
                                   fill_opacity=0.7,
                                   line_opacity=0.5,
                                   #                   tooltip=folium.features.GeoJsonTooltip(fields=['neighbourhood_cleansed', 'price'],
                                   #                                                          labels=True,
                                   #                                                          sticky=False),
                                   key_on='feature.properties.CTP_KOR_NM').add_to(map_mz_medical)

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
    st_folium(map_mz_medical, width=400, height=400)

further_spacer1, further_1, further_spacer2 = st.columns((0.01, 1, 0.01))
with further_1, _lock:

    st.subheader('**Conclusion**')
    st.markdown(
        '''
        
        시각화를 해보니 서울, 경기도의 청년 비율이 높아 연령대별 상관관계 중에 가장 높은 것으로 추정한다. 
        그러나 경제인구가 밀집된 서울, 경기 지역의 데이터를 제외하고 보면 **청년 연령층과의 상관계수도 유의미하지 않다**고 판단하였다.
        
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
