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

# 가설 4 : 미용 목적 의료기관 비율
st.set_page_config(
    page_title="Hypothesis 4 : Beauty or Life - Medical Institutions",
    page_icon="💄",
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
geo_str_seoul = json.load(open('data/seoul.json'))
geo_str_gg = json.load(open('data/gg.json'))

# Preparation to display plot
# matplotlib.use("agg")
_lock = RendererAgg.lock

# Title
st.title("Hypothesis 4 : Beauty or Life - Medical Institutions")

st.subheader(
    '''
        **[ 가설 4 ]**  미용 목적 의료기관과 필수 의료 목적 의료기관
        '''
)


# Introduction
row1_spacer1, row1_1, row1_spacer2 = st.columns([0.1, 3.2, 0.1])

with row1_1, _lock:
    st.markdown(
        '''
        서울시 강남구에 의료기관이 제일 많이 집중되어 있는 이유는 강남에는 미용목적 의료기관이 몰려있기 때문일 것이다.
        '''
    )

    st.markdown(
        '''
        '''
    )
    st.markdown(
        '''
        🔍 `미용 목적 의료기관` : 성형외과 / 내과

        🔍 `필수 의료 목적 의료기관` : 치과 / 산부인과 / 내과 / 외과 / 안과
        
        '''
    )
    st.markdown(
        '''
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


# data = get_hypo_data('df_now_hos')
data = get_hypo_data('df_oc_seoul_total')
df_cosmetics = get_hypo_data('df_cosmetics')
data_gg = get_hypo_data('df_oc_gg_total')

# Display Data Set
row3_space1, row3_1, row3_space2 = st.columns(
    (0.01, 1, 0.01)
)

with row3_1, _lock:
    st.subheader("DataSet")
    with st.expander("DataSet 보기 👉"):
        st.markdown('**서울시 의료기관 미용 / 비미용 분류**')
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

a_space1, a_1, a_space2, a_2, a_space3 = st.columns(
    (0.01, 1, 0.05, 1, 0.01)
)
with a_1, _lock:
    st.markdown('**시군구별 성형외과 비율 TOP5**')
    st.markdown('')
    st.markdown('')
    st.image(Image.open('img/beauty_pie.png'), width=300)  # mz_medical_corr
    st.markdown('')
with a_2, _lock:

    df_c = df_cosmetics.set_index('시도명')

    for idx, sigun_dict in enumerate(geo_str_korea['features']):
        sigun_id = sigun_dict['properties']['CTP_KOR_NM']
        dep_ratio = np.around(df_cosmetics.loc[df_cosmetics['시도명']
                                               == sigun_id, '요양종별비율(%)'].iloc[0], 2)
        txt = f'<b><h4>{sigun_id}</h4></b>성형외과 비율 : {dep_ratio} %'
        geo_str_korea['features'][idx]['properties']['dep_ratio'] = txt

    st.markdown('**전국 성형외과 비율**')
    map_cosmetics = folium.Map(
        location=[36.8, 127.5], zoom_start=5.5)

    choropleth = folium.Choropleth(geo_data=geo_str_korea,
                                   data=df_c['요양종별비율(%)'],
                                   columns=[df_c.index,
                                            df_c['요양종별비율(%)']],
                                   fill_color='Oranges',
                                   fill_opacity=0.7,
                                   line_opacity=0.7,
                                   key_on='feature.properties.CTP_KOR_NM',
                                   legend_name='요양종별비율(%)').add_to(map_cosmetics)
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(fields=['dep_ratio'],
                                       aliases=['dep_ratio'],
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
    st_folium(map_cosmetics, width=300, height=300)

con_space1, con_1, con_space2 = st.columns(
    (0.01, 1, 0.01)
)

with con_1, _lock:

    st.markdown('''
                **⭕️ 강남구의 성형외과, 외과의 비율은 높은 편이다.**

                → 강남구의 성형외과 비율은 13.3%, 피부과 비율은 4.7%로 국내 시군구 중에서 가장 높은 비율을 차지하고 있다.
                ''')

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

data_sigun = data.set_index('시군구명')
with map_1, _lock:
    st.markdown('💄 **서울 미용목적 의료기관 비율**')

    for idx, sigun_dict in enumerate(geo_str_seoul['features']):
        sigun_id = sigun_dict['properties']['SIG_KOR_NM']
        beauty_ratio = np.around(data.loc[data['시군구명']
                                          == sigun_id, '미용목적_병원_비율'].iloc[0], 2)
        txt = f'<b><h4>{sigun_id}</h4></b>미용 목적 의료기관 비율 : {beauty_ratio} %'
        geo_str_seoul['features'][idx]['properties']['beauty_ratio'] = txt

    map_seoul_beauty = folium.Map(location=[37.5665, 127], zoom_start=10)

    choropleth = folium.Choropleth(geo_data=geo_str_seoul,
                                   data=data_sigun["미용목적_병원_비율"],
                                   columns=[data_sigun.index,
                                            data_sigun["미용목적_병원_비율"]],
                                   fill_opacity=0.8,
                                   line_opacity=0.8,
                                   fill_color="Blues", key_on='feature.properties.SIG_KOR_NM').add_to(map_seoul_beauty)
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(fields=['beauty_ratio'],
                                       aliases=['beauty_ratio'],
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
    st_folium(map_seoul_beauty, width=400, height=400)


with map_2, _lock:

    st.markdown('🩺 **서울 필수 목적 의료기관 비율**')

    for idx, sigun_dict in enumerate(geo_str_seoul['features']):
        sigun_id = sigun_dict['properties']['SIG_KOR_NM']
        non_beauty_ratio = np.around(data.loc[data['시군구명']
                                              == sigun_id, '비미용목적_병원_비율'].iloc[0], 2)

        txt = f'<b><h4>{sigun_id}</h4></b>필수 의료 목적 의료기관 비율 : {non_beauty_ratio} %'
        geo_str_seoul['features'][idx]['properties']['non_beauty_ratio'] = txt

    map_seoul_non_beauty = folium.Map(location=[37.5665, 127], zoom_start=10)

    choropleth = folium.Choropleth(geo_data=geo_str_seoul,
                                   data=data_sigun["비미용목적_병원_비율"],
                                   columns=[data_sigun.index,
                                            data_sigun["비미용목적_병원_비율"]],
                                   fill_opacity=0.8,
                                   line_opacity=0.8,
                                   fill_color="Blues", key_on='feature.properties.SIG_KOR_NM').add_to(map_seoul_non_beauty)
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(fields=['non_beauty_ratio'],
                                       aliases=['non_beauty_ratio'],
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
    st_folium(map_seoul_non_beauty, width=400, height=400)

st.markdown('''
            ***
            ''')


map2_space1, map2_1, map2_space2, map2_2, map2_space3 = st.columns(
    (0.01, 1, 0.05, 1, 0.01)
)

data_gg_sigun = data_gg.set_index('시군구명')
with map2_1, _lock:
    st.markdown('💄 **경기도 미용목적 의료기관 비율**')

    for idx, sigun_dict in enumerate(geo_str_gg['features']):
        sigun_id = sigun_dict['properties']['name']
        beauty_ratio = np.around(data_gg.loc[data_gg['시군구명']
                                             == sigun_id, '미용목적_병원_비율'].iloc[0], 2)
        txt = f'<b><h4>{sigun_id}</h4></b>미용 목적 의료기관 비율 : {beauty_ratio} %'
        geo_str_gg['features'][idx]['properties']['beauty_ratio'] = txt

    map_gg_beauty = folium.Map(location=[37.5665, 127], zoom_start=8)

    choropleth = folium.Choropleth(geo_data=geo_str_gg,
                                   data=data_gg_sigun["미용목적_병원_비율"],
                                   columns=[data_gg_sigun.index,
                                            data_gg_sigun["미용목적_병원_비율"]],
                                   fill_opacity=0.8,
                                   line_opacity=0.8,
                                   fill_color="PuBuGn", key_on='feature.properties.name').add_to(map_gg_beauty)
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(fields=['beauty_ratio'],
                                       aliases=['beauty_ratio'],
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
    st_folium(map_gg_beauty, width=400, height=400)


with map2_2, _lock:

    st.markdown('🩺 **경기도 필수 목적 의료기관 비율**')

    for idx, sigun_dict in enumerate(geo_str_gg['features']):
        sigun_id = sigun_dict['properties']['name']
        non_beauty_ratio = np.around(data_gg.loc[data_gg['시군구명']
                                                 == sigun_id, '비미용목적_병원_비율'].iloc[0], 2)
        txt = f'<b><h4>{sigun_id}</h4></b>필수 의료 목적 의료기관 비율 : {non_beauty_ratio} %'
        geo_str_gg['features'][idx]['properties']['non_beauty_ratio'] = txt

    map_gg_non_beauty = folium.Map(location=[37.5665, 127], zoom_start=8)

    choropleth = folium.Choropleth(geo_data=geo_str_gg,
                                   data=data_gg_sigun["비미용목적_병원_비율"],
                                   columns=[data_gg_sigun.index,
                                            data_gg_sigun["비미용목적_병원_비율"]],
                                   fill_opacity=0.8,
                                   line_opacity=0.8,
                                   fill_color="PuBuGn", key_on='feature.properties.name').add_to(map_gg_non_beauty)
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(fields=['non_beauty_ratio'],
                                       aliases=['non_beauty_ratio'],
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
    st_folium(map_gg_non_beauty, width=400, height=400)

analy_space1, analy_1, analy_space2 = st.columns(
    (0.1, 2, 0.1)
)
with analy_1, _lock:
    st.markdown('''
                → 서울특별시의 경우 `의료기관수`와 `다른 인프라`의 상관관계는 적다고 볼 수 있고, 
                **강남구**의 경우 미용목적의료기관이 집중되어있는 등 의료인프라의 상관관계는 다른 인프라의 요인보다 특히 **경제적 요인**이 크다고 할 수 있다. 
                경기도의 경우도 같은 맥락으로 **수원팔달구**와 **성남**에서 미용목적 의료기관의 비율이 높은 것을 확인할 수 있었다.
                ''')
    st.markdown('''
                ''')


st.markdown('''
            ***
            ''')


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
