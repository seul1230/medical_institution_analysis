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

st.set_page_config(
    page_title="Population And Medical Institutions Analysis",
    page_icon="π₯",
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
row0_1.title("Population And Medical Institutions Analysis")

with row0_2:
    st.write("")

row0_2.subheader(
    "GrowingTenten \n π μ±μ₯λ°μ‘μνν"
)
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')

# Introduction
row1_spacer1, row1_1, row1_spacer2 = st.columns([0.1, 3.2, 0.1])

with row1_1:
    st.subheader(
        '''
        **κ³ λ Ήν, κ·Έλ¦¬κ³  μ½λ‘λ 19 μ΄ν μλ£ μΈνλΌ**
        '''
    )
# img_space1, img_1, img_space2, img_2, img_space3 = st.columns(
#     (0.1, 1, 0.05, 1, 0.1)
# )

row2_spacer1, row2_1, row2_spacer2 = st.columns([0.1, 3.2, 0.1])

with row2_1:
    st.markdown(
        '''
        μ½λ‘λ19 μ΄νλ‘ μλ£ μΈνλΌλ μ΄λ£¨ λ§ν  μ μμ΄ μ€μν μ¬μμ΄ λμλ€. μ€νμ λ° μκΈ λ³μ λΆμ‘± λ¬Έμ κ° μ¬κ°ν΄μ§κ³ ,
         κ°μνλλ **μΈκ΅¬ κ³ λ Ήν**λ‘ μΈν΄ μ§μ­ κ° μλ£ μΈνλΌ λΆκ· ν λ¬Έμ κ° μ μ  μ¬κ°ν΄μ§κ³  μλ€.
        μ΄μ λ°λΌ μ°λ¦¬ μ‘°λ λ―Έλνλ‘μ νΈμμ λΆμνμλ **μ΄ μΈκ΅¬μ**(2008 - 2021)λ₯Ό λ°νμΌλ‘ μλ£κΈ°κ΄ λ°μ΄ν°μ μ κ·Όνκ³ μ νλ€.
        '''
    )

img_space1, img_1, img_space2 = st.columns(
    (0.3, 1, 0.3)
)
with img_1, _lock:
    st.image(Image.open('img/background.png'))
#     st.image(Image.open('img/background_1.png'))
# with img_2, _lock:
#     st.image(Image.open('img/background_2.png'))
#     st.image(Image.open('img/background_3.png'))


@st.cache
def get_hypo_data(hypo_name):
    file_name = f"data/{hypo_name}.csv"
    data = pd.read_csv(file_name)
    return data


# data = get_hypo_data('αα§α«αα§αΌαα§α―_αα΅α«αα?αα§α«ααͺαΌ(2008_2021)')
data = pd.read_csv('data/age_population(2008_2021).csv')


# Display Data Set
row3_space1, row3_1, row3_space2 = st.columns(
    (0.01, 1, 0.01)
)

with row3_1, _lock:
    # st.markdown(
    #     '''
    #     μ½λ‘λ19 μ΄νλ‘ μλ£ μΈνλΌλ μ΄λ£¨ λ§ν  μ μμ΄ μ€μν μ¬μμ΄ λμλ€. μ€νμ λ° μκΈ λ³μ λΆμ‘± λ¬Έμ κ° μ¬κ°ν΄μ§κ³ ,
    #      κ°μνλλ **μΈκ΅¬ κ³ λ Ήν**λ‘ μΈν΄ μ§μ­ κ° μλ£ μΈνλΌ λΆκ· ν λ¬Έμ κ° μ μ  μ¬κ°ν΄μ§κ³  μλ€.
    #     μ΄μ λ°λΌ μ°λ¦¬ μ‘°λ λ―Έλνλ‘μ νΈμμ λΆμνμλ **μ΄ μΈκ΅¬μ**(2008 - 2021)λ₯Ό λ°νμΌλ‘ μλ£κΈ°κ΄ λ°μ΄ν°μ μ κ·Όνκ³ μ νλ€.
    #     '''
    # )

    st.markdown(
        '''
        μ°μ  μ§μ­ λ³ **μΈκ΅¬ μ**μ λ°λ₯Έ **νμ¬ μ΄μ μ€μΈ μλ£κΈ°κ΄ μ**(2022.06 κΈ°μ€)λ₯Ό λΆμνλ€. 
        λͺ©νλ μ§μ­ λ³ μΈκ΅¬ μμ λ°λ₯Έ μλ£κΈ°κ΄ λΉμ¨μ λΉκ΅ λΆμνκ³  λνμ μ§λλ₯Ό ν΅ν΄ μκ°ννλ κ²μ΄λ€. 
        μΈκ΅¬μμ λ°λ₯Έ **μΈνλΌ κ²©μ°¨**κ° λ°μν  κ²μ΄λΌλ κ°μ€μ κ²μ¦νκ³  νμ¬ μλ£ μΈνλΌκ° λΆμ‘±ν μ§μ­μ μ°Ύλλ€. 
        λνμ¬, μλ£μμ€ κ°μκ³Ό νμ λ°μ΄ν°λ₯Ό λΆμνμ¬ μμΌλ‘μ μΈνλΌ κ²©μ°¨λ₯Ό κ°μ μν¬ μ μλ λ°©μμ λͺ¨μν΄ λ³Έλ€.
        
        
        '''
    )

    st.markdown(
        '''
        
        '''
    )
    st.subheader("DataSet")
    with st.expander("MiniProject Final DataSet λ³΄κΈ° π"):
        st.markdown('**λ―Έλνλ‘μ νΈκ²°κ³Όλ¬Ό_μ κ΅­μ΄μΈκ΅¬μ**')
        st.dataframe(data)

st.markdown('')
st.markdown('')
hypo_space1, hypo_1, hypo_space2 = st.columns(
    (0.01, 1, 0.01)
)

with hypo_1, _lock:
    st.subheader("Hypothesis")
    st.markdown('''
            1.  μ΄μΈκ΅¬μκ° μ μ νμ κ΅¬μ­μ νμ‘΄νλ μλ£κΈ°κ΄μκ° λΆμ‘±ν  κ²μΌλ‘ μμνλ€
            2.  κ³ λ Ήνκ° λ§μ΄ μ§νλ μ§μ­μ νμ‘΄νλ μλ£κΈ°κ΄μ΄ λΆμ‘±ν  κ²μ΄λ€
            3.  μλ£κΈ°κ΄μλ λ€λ₯ΈλΆμΌ(λ¬Έν, νκ²½, κ΅μ‘)μ μΈνλΌμλ μκ΄κ΄κ³κ° μμ κ²μ΄λ€
            4.  μμΈμ κ°λ¨κ΅¬μ μλ£κΈ°κ΄μ΄ μ μΌ λ§μ΄ μ§μ€λμ΄ μλ μ΄μ λ κ°λ¨μλ λ―Έμ©λͺ©μ  μλ£κΈ°κ΄μ΄ λͺ°λ €μκΈ° λλ¬ΈμΌ κ²μ΄λ€.
            5.  μ°λλ³ μλ£κΈ°κ΄ κ°νμμμ μ΄μΈκ΅¬μ, μ°λ ΉμΈ΅ λΉμ¨μ μκ΄κ΄κ³κ° μμ κ²μ΄λ€.
    
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
        π¦

        **μ±μ₯λ°μ‘μνν** - μ΄μ¬λͺ¨, μ‘°μμ¬, μνμ§, κΉμλ―Ό
        '''
    )

    st.markdown(
        "**λ©μμ΄μ¬μμ²λΌ AI μ€μΏ¨ 7κΈ° λ―Έλνλ‘μ νΈ** : 2022.10.19 - 2022.10.23"

    )
