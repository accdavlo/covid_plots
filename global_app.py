import streamlit as st
from app_time_integration import run_model_and_simulation
from app_italy import run_italian_data
from app_world_data import run_world
from about import about
st.set_page_config(page_title="Analisi Pandemia")

def main():
    st.sidebar.title("Cosa visualizzare")
    app_mode = st.sidebar.selectbox("Scegli l'argomento",
        ["Dati Italiani", "Modelli e simulazioni", "Dati Mondo", "About"])

    if app_mode == "Modelli e simulazioni":
        run_model_and_simulation()
    elif app_mode == "Dati Italiani":
        run_italian_data()
    elif app_mode == "Dati Mondo":
        run_world()
    elif app_mode == "About":
        about()

if __name__ == '__main__':
    main()