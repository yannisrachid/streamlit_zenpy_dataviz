# Import of required libraries
import streamlit as st
from connection import *
from main import *
import logging
from datetime import date
from PIL import Image
from process import *

# To have the current date
today = date.today()

# to speed up the execution time of the function
@st.cache
def convert_df(df):
    """
    input: a pandas DataFrame
    returns the csv file with utf-8 encoding
    """
    return df.to_csv().encode('utf-8')

# Display the title
# st.title('Meetdeal Data Visualisation')
st.markdown("<h1 style='text-align: center; color: white;'>Entreprise Data Visualisation</h1>", unsafe_allow_html=True)
# Load our params (credentials to connect to zenpy and to get the brands_id dicts)

# the dictionary of months is written in order
months = {'janvier': 1, 'février': 2, 'mars': 3, 'avril': 4, 'mai': 5, 'juin': 6, 'juillet': 7, 'août': 8, 'septembre': 9, 'octobre': 10, 'novembre': 11, 'décembre': 12}

# Display the MeetDeal logo
logo = Image.open('../data/logo_entreprise.png')
st.sidebar.image(logo)

# Connection to zenpy
zenpy_client = zpc
st.sidebar.write('Connexion à zenpy réussie !')
# Display of fields to select a brand, month and year, with some verifications
brand = st.sidebar.selectbox('Choisissez une marque', ('brand1', 'brand2', 'brand3', 'brand4', 'brand5', 'brand6', 'brand7', 'brand8'))
month = st.sidebar.selectbox('Choisissez un mois', tuple(months.keys()))
m = months[month]
year = 2022
if m>today.month:
    st.sidebar.write("Les données ne sont pas encore disponibles pour le mois sélectionné")
    m=0
bid = brands[brand]
choices_bid = st.sidebar.multiselect("Brand ID", bid)
if type(choices_bid)!=list:
    choices_bid = [choices_bid]

# if everything is alright, loading data, display the download button and displaying datavizs
if choices_bid and brand and m:
    st.sidebar.write("Chargement des données...")
    my_bar = st.sidebar.progress(0.0)
    df = process_period(zenpy_client, choices_bid, m, year, my_bar)
    csv = convert_df(df)
    st.sidebar.download_button("Télécharger les données en csv", csv, "data_{}_{}_{}.csv".format(brand, month, year), "text/csv", key='download-csv')
    st.sidebar.write("Données chargées avec succès ! Génération des visualisations...")

    df['url'] = df['url'].apply(clean_url)
    st.pyplot(get_url_test_distrib(df, brand))
    st.pyplot(get_test_lq_distrib(df, brand))
    st.pyplot(get_test_blq_distrib(df, brand))
    st.pyplot(get_am_distrib(df, brand))
    st.pyplot(get_am_bis_distrib(df, brand))
    st.pyplot(get_pm_distrib(df, brand))
    st.pyplot(get_time_df(df, brand))
    st.pyplot(get_time_intervals(df, brand))
    st.pyplot(get_wordcloud(df, brand))
