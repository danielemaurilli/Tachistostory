# Tachistostory

[English version](README.md)

Tachistostory e un'app di training della lettura basata su presentazioni tachistoscopiche, progettata per sostenere la fluenza tramite esposizioni visive brevi, ritmo controllato e risposte rapide ma accurate.
L'idea nasce anche con uno scopo specifico: far leggere un testo di comprensione verbale in modalita tachistoscopica e, al termine, proporre al bambino domande di comprensione.

## Panoramica del Progetto

La lettura non e uno scorrimento continuo: si basa su cicli ripetuti di fissazioni e saccadi.  
Tachistostory nasce dall'idea che allenare l'efficienza del campionamento visivo, il controllo attentivo e il mantenimento a breve termine dell'informazione verbale possa sostenere la fluenza e l'automatizzazione della decodifica.

L'app **non** dichiara un effetto causale garantito sui risultati di lettura.  
La logica di training e coerente con la letteratura su movimenti oculari, visual attention span, memoria di lavoro e funzioni esecutive.

## Funzionalita Principali

- Loop tachistoscopico di presentazione (parola + maschera + prova successiva)
- Velocita di esposizione regolabile con slider in gioco
- Supporto a file di input `.txt` e `.docx`
- Flusso sessione con gestione partecipante e selezione file stimolo
- Controlli pausa/restart/navigazione manuale durante la presentazione
- Logging strutturato di sessione (eventi parola, eventi pausa)
- Export finale in CSV e JSON
- Workflow base di pseudonimizzazione degli ID partecipante
- Struttura didattica orientata alla comprensione: lettura del testo + domande finali al bambino

## Perche Questa Scelta Ha Senso

- **Efficienza oculomotoria:** una migliore gestione fissazioni/saccadi puo sostenere la lettura fluente.
- **Vincolo tachistoscopico:** l'esposizione breve spinge a selezionare rapidamente l'informazione visiva rilevante.
- **Visual attention span:** l'estrazione rapida da stringhe di lettere/parole allena una componente collegata alla fluenza.
- **Coinvolgimento della memoria di lavoro:** l'utente deve mantenere brevemente in memoria cio che ha visto per rispondere.
- **Controllo esecutivo-attentivo:** il compito richiede anche inibizione, focus sostenuto e monitoraggio sotto pressione temporale.

In sintesi, Tachistostory combina vincoli temporali visivi e richieste di risposta per ingaggiare piu meccanismi associati alla fluenza di lettura.

## Avvio Locale

```bash
pip install -r requirements.txt
python main.py
```

## Download

E possibile scaricare Tachistostory direttamente dalla sezione **GitHub Releases**, dove sono disponibili tutte le versioni pubblicate.

## Riferimenti Scientifici (selezione)

- Rayner, K. (1998). *Eye movements in reading and information processing: 20 years of research.* Psychological Bulletin, 124(3), 372-422. https://doi.org/10.1037/0033-2909.124.3.372
- Bosse, M.-L., Tainturier, M. J., & Valdois, S. (2007). *Developmental dyslexia: The visual attention span deficit hypothesis.* Cognition, 104(2), 198-230. https://doi.org/10.1016/j.cognition.2006.05.009
- Bosse, M.-L., & Valdois, S. (2009). *Influence of the visual attention span on child reading performance: A cross-sectional study.* Journal of Research in Reading, 32(2), 230-253. https://doi.org/10.1111/j.1467-9817.2008.01387.x
- Lobier, M., Zoubrinetzky, R., & Valdois, S. (2012). *The visual attention span deficit in dyslexia is visual and not verbal.* Cortex, 48(6), 768-773. https://doi.org/10.1016/j.cortex.2011.09.003
- Valdois, S. (2022). *The visual-attention span deficit in developmental dyslexia: Review of evidence for a visual-attention-based deficit.* Dyslexia, 28(4), 397-415. https://doi.org/10.1002/dys.1724
- Sinha, N., Arrington, C. N., Malins, J. G., Pugh, K. R., Frijters, J. C., & Morris, R. (2024). *The reading-attention relationship: Variations in working memory network activity during single word decoding in children with and without dyslexia.* Neuropsychologia, 195, 108821. https://doi.org/10.1016/j.neuropsychologia.2024.108821
- Smith-Spark, J. H., & Gordon, R. (2022). *Automaticity and executive abilities in developmental dyslexia: A theoretical review.* Brain Sciences, 12(4), 446. https://doi.org/10.3390/brainsci12040446
- Hautala, J., Hawelka, S., & Ronimus, M. (2024). *An eye movement study on the mechanisms of reading fluency development.* Cognitive Development, 69, 101395. https://doi.org/10.1016/j.cogdev.2023.101395

## Nota

Tachistostory e uno strumento di training e va considerato complementare a percorsi professionali educativi o clinici di valutazione/intervento.
