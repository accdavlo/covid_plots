import streamlit as st

def app():
    st.write("# About")
    col1, col2, col3 = st.beta_columns([5,2,5])

    with col1:
        st.image("davide.jpg")
        st.write("### Davide Torlo")
        st.write("Ricercatore PostDoc all'Università SISSA di Trieste")
        st.write("Ideatore principale di concept, metriche e grafici")
        st.write("[Website](https://davidetorlo.it/), [Twitter](https://twitter.com/accdavlo)")

    with col3:
        st.image("fede_new.jpeg")
        st.write("### Federico Bianchi")
        st.write("Ricercatore PostDoc all'Università Bocconi di Milano")
        st.write("Support alla realizzazione della webapp e deploy")
        st.write("[Website](https://federicobianchi.io/), [Twitter](https://twitter.com/federicobianchy)")



