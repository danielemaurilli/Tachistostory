# Tachistostory

![License: Custom Non-Commercial](https://img.shields.io/badge/License-Custom_Non--Commercial-blue.svg)
![Clinical Use: Allowed](https://img.shields.io/badge/Clinical_Use-Allowed-green.svg)
![Version](https://img.shields.io/badge/Version_0.9.0-orange.svg)
Maurilli, D. (2025). Tachistostory: Applicazione tachistoscopica per 
il potenziamento delle abilità di lettura [Software]. 
GitHub: https://github.com/danielemaurilli/tachistostory

Licenza: Custom Non-Commercial Clinical License

[Python](https://img.shields.io/badge/python-3.8+-blue.svg)

> Applicazione tachistoscopica per il potenziamento delle abilità di lettura attraverso l'allenamento dei movimenti oculari saccadici

[🇮🇹 Italiano](README.md) | [🇬🇧 English](README_EN.md)

## 📋 Descrizione

**Tachistostory** è uno strumento clinico-educativo innovativo progettato per il potenziamento delle abilità di lettura nei bambini attraverso la tecnica tachistoscopica. L'applicazione si basa su solidi principi neuroscientifici riguardanti i movimenti oculari saccadici durante la lettura.

### Come Funziona

Il tachistoscopio presenta parole singole per brevi periodi di tempo controllati, allenando il sistema visivo a processare l'informazione scritta in modo più efficiente. Il training segue un percorso graduale:

- **Inizio**: Le parole vengono presentate per **1200 ms** (tempo confortevole per i lettori in difficoltà)
- **Progressione**: Con l'esercizio costante, il tempo di esposizione viene progressivamente ridotto
- **Obiettivo**: Raggiungere **220-250 ms**, il tempo naturale di una saccade durante la lettura fluente secondo la letteratura scientifica

### Obiettivi Clinici

1. **Potenziamento della velocità di lettura**: Allenamento dei movimenti oculari saccadici
2. **Comprensione del testo**: Domande di comprensione dopo ogni frase per verificare l'elaborazione
3. **Attenzione sostenuta e divisa**: Mantenimento del focus durante la presentazione rapida
4. **Memoria di lavoro**: Ritenzione delle parole per ricostruire il significato della frase

## ✨ Caratteristiche Principali

- 📖 **Presentazione tachistoscopica** di parole singole con tempi configurabili (220-1200 ms)
- 🎯 **Mascheramento post-stimolo** per evitare l'elaborazione prolungata dell'immagine retinica
- 📝 **Personalizzazione contenuti**: Carica testi personalizzati (`.txt`, `.doc`, `.docx`)
- 🎮 **Interfaccia intuitiva**: Controlli semplici adatti all'uso con bambini
- 📊 **Tracciamento progressi**: Indicatore di avanzamento parola per parola
- 🖥️ **Modalità fullscreen**: Per eliminare distrazioni visive
- ⚙️ **Slider di regolazione**: Modifica del tempo di esposizione in tempo reale

## 🎯 A Chi è Rivolto

### Professionisti Clinici
- **Psicologi e neuropsicologi** per training cognitivo
- **Logopedisti** per riabilitazione della lettura
- **Psicopedagogisti** per interventi educativi
- **Terapisti della neuro e psicomotricità dell'età evolutiva** per interventi integrati

### Contesti di Utilizzo
- Disturbi Specifici dell'Apprendimento (DSA - Dislessia)
- Ritardi nello sviluppo delle abilità di lettura
- Riabilitazione post-trauma o post-ictus (adulti)
- Potenziamento delle abilità di lettura in bambini normolettori

## 🚀 Installazione

### Requisiti
- Python 3.8 o superiore
- Pygame
- docx2txt

### Installazione Dipendenze

```bash
# Clona la repository
git clone https://github.com/danielemaurilli/tachistostory.git

# Entra nella directory
cd tachistostory

# Installa le dipendenze
pip install -r requirements.txt
```

### File requirements.txt
```
pygame>=2.5.0
docx2txt>=0.8
```

## 💡 Utilizzo

### Avvio dell'Applicazione

```bash
python main.py
```

### Preparazione del Materiale

1. **Prepara un file di testo** (`.txt`, `.doc`, o `.docx`) contenente le frasi da presentare
2. **Formato consigliato**: Una frase per riga, con parole separate da spazi
3. **Esempio di contenuto**:
   ```
   Il gatto dorme sul divano
   Maria gioca a palla nel parco
   Il sole splende nel cielo blu
   ```

### Workflow Clinico Completo

1. **Caricamento**: Trascina il file nella finestra dell'applicazione
2. **Configurazione**: Regola il tempo di esposizione con lo slider (inizia da 1200 ms)
3. **Presentazione**: Premi INVIO per iniziare
4. **Lettura**: Il bambino legge ogni parola che appare
5. **Ricostruzione**: Dopo la frase completa, chiedi al bambino di ricostruirla
6. **Comprensione**: Poni domande sulla frase letta (es. "Dove dormiva il gatto?")
7. **Progressione**: Riduci gradualmente il tempo di esposizione nelle sessioni successive

### Controlli

| Tasto | Funzione |
|-------|----------|
| **INVIO** | Inizia la presentazione dalla schermata istruzioni |
| **SPAZIO** | Passa alla parola successiva (dopo la maschera) |
| **P** | Pausa / Riprendi |
| **R** | Ricomincia dalla prima parola |
| **F** | Attiva/disattiva fullscreen |
| **I** | Minimizza la finestra |
| **Slider** | Regola il tempo di esposizione (220-1200 ms) |

## 🔬 Fondamenti Scientifici

### Movimenti Saccadici nella Lettura

Durante la lettura fluente, gli occhi eseguono movimenti rapidi chiamati **saccadi** che durano circa **20-40 ms**, seguiti da fissazioni di **200-250 ms** durante le quali il cervello elabora l'informazione. Tachistostory allena questo processo naturale.

### Progressione del Training

```
Settimana 1-2:  1200 ms → Familiarizzazione con lo strumento
Settimana 3-4:  900 ms  → Prima riduzione significativa
Settimana 5-6:  600 ms  → Avvicinamento al tempo naturale
Settimana 7-8:  400 ms  → Affinamento delle abilità
Settimana 9+:   250 ms  → Tempo target di lettura fluente
```

*Nota: I tempi sono indicativi e vanno adattati al singolo bambino*

### Componenti Cognitive Allenate

1. **Elaborazione visiva rapida**: Riconoscimento immediato delle parole
2. **Memoria di lavoro**: Mantenimento delle parole in memoria per ricostruire la frase
3. **Attenzione sostenuta**: Mantenimento del focus durante la presentazione
4. **Attenzione divisa**: Gestione simultanea di lettura e comprensione
5. **Integrazione sequenziale**: Ricostruzione del significato dalla sequenza di parole

## 📖 Esempio di Sessione Clinica

### Setting
- Durata: 20-30 minuti
- Frequenza: 2-3 volte a settimana
- Ambiente: Silenzioso, con illuminazione adeguata

### Protocollo
1. **Warm-up** (5 min): Tempo di esposizione confortevole (es. 800 ms)
2. **Training** (15 min): Tempo target della sessione
3. **Cool-down** (5 min): Domande di comprensione e feedback
4. **Registrazione**: Annotare tempo usato, numero di frasi, errori, fatica percepita

### Domande di Comprensione (Esempi)

Per la frase: *"Il gatto dorme sul divano"*

- **Letterali**: "Chi dorme?" "Dove dorme il gatto?"
- **Inferenziali**: "Secondo te è giorno o notte?" "Il gatto è stanco?"
- **Memoria**: "Quante parole aveva la frase?" "Qual era la terza parola?"

## 🎨 Personalizzazione

### Creazione di Materiali Personalizzati

Il contenuto può essere adattato a:
- **Livello di lettura** del bambino
- **Interessi personali** (sport, animali, videogiochi)
- **Obiettivi specifici** (vocaboli nuovi, strutture grammaticali)
- **Tematiche curriculari** (per supporto scolastico)

### Suggerimenti per i Contenuti

- Inizia con parole brevi (3-5 lettere)
- Usa frasi semplici (soggetto-verbo-complemento)
- Evita strutture sintattiche complesse all'inizio
- Aumenta gradualmente la complessità

## 📊 Monitoraggio dei Progressi

### Indicatori da Registrare
- Tempo di esposizione utilizzato
- Numero di parole/frasi completate
- Accuratezza nella ricostruzione delle frasi
- Risposte corrette alle domande di comprensione
- Livello di fatica percepita (scala 1-5)

### Criteri di Progressione
Riduci il tempo di esposizione quando il bambino:
- Legge correttamente almeno l'80% delle parole
- Ricostruisce correttamente le frasi
- Risponde correttamente alle domande di comprensione
- Non manifesta eccessiva fatica

## 📜 Licenza

Questo progetto è rilasciato sotto una **Licenza Non Commerciale Personalizzata**.

### ✅ USO CONSENTITO

- **Uso clinico**: Libero utilizzo da parte di psicologi, logopedisti, terapisti come strumento di supporto professionale
- **Uso didattico**: Utilizzo in contesti educativi, universitari, di ricerca
- **Uso personale**: Studio, apprendimento, sperimentazione
- **Collaborazione**: Fork, modifiche e contributi tramite GitHub

### ❌ USO NON CONSENTITO

- Vendita del software o inclusione in prodotti commerciali
- Distribuzione come servizio a pagamento (SaaS, app)
- Ridistribuzione al di fuori di GitHub

📋 **Dettagli completi**: [LICENSE.md](LICENSE.md)  
❓ **Domande frequenti**: [FAQ.md](FAQ.md)

### 💼 Licenza Commerciale

Sei un'azienda o istituzione interessata a un uso commerciale? [Contattami](mailto:maurillidaniele@gmail.com) per discutere una licenza dedicata.

## 🤝 Contribuire

I contributi sono benvenuti! Questo progetto è aperto alla collaborazione della comunità clinica e di sviluppo.

### Come Contribuire

1. Fork del progetto
2. Crea un branch (`git checkout -b feature/NuovaFunzionalita`)
3. Commit delle modifiche (`git commit -m 'Add: nuova funzionalità'`)
4. Push al branch (`git push origin feature/NuovaFunzionalita`)
5. Apri una Pull Request

**💼 Valorizza il tuo contributo**: I contributori possono includere i loro contributi in CV, portfolio o LinkedIn!

Leggi [CONTRIBUTING.md](CONTRIBUTING.md) per maggiori dettagli.

## 🐛 Segnalazione Bug

Hai trovato un bug? [Apri una issue](https://github.com/[username]/tachistostory/issues) descrivendo:
- Cosa hai fatto
- Cosa ti aspettavi
- Cosa è successo invece
- Sistema operativo e versione Python
- Screenshot (se rilevanti)

## 📚 Citazione

Se utilizzi Tachistostory in un contesto clinico o di ricerca, citalo come:

```
Maurilli, D. (2025). Tachistostory: Applicazione tachistoscopica per il 
potenziamento delle abilità di lettura [Software]. 
GitHub: https://github.com/[username]/tachistostory
Licenza: Custom Non-Commercial Clinical License
```

**BibTeX**:
```bibtex
@software{maurilli2025tachistostory,
  author = {Maurilli, Daniele},
  title = {Tachistostory: Applicazione tachistoscopica per il potenziamento delle abilità di lettura},
  year = {2025},
  url = {https://github.com/[username]/tachistostory},
  note = {Licenza: Custom Non-Commercial Clinical License}
}
```

## 👤 Autore

**Daniele Maurilli**

- 📧 Email: maurillidaniele@gmail.com
- 💼 GitHub: [@danielemaurilli](https://github.com/danielemaurilli)

## 🙏 Ringraziamenti

- La comunità scientifica per le ricerche sui movimenti oculari nella lettura
- I professionisti clinici che utilizzeranno questo strumento per aiutare i bambini
- La comunità Pygame per l'eccellente framework

## ⚠️ Disclaimer Clinico

Tachistostory è uno **strumento di supporto** clinico e non sostituisce una valutazione diagnostica completa o un intervento terapeutico strutturato. Deve essere utilizzato:

- Da professionisti qualificati (psicologi, logopedisti, terapisti)
- All'interno di un percorso terapeutico più ampio
- Con supervisione diretta durante l'uso con bambini
- Nel rispetto delle normative sulla privacy (GDPR) e dei codici deontologici professionali

L'utente è responsabile dell'uso appropriato del software e della conformità alle normative vigenti.

## 🔮 Roadmap Futura

- [ ] Sistema di tracciamento automatico dei progressi
- [ ] Generazione di report per i genitori
- [ ] Database di frasi pre-configurate per età/livello
- [ ] Modalità multiplayer per competizione amichevole
- [ ] Integrazione domande di comprensione nell'interfaccia
- [ ] Supporto per immagini associate alle parole
- [ ] Esportazione dati per analisi statistiche

## 📞 Supporto

- 📖 [Wiki](https://github.com/[username]/tachistostory/wiki) (in sviluppo)
- 💬 [Discussions](https://github.com/[username]/tachistostory/discussions)
- 🐛 [Issues](https://github.com/[username]/tachistostory/issues)
- 📧 Email: maurillidaniele@gmail.com

---

**Sviluppato con ❤️ per supportare bambini con difficoltà di lettura**

*Versione 0.9.0 - Dicembre 2025*
