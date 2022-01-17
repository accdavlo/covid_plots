import streamlit as st
import numpy as np
from timeIntegration import DeC
from timeIntegration import RungeKutta
from timeIntegration import ODEproblems
import matplotlib.pyplot as plt



def app():
    st.write("# Modello SIR: simulazioni")  # markdown
    st.write(" Il modello SIR considera 3 classi: S suscettibili, I infetti e R guariti")
    #st.latex(
     #   r"\frac{dS}{dt} = -\beta \frac{SI}{N}, \quad \frac{dI}{dt} = \beta \frac{SI}{N} -  \gamma I, \quad  \frac{dR}{dt}= \gamma I .")

    st.sidebar.title("Modelli e simulazioni")
    app_mode = st.sidebar.selectbox("Scegli l'argomento",
                                    ["Modello SIR", "Simulazione"])
    if app_mode == "Modello SIR":
        run_model()
    elif app_mode == "Simulazione":
        run_simulations()


@st.cache()
def setup_problem_ref():
    problem = ODEproblems.ODEproblem("SIR")
    dd = np.loadtxt("SIR_ref.dat", dtype="float", delimiter=" ", usecols=range(4))
    tspan = dd[:, 0]
    u_ref = dd[:, 1:].transpose()
    return problem, tspan, u_ref


def run_simulations():
    st.write("### Simulazioni con Eulero Esplicito (FE) e modified Patankar Deferred Correction (mPDeC)")  # markdown

    problem, t_ref, u_ref = setup_problem_ref()

    labels = ["S", "I", "R"]
    N = st.sidebar.slider("Punti in cui calcolare", min_value=2, max_value=200, value=20)

    tspan = np.linspace(0, problem.T_fin, N)
    t_mpDeC, u_mpDeC = DeC.decMPatankar(problem.prod_dest, lambda x: 0 * x,
                                        tspan, problem.u0, 4, 7, "gaussLobatto")
    t_FE, u_FE = RungeKutta.explicitRK(problem.flux,
                                       tspan, problem.u0,
                                       np.zeros((1, 1)),
                                       np.array([1]),
                                       np.zeros(1))

    fig = plt.figure()
    for k in range(3):
        plt.plot(t_ref, u_ref[k, :], "-", color="gray", label=labels[k] + " ref")
        plt.plot(t_mpDeC, u_mpDeC[k, :], "--", color="blue", label=labels[k] + " mPDeC")
        plt.plot(t_FE, u_FE[k, :], ":", color="red", label=labels[k] + " FE")
    plt.legend()
    beta = 3
    gamma = 1
    R0 = beta / gamma
    #plt.title(r"$\beta = " + f"{beta}" + r", \gamma =" + f"{gamma}" + ", R_0=" + "%g $" % R0)

    plt.xlabel("Time")
    plt.ylabel("Population")

    st.pyplot(fig)

    st.write("Euler esplicito calcola semplicemente la soluzione al tempo \
     successivo aggiungendo al precedente il termine di evoluzione per il \
     time step, cioè")  # markdown
    #st.latex(r"S^{n+1}=S^n - \beta \frac{S^n I^n}{N}")
    st.write("Modified Patankar Deferred Correction sono una classe di metodi \
        alto ordine che garantiscono \
        la conservazione della popolazione totale e la positività di tutte le classi")
    st.write("Se vuoi scoprire di più su mPDeC guarda [l'articolo qui](https://arxiv.org/abs/1905.09237) \
     e il [codice qua](https://git.math.uzh.ch/abgrall_group/deferred-correction-patankar-scheme)")


def run_model():
    st.write("### Modello SIR: parametri β e γ")  # markdown
    st.write("I parametri β e γ descrivono rispettivamente il tasso di infezione e di guarigione dalla malattia")
    st.write("R0 è definito come β/γ")

    beta = st.sidebar.slider("β", min_value=0., max_value=10., value=3., step=0.01)
    gamma = st.sidebar.slider("γ", min_value=0., max_value=10., value=1., step=0.01)
    T_fin = st.sidebar.slider("Tempo finale", min_value=1., max_value=100., value=10., step=0.1)
    N = 100
    tspan = np.linspace(0, T_fin, N)
    problem, t_ref, u_ref = setup_problem_ref()

    labels = ["S", "I", "R"]

    def SIR_production_destruction(u, t=0, beta=3, gamma=1):
        p = np.zeros((len(u), len(u)))
        d = np.zeros((len(u), len(u)))
        N = np.sum(u)
        p[1, 0] = beta * u[0] * u[1] / N
        d[0, 1] = p[1, 0]
        p[2, 1] = gamma * u[1]
        d[1, 2] = p[2, 1]
        return p, d

    def new_pd(u, t=0):
        return SIR_production_destruction(u, t=t, beta=beta, gamma=gamma)

    t_mpDeC, u_mpDeC = DeC.decMPatankar(new_pd, lambda x: 0 * x,
                                        tspan, problem.u0, 5, 7, "gaussLobatto")

    fig2 = plt.figure()
    for k in range(3):
        plt.plot(t_mpDeC, u_mpDeC[k, :], label=labels[k])
    plt.legend()
    R0 = beta / gamma
    #plt.title(r"$\beta = " + f"{beta}" + r", \gamma =" + f"{gamma}" + ", R_0=" + "%1.3f $" % R0)

    plt.xlabel("Time")
    plt.ylabel("Population")
    st.pyplot(fig2)

    #st.latex(
     #   r"\frac{dI}{dt} = \beta I \frac{S}{N} -\gamma I = \gamma \left( R_0 I \frac{S}{N} - I\right)= \gamma I \underbrace{\left( R_0 \frac{S}{N} - 1 \right)}_{\text{Segno?}} ")
    st.write("Il segno della variazione degli infetti cambia quando la popolazione \
        suscettibile diminuisce a sufficienza gli infetti diminuiscono nel tempo, \
        precisamente quando")
    #st.latex(r"\frac{S}{N}<\frac{1}{R_0}")


if __name__ == '__main__':
    main()
