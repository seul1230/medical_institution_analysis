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


# "가설 1 : 총 인구수 - 의료기관 수"
