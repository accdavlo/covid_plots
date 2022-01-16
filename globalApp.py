import streamlit as st
from appTimeIntegration import run_model_and_simulation
from appItaly import run_italian_data
from appWorldData import run_world

def main():
    st.sidebar.title("Cosa visualizzare")
    app_mode = st.sidebar.selectbox("Scegli l'argomento",
        ["Modelli e simulazioni", "Dati Italiani", "Dati Mondo"])
    if app_mode == "Modelli e simulazioni":
        run_model_and_simulation()
    elif app_mode == "Dati Italiani":
        run_italian_data()
    elif app_mode == "Dati Mondo":
        run_world()

if __name__ == '__main__':
    main()