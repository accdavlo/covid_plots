import streamlit as st
import app_italy
import app_time_integration
import about
import home
import app_world_data
import app_convolution

def app_loading():
    st.set_page_config(page_title="Analisi Pandemia")
    st.write("# Analisi sui dati della pandemia")

    st.sidebar.title("Cosa visualizzare")

    PAGES = {
        "Home": home,
        "Dati Italia": app_italy,
        "Dati Mondo": app_world_data,
        "Convoluzione Casi":app_convolution,
        "Modelli e Simulazioni": app_time_integration,
        "About": about,
    }

    page = st.sidebar.radio("", list(PAGES.keys()))
    PAGES[page].app()

app_loading()
