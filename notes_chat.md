
# Dati italiani sulla pandemia

## Modellistica
 * Come si diffonde un virus? Contatti, reti
 * Modelli molto complicati
 * Semplificazioni: [Bel thread di Francesco di Lauro](https://twitter.com/Di_SPACE_Lauro/status/1404912878474383362)
   * SIR
     * 3 classi 
     * 2 parametri: probabilità di infezione e tempo di guarigione
     * Asintotico a esponenziale
     * Cons: difficile interpretare parametri, no struttura geografica/demografica, deterministico
   * Metapopulation SIR
     * Più classi (geografiche, anagrafiche, malattie, stato vaccinale)
   * SEIR 
     * Exposed: prima di diventare infettiva c'è un altro periodo, più realistico
     * Si possono rappresentare isolamenti, ospedalizzati ecc
     * Più parametri
     * Contatti tra tutta la popolazione con probabilità
   * Stochastic SIR/SEIR
   * SIR su network
     * Fissi a priori la topologia del network
     * Sleghi

## Approssimazione e previsioni
  * Metodi per simulare
  * Due prove -> notebook: explicit euler e mPDeC
  * Ill-posedness
  * Data fitting
  * 

## Data analisi

### Plot carini
 * [Ricoverati per fasce età e vaccino](https://www.datawrapper.de/_/ZNE0I/) (opencovid-mr)


