# Descrizione del lavoro

## consistency.py
1. la prima cosa è scrivere gli attributi del csv principale, poi estraiamo una serie di statistiche dal csv principale tipo quante righe, quanti valori, quanti sono non nulli e quanti nulli. Poi controlliamo che i valori mancanti siano correttamente codificati con `,,`. Poi controlliamo che alcune colonne che sembrano intere siano effettivamente tutti valori int (index da 24 a 46 inclusi, queste appaiono come float ma noi verifichiamo se sono interi e decidiamo di tenerle come int not float);
2. Poi controlliamo quanti valori unici ha la colonna `best_of`, ne ha 2 (3 e 5);
3. Tabella statistica: valori totali (cnt), n.missing values (val assoluto e %), unique di best_of;
4. Poi abbiamo fatto i controlli in tourney_day per verificare che fossero 8 di len e che i mesi fossero codificati con 01-02-03,ecc... Tutto ok.

## divide.py
1. dividiamo la tabella tennis in 3 tabelle: player, tournament e match. E non aggiunge i duplicati, quindi è corretta.

# Domande Lab

1. Possiamo usare delle funzioni di pandas per verificare che quello che abbiamo fatto manualmente è corretto? Se si possiamo tenerle nel codice da consegnare e segnarle come testing?
2. dato che stiamo creando una datawherehouse noi abbiamo pensato di lasciare i valori mancanti così come sono e inserirli con NULL in database, è corretto?
3. ogni riga di `tennis.csv` rappresenta un match?
