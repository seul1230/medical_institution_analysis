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
    page_title="Hypothesis 1 : Population - Healthcare Facilities",
    page_icon="🏥",
    layout="wide",
)

# "가설 1 : 총 인구수 - 의료기관 수",
# "가설 2 : 고령화 비율 - 의료기관 수",
# "가설 3 : 인구수 - 의료기관 개폐업",
# "가설 4 : 기본 인프라 - 의료기관 수",
# "가설 5 : 미용 목적 의료기관 비율"
