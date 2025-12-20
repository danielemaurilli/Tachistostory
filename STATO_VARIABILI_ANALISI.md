# Analisi Variabili di Stato - Tachistostory

## Stati Applicazione (State Enum)

| Stato | Descrizione | Scopo | Trigger In | Trigger Out |
|-------|-------------|-------|------------|-------------|
| **MENU_START** | Menu iniziale | Schermata di avvio con logo e fade-in | App start | Click/Enter |
| **INTRO_TABLE** | Intro tavolo | Mostra tavolo con libro chiuso | Dopo MENU_START | Automatico (timer) |
| **INTRO_BOOK_OPEN** | Animazione libro | 17 frame di apertura libro | Dopo INTRO_TABLE | book_animation_completed |
| **TRANSITION** | Transizione | Effetto fade tra stati | Richiesto tra stati | Alpha complete |
| **FILE** | Selezione file | Attesa drag&drop file testo/Word | Dopo intro o reset | File caricato |
| **ISTRUCTION** | Istruzioni | Mostra info file e slider velocità | Dopo FILE | Spacebar press |
| **SHOW_WORD** | Mostra parola | Display parola corrente | Dopo ISTRUCTION o ciclo | durata_parola_ms |
| **SHOW_MASK** | Mostra maschera | Display parola mascherata (###) | Dopo SHOW_WORD | durata_maschera_ms |
| **END** | Fine | Presentazione completata | Ultima parola | Reset/Quit |

---

## Variabili di Stato per Categoria

### 🎯 **Core State Machine**

| Variabile | Tipo | Valore Iniziale | Scopo | Modificato Da | Usato In |
|-----------|------|-----------------|-------|---------------|----------|
| `stato_presentazione` | `State` | `State.MENU_START` | Stato corrente app | Transizioni | Render loop |
| `tempo_inizio_stato` | `int \| None` | `None` | Timestamp entrata stato | Cambio stato | Timer duration |

**🔄 Refactoring:** Sarà sostituito da `StateMachine.current_state`

---

### 📝 **File & Text Data**

| Variabile | Tipo | Valore Iniziale | Scopo | Modificato Da | Usato In |
|-----------|------|-----------------|-------|---------------|----------|
| `file_caricato` | `bool` | `False` | Flag caricamento completato | load_from_txt/word | FILE state |
| `percorso_file` | `str \| None` | `None` | Path file caricato | File selection | Load methods |
| `nome_file` | `str \| None` | `None` | Nome file (display) | File selection | ISTRUCTION state |
| `num_parole` | `int \| None` | `None` | Conteggio parole totali | len(lista_parole) | ISTRUCTION state |
| `lista_parole` | `List[str]` | `[]` | Lista tutte parole pulite | FileLoader | Presentazione |
| `indice_parola` | `int` | `0` | Indice parola corrente | set_word_index | Navigation |
| `parola_corrente` | `str` | `""` | Parola attualmente mostrata | set_word_index | SHOW_WORD |
| `parola_mascherata` | `str` | `""` | Versione mascherata (###) | maschera_parola | SHOW_MASK |

**🔄 Refactoring:** Diventeranno stato del `FileState` e `PresentationState`

---

### 📖 **Sentence/Phrase Tracking**

| Variabile | Tipo | Valore Iniziale | Scopo | Modificato Da | Usato In |
|-----------|------|-----------------|-------|---------------|----------|
| `phrases_list` | `List[str]` | `[]` | Lista frasi complete | helper_sentences | Context display |
| `phrases_index` | `int` | `0` | Indice frase corrente | _sync_phrase_index_to_word | UI info |
| `phrases_total` | `int` | `0` | Totale frasi nel testo | build_word_to_sentence_map | Progress bar |
| `word_to_phrase_map` | `List[int]` | `[]` | Mappa parola→frase | build_word_to_sentence_map | Sync tracking |

**🔄 Refactoring:** Gestiti da FileLoader, stato in PresentationState

---

### ⏱️ **Timing & Animation**

| Variabile | Tipo | Valore Iniziale | Scopo | Modificato Da | Usato In |
|-----------|------|-----------------|-------|---------------|----------|
| `durata_parola_ms` | `int` | `220` | Durata display parola (ms) | Slider | SHOW_WORD timer |
| `durata_maschera_ms` | `int` | `400` | Durata display maschera (ms) | Fixed | SHOW_MASK timer |
| `logo_alpha` | `int` | `0` | Opacità logo (0-255) | Fade animation | MENU_START |
| `logo_fade_duration` | `int` | `3500` | Durata fade logo (ms) | Config | MENU_START |
| `logo_fade_start` | `int` | `pygame.time.get_ticks()` | Timestamp inizio fade | MENU_START enter | Fade calc |
| `book_current_frame` | `int` | `0` | Frame corrente animazione | Animation loop | INTRO_BOOK_OPEN |
| `book_animation_start` | `int` | `0` | Timestamp inizio anim libro | State enter | Frame timing |
| `book_frame_duration_ms` | `int` | `220` | Durata singolo frame (ms) | Config | Frame advance |
| `book_animation_completed` | `bool` | `False` | Flag fine animazione | Frame 17 reached | Transition trigger |

**🔄 Refactoring:** Durate in `config.timing`, stato in singoli State

---

### 🎨 **UI & Interaction**

| Variabile | Tipo | Valore Iniziale | Scopo | Modificato Da | Usato In |
|-----------|------|-----------------|-------|---------------|----------|
| `in_pausa` | `bool` | `False` | Flag pausa attiva | Spacebar | SHOW_WORD/MASK |
| `avanti` | `bool` | `False` | Flag avanzamento manuale | Arrow keys | Navigation |
| `slider_drag` | `bool` | `False` | Slider in dragging | Mouse events | Slider component |
| `posizione_cursore` | `int` | `self.x_slider` | Posizione X knob slider | Slider drag | Slider render |
| `mostra_errore` | `bool` | `False` | Flag errore visibile | Error handlers | Error display |
| `tempo_errore` | `int` | `0` | Timestamp errore | Error trigger | Error timeout |
| `messaggio_errore` | `str` | `""` | Testo messaggio errore | Exception handlers | Error render |

**🔄 Refactoring:** 
- `slider_*` → `Slider` component
- `in_pausa` → PresentationState
- `mostra_errore` → ErrorOverlay component

---

### 🖼️ **Assets & Resources**

| Variabile | Tipo | Valore Iniziale | Scopo | Modificato Da | Usato In |
|-----------|------|-----------------|-------|---------------|----------|
| `logo_image` | `Surface \| None` | `None` | Immagine logo grande | load_image_asset | MENU_START |
| `logo_icon` | `Surface \| None` | `None` | Icona finestra | load_image_asset | Window icon |
| `bg_menu` | `Surface \| None` | `None` | Background menu | _scala_background_intro | MENU_START |
| `bg_tavolo` | `Surface \| None` | `None` | Background tavolo | _scala_background_intro | INTRO_TABLE |
| `sprite_libro_chiuso` | `Surface \| None` | `None` | Sprite libro chiuso | book_frames[0] | INTRO_TABLE |
| `book_frames` | `List[Surface]` | `[]` | 17 frame animazione libro | _extract_sprite_frames | INTRO_BOOK_OPEN |
| `book_frames_scaled` | `List[Surface]` | `[]` | Frame scalati per schermo | _scale_book_frames | Render |
| `book_open_bg` | `Surface \| None` | `None` | Background libro aperto | _scala_background_intro | Post-animation |

**🔄 Refactoring:** Gestiti da AssetLoader, caricati on-demand per stato

---

### 🎭 **Transition Effects**

| Variabile | Tipo | Valore Iniziale | Scopo | Modificato Da | Usato In |
|-----------|------|-----------------|-------|---------------|----------|
| `transition_active` | `bool` | `False` | Transizione in corso | change_state request | Render overlay |
| `transition_alpha` | `int` | `0` | Opacità fade (0-255) | Update loop | Fade effect |
| `transition_target_state` | `State \| None` | `None` | Stato destinazione | change_state request | Completion check |

**🔄 Refactoring:** Gestiti da TransitionState dedicato

---

### 🖥️ **Display & Layout**

| Variabile | Tipo | Valore Iniziale | Scopo | Modificato Da | Usato In |
|-----------|------|-----------------|-------|---------------|----------|
| `screen` | `Surface \| None` | `None` | Main display surface | get_screen | Render target |
| `base_width` | `int` | `1920` | Larghezza design base | Config | Scaling calc |
| `base_height` | `int` | `1080` | Altezza design base | Config | Scaling calc |
| `screen_width` | `int` | `1920` | Larghezza corrente | Resize/fullscreen | Layout |
| `screen_height` | `int` | `1080` | Altezza corrente | Resize/fullscreen | Layout |
| `full_screen` | `bool` | `False` | Modalità fullscreen | F11 key | Window mode |
| `last_layout_size` | `Tuple[int,int]` | `(1920, 1080)` | Dimensioni precedenti | aggiorna_layout | Resize detection |

**🔄 Refactoring:** Centralizzati in `config.display`, gestiti da DisplayManager

---

### 🎨 **Colors** (Già in config)

| Variabile | Tipo | Valore Iniziale | Migrato In |
|-----------|------|-----------------|------------|
| `bg_color` | `Tuple[int,int,int]` | `(210, 245, 130)` | `config.display.bg_color` |
| `menu_bg_color` | `Tuple[int,int,int]` | `(0, 157, 198)` | `config.display.menu_bg_color` |
| `error_color` | `Tuple[int,int,int]` | `(200, 30, 30)` | `config.display.error_color` |

---

### 🔤 **Fonts** (Già in config)

| Variabile | Tipo | Migrato In |
|-----------|------|------------|
| `font` | `Font \| None` | Creato dinamicamente da config |
| `font_path` | `str` | `config.font.path` |
| `base_font` | `int` | `config.font.main_size` |
| `font_ms` | `Font` | Creato da `config.font.slider_label_size` |
| `font_attes` | `Font` | Creato da `config.font.menu_size` |
| `font_istruzioni` | `Font` | Creato da `config.font.instruction_size` |
| `font_about` | `Font` | Creato da `config.font.about_size` |
| `font_pausa` | `Font` | Creato da `config.font.pause_size` |

---

### 🎚️ **Slider** (Già estratto in Slider component)

| Variabile | Tipo | Migrato In |
|-----------|------|------------|
| `x_slider` | `int` | `Slider.x` |
| `y_slider` | `int` | `Slider.y` |
| `base_y_slider` | `int` | Config/non usato |
| `posizione_cursore` | `int` | `Slider.knob_x` |
| `slider_drag` | `bool` | `Slider.is_dragging` |
| `pomello_radius` | `int` | `Slider.knob_radius` |
| `base_slider_width` | `int` | `config.slider.base_width` |
| `slider_width` | `int` | `Slider.width` |
| `lista_fattori` | `List[float]` | `config.slider.tick_factors` |

---

### 🎬 **Costanti Layout** (Già in config)

| Variabile | Migrato In |
|-----------|------------|
| `LOGO_WIDTH_RATIO` | `config.display.logo_width_ratio` |
| `SLIDER_MARGIN_RATIO` | `config.display.slider_margin_ratio` |
| `SLIDER_WIDTH_RATIO` | `config.display.slider_width_ratio` |
| `book_bottom_margin` | `config.book.bottom_margin` |

---

## 📊 Statistiche Refactoring

### Variabili di Stato Totali: **~80**

**Status Migrazione:**
- ✅ **Completate (26)**: Colors, Fonts, Slider, Layout constants → Config/Slider
- 🔄 **In Progress (0)**: Nessuna
- ⏳ **Da Migrare (54)**: 
  - 9 variabili → StateMachine
  - 8 variabili → FileState/PresentationState
  - 4 variabili → SentenceTracker
  - 10 variabili → TimingManager per stati
  - 8 variabili → UI Components (Pause, Error)
  - 8 variabili → AssetManager
  - 3 variabili → TransitionState
  - 4 variabili → DisplayManager

### Breakdown per Destinazione:

| Componente Target | N° Variabili | Priorità |
|-------------------|--------------|----------|
| StateMachine | 9 | 🔴 Alta (FASE 4) |
| State Classes | 12 | 🔴 Alta (FASE 5) |
| AssetManager | 8 | 🟡 Media (FASE 6) |
| UI Components | 8 | 🟡 Media (FASE 7) |
| DisplayManager | 4 | 🟢 Bassa (FASE 8) |
| Già Migrati | 26 | ✅ Completato |

---

## 🎯 Prossimi Step (FASE 4-5)

### Step 4.1: StateMachine Migration
Variabili da gestire:
- `stato_presentazione` → `StateMachine.current_state`
- `tempo_inizio_stato` → `BaseState.enter_time`

### Step 4.2: Create State Classes
Ogni stato eredita da BaseState e gestisce proprie variabili:

1. **MenuStartState**: `logo_alpha`, `logo_fade_start`, `logo_image`
2. **IntroTableState**: `bg_tavolo`, `sprite_libro_chiuso`
3. **IntroBookOpenState**: `book_current_frame`, `book_animation_start`, `book_animation_completed`
4. **FileSelectionState**: `file_caricato`, `percorso_file`
5. **InstructionState**: `nome_file`, `num_parole`
6. **PresentationState**: `indice_parola`, `parola_corrente`, `parola_mascherata`, `in_pausa`
7. **TransitionState**: `transition_alpha`, `transition_target_state`
8. **EndState**: Reset e cleanup

Questo approccio:
- ✅ Incapsula stato per contesto
- ✅ Elimina variabili globali monolitiche
- ✅ Facilita testing isolato
- ✅ Rende chiare le dipendenze