# Linee Guida per Contribuire

Grazie per il tuo interesse nel contribuire a questo progetto! 🎉

## 📋 Indice

- [Codice di Condotta](#codice-di-condotta)
- [Come Contribuire](#come-contribuire)
- [Processo di Review](#processo-di-review)
- [Linee Guida per il Codice](#linee-guida-per-il-codice)
- [Licenza dei Contributi](#licenza-dei-contributi)

## Codice di Condotta

Questo progetto aderisce a un codice di condotta. Partecipando, ti impegni a:
- Essere rispettoso e costruttivo
- Accettare critiche costruttive
- Concentrarti su ciò che è meglio per il progetto

## Come Contribuire

### 🐛 Segnalare Bug

Prima di segnalare un bug:
1. Controlla le [issues esistenti](https://github.com/danielemaurilli/tachistostory/issues)
2. Assicurati di usare l'ultima versione

Quando segnali un bug, includi:
- Descrizione chiara del problema
- Passi per riprodurlo
- Comportamento atteso vs comportamento effettivo
- Screenshot (se rilevanti)
- Informazioni sul sistema (browser, OS, ecc.)

### 💡 Proporre Nuove Funzionalità

1. Apri una [issue](https://github.com/danielemaurilli/tachistostory/issues) con tag `enhancement`
2. Descrivi la funzionalità e perché sarebbe utile
3. Discuti l'implementazione con i maintainer prima di iniziare a programmare

### 🔧 Inviare Pull Request

#### Processo Standard

1. **Fork** il repository
2. **Clona** il tuo fork localmente
   ```bash
   git clone https://github.com/tuo-username/tachistostory.git
   ```
3. **Crea un branch** per la tua modifica
   ```bash
   git checkout -b feature/nome-feature
   # oppure
   git checkout -b fix/nome-bug
   ```
4. **Fai le modifiche** seguendo le [linee guida del codice](#linee-guida-per-il-codice)
5. **Testa** le tue modifiche
6. **Commit** con messaggi chiari
   ```bash
   git commit -m "Add: descrizione della feature"
   # oppure
   git commit -m "Fix: descrizione del fix"
   ```
7. **Push** al tuo fork
   ```bash
   git push origin feature/nome-feature
   ```
8. **Apri una Pull Request** dalla tua branch verso `main`

#### Checklist per Pull Request

Prima di inviare, assicurati che:
- [ ] Il codice funzioni correttamente
- [ ] Hai testato le modifiche
- [ ] Il codice segue lo stile del progetto
- [ ] Hai aggiornato la documentazione (se necessario)
- [ ] Hai aggiunto commenti al codice complesso
- [ ] Non ci sono errori di console
- [ ] La PR ha un titolo descrittivo

## Processo di Review

1. Un maintainer revisionerà la tua PR
2. Potrebbero essere richieste modifiche
3. Rispondi ai commenti e aggiorna la PR
4. Una volta approvata, la PR verrà merged

**Tempo di risposta**: Cerco di rispondere entro 3-5 giorni lavorativi.

## Linee Guida per il Codice

### Stile del Codice

#### JavaScript
```javascript
// Usa const/let, non var
const variabile = "valore";

// Nomi descrittivi
function calcolaTempoEsposizione() {
  // ...
}

// Commenti per logica complessa
// Calcola il tempo in ms basandosi sulla frequenza
const tempo = 1000 / frequenza;
```

#### HTML/CSS
```html
<!-- Usa nomi di classe descrittivi -->
<div class="tachistoscopio-container">
  <button class="btn-start">Avvia</button>
</div>
```

```css
/* Organizza il CSS per componente */
.tachistoscopio-container {
  display: flex;
  justify-content: center;
}
```

### Commit Messages

Usa messaggi chiari e descrittivi:

- ✨ `Add: [descrizione]` - Nuova funzionalità
- 🐛 `Fix: [descrizione]` - Correzione bug
- 📝 `Docs: [descrizione]` - Modifica documentazione
- 🎨 `Style: [descrizione]` - Formattazione, pulizia codice
- ♻️ `Refactor: [descrizione]` - Refactoring
- ⚡ `Perf: [descrizione]` - Miglioramento performance
- ✅ `Test: [descrizione]` - Aggiunta/modifica test

Esempio:
```
Add: opzione per configurare durata stimoli

- Aggiunta interfaccia per impostare durata
- Validazione input utente
- Aggiornata documentazione
```

### Testing

- Testa il codice su diversi browser (Chrome, Firefox, Safari)
- Verifica la responsività su mobile
- Controlla la console per errori

## Licenza dei Contributi

⚖️ **IMPORTANTE**: Inviando un contributo, accetti che:

1. Hai i diritti sul codice che stai contribuendo
2. Concedi all'autore del progetto il diritto di:
   - Usare il tuo contributo nel progetto
   - Modificarlo
   - Distribuirlo sotto i termini della licenza del progetto
3. Mantieni il diritto di essere riconosciuto come contributore
4. Il tuo contributo sarà sotto la stessa licenza del progetto (vedi [LICENSE.md](LICENSE.md))
5. **Puoi includere il tuo contributo nel tuo CV, portfolio o profilo LinkedIn**

**Non puoi**:
- Contribuire codice protetto da copyright di terzi
- Contribuire codice sotto licenze incompatibili

### 💼 Valorizza il Tuo Contributo

Contribuire a questo progetto è un'ottima esperienza da mostrare professionalmente!

**Puoi**:
- ✅ Menzionare il progetto nel tuo CV
- ✅ Includerlo nel tuo portfolio GitHub/personale
- ✅ Aggiungerlo su LinkedIn (sezione Progetti o Esperienza)
- ✅ Linkare le tue PR e issue nei tuoi materiali professionali

**Esempio per CV**:
```
Open Source Contributor - Progetto Tachistoscopio
• Implementato sistema di configurazione tempi (PR #42)
• Risolti 5 bug critici relativi alla visualizzazione
• Migliorata documentazione per utenti clinici
GitHub: github.com/danielemaurilli/tachistostory/pulls?q=author:tuo-username
```

**Esempio per LinkedIn**:
```
Titolo: Contributor - Tachistoscopio (Open Source)
Descrizione: Contribuito allo sviluppo di uno strumento tachistoscopico 
per uso clinico e di ricerca. Implementate nuove funzionalità e 
corretti bug critici.
Link: [link alla repository o alle tue PR]
```

## 🎯 Aree dove Contribuire

Cerco particolarmente aiuto in:

- [ ] 🐛 Correzione bug
- [ ] 📝 Miglioramento documentazione
- [ ] 🌍 Traduzioni
- [ ] ✨ Nuove funzionalità (vedi [issues con tag `good first issue`](https://github.com/danielemaurilli/tachistostory/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22))
- [ ] 🧪 Testing su diversi dispositivi/browser
- [ ] ♿ Miglioramenti accessibilità

## 💬 Domande?

- Apri una [Discussion](https://github.com/danielemaurilli/tachistostory/discussions)
- Oppure contattami: maurillidaniele@gmail.com

## 🙏 Grazie!

Ogni contributo, grande o piccolo, è apprezzato! 

---

**Ricorda**: Contribuire è anche segnalare bug, migliorare la documentazione, o aiutare altri utenti. Non serve essere un esperto di programmazione! 🚀