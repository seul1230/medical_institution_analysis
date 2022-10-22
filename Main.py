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

st.set_page_config(
    page_title="Population And HealthCare Analysis",
    page_icon="🏥",
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


# Preparation to display plot
# matplotlib.use("agg")
_lock = RendererAgg.lock

# Seaborn style setup
# sns.set_style("darkgrid")
row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns(
    (0.1, 2, 0.2, 1, 0.1)
)

# Title
row0_1.title("Population And HealthCare Analysis")

with row0_2:
    st.write("")

row0_2.subheader(
    "GrowingTenten \n 🔟 성장발육엔텐텐"
)

# Introduction
row1_spacer1, row1_1, row1_spacer2 = st.columns([0.1, 3.2, 0.1])

with row1_1:
    st.subheader(
        '''
        **고령화, 그리고 코로나 19 이후 의료 인프라**
        '''
    )
    st.markdown(
        '''
        
        '''
    )
    st.markdown(
        '''
        코로나19 이후로 의료 인프라는 이루 말할 수 없이 중요한 사안이 되었다. 중환자 및 응급 병상 부족으로 인해 ~~
        그리고 가속화되는 **인구 고령화**로 인해 지역 간 의료 인프라 불균형 문제가 점점 심각해지고 있다. 
        이에 따라 우리 조는 미니프로젝트에서 분석하였던 **총 인구수**(2008 - 2021)를 바탕으로 의료기관 데이터에 접근하고자 한다.
        '''
    )
    st.markdown(
        '''
        우선 지역 별 **인구 수**에 따른 **현재 운영 중인 의료기관 수**(2022.06 기준)를 분석한다. 
        목표는 지역 별 인구 수에 따른 의료기관 비율을 비교 분석하고 도표와 지도를 통해 시각화하는 것이다. 
        인구수에 따른 **인프라 격차**가 발생할 것이라는 가설을 검증하고 현재 의료 인프라가 부족한 지역을 찾는다. 
        더하여, 의료시설 개업과 폐업 데이터를 분석하여 앞으로의 인프라 격차를 개선시킬 수 있는 방안을 모색해 본다.
        
        
        '''
    )
    st.markdown(
        '''
        
        '''
    )


@st.cache
def get_hypo_data(hypo_name):
    file_name = f"data/{hypo_name}.csv"
    data = pd.read_csv(file_name)
    return data


data = get_hypo_data('연령별_인구현황(2008_2021)')


# Display Data Set
row3_space1, row3_1, row3_space2 = st.columns(
    (0.01, 1, 0.01)
)

with row3_1, _lock:
    st.subheader("DataSet")
    with st.expander("DataSet 보기 👉"):
        st.markdown('**미니프로젝트_전국총인구수**')
        st.dataframe(data)

st.markdown(
    '''
    
    '''
)


# Footers
footer_space1, footer_1, footer_space2 = st.columns(
    (0.01, 1, 0.01)
)

with footer_1, _lock:
    st.markdown("***")
    st.markdown(
        "**성장발육엔텐텐** - 이재모, 조예슬, 임혜진, 김영민"
    )

    st.markdown(
        "**멋쟁이사자처럼 AI 스쿨 7기 미드프로젝트** : 2022년 10월 19일 ~ 23일"

    )
