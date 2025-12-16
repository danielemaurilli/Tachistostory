"""
Tachistostory - Main Entry Point
Speed reading training application using tachistoscope technique.
"""

import pygame 
from pygame.locals import (
    QUIT, KEYDOWN, K_SPACE, K_RETURN,
    K_p, K_r, K_f, K_i, K_RIGHT, K_LEFT,
    MOUSEBUTTONDOWN, MOUSEBUTTONUP, 
    MOUSEMOTION, VIDEORESIZE,
    K_KP_ENTER, RESIZABLE,
    K_e
)
import sys
import os
import traceback
import settings
from game import Tachistostory, Error, State

# ============================================================================
# GAME INITIALIZATION
# ============================================================================

def resource_path(relative_path: str) -> str:
    """
    Restituisce il path corretto sia in sviluppo che dentro l'eseguibile PyInstaller.
    """
    # Quando l'app è congelata, PyInstaller usa sys._MEIPASS
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def main():
    app = Tachistostory()
    app.get_screen()
    app.caption_window()
    app.get_font()  
    app.load_assets() 
    app.disegna_schermata_attesa() 
    app.helper_slider(settings.DURATA_MIN, settings.DURATA_MAX)
    app.stato_presentazione = State.MENU_START
    app.tempo_inizio_stato = pygame.time.get_ticks()

    # Error renderers (avoid long if/elif chains)
    error_renderers = {
        Error.EMPTY: app.empty_message,
        Error.EXCEPTION: lambda: app.error_message(app.messaggio_errore),
        Error.INVALID: lambda: app.invalid_message(app.messaggio_errore),
    }

    state_renderers = {
        State.MENU_START: app.disegna_menu_start,
        State.INTRO_TABLE: app.disegna_tavolo_libro_chiuso,
        State.INTRO_BOOK_OPEN: app.disegna_apertura_libro,
        State.FILE: app.disegna_schermata_attesa,
        State.ISTRUCTION: app.disegna_schermata_istruzioni,
        State.SHOW_WORD: lambda: app.scrivi_testo_centrato(app.parola_corrente),
        State.SHOW_MASK: lambda: app.scrivi_testo_centrato(app.parola_mascherata),
        State.END: lambda: app.scrivi_testo_centrato('End of list'),
    }

    def handle_show_word(elapsed_ms: int) -> None:
        if elapsed_ms >= app.durata_parola_ms:
            app.stato_presentazione = State.SHOW_MASK
            app.tempo_inizio_stato = pygame.time.get_ticks()

    def handle_show_mask(elapsed_ms: int) -> None:
        if elapsed_ms >= app.durata_maschera_ms and app.avanti:
            next_index = app.indice_parola + 1
            if next_index < len(app.lista_parole):
                app.set_word_index(next_index)
                app.stato_presentazione = State.SHOW_WORD
                app.tempo_inizio_stato = pygame.time.get_ticks()
            else:
                app.stato_presentazione = State.END

    state_updaters = {
        State.SHOW_WORD: handle_show_word,
        State.SHOW_MASK: handle_show_mask,
    }
    

    # ============================================================================
    # MAIN GAME LOOP
    # ============================================================================

    running = True
    clock = pygame.time.Clock()

    while running:
        try:
            # Reset forward flag every frame
            app.avanti = False

            # EVENT HANDLING (always active, regardless of file_caricato state)
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                # ================================================================
                # FILE HANDLING (works even while waiting)
                # ================================================================
                
                if event.type == pygame.DROPFILE:
                    file = os.path.abspath(event.file)
                    file_low = file.lower()

                    if file_low.endswith(('.docx', '.doc')):
                        try:
                            run = app.carica_parola_da_word(file_low)
                            if run:
                                nome_path_completo = str(os.path.basename(file_low))
                                app.nome_file = nome_path_completo.replace('.docx', '').replace('.doc', '')
                                app.file_caricato = True
                                app.stato_presentazione = State.ISTRUCTION
                                app.num_parole = len(app.lista_parole)
                                app.tempo_inizio_stato = pygame.time.get_ticks()
                                if app.full_screen == False:
                                    app.get_full_screen()
                                    app.aggiorna_layout()  
                            else:
                                app.mostra_errore = True
                                app.tipo_errore = Error.EMPTY
                                app.tempo_errore = pygame.time.get_ticks()
                        except Exception as e:
                            app.mostra_errore = True
                            app.tipo_errore = Error.EXCEPTION
                            app.messaggio_errore = str(e)
                            app.tempo_errore = pygame.time.get_ticks()
                            traceback.print_exc()

                    elif file_low.endswith('.txt'):
                        try:
                            run = app.carica_parola_da_txt(file_low)
                            if run:
                                nome_path_completo = str(os.path.basename(file_low))
                                app.nome_file = nome_path_completo.replace('.txt', '')
                                app.file_caricato = True
                                app.stato_presentazione = State.ISTRUCTION
                                app.num_parole = len(app.lista_parole)
                                app.tempo_inizio_stato = pygame.time.get_ticks()
                                if app.full_screen == True:    
                                    app.get_full_screen()
                                    app.aggiorna_layout()
                            else:
                                app.mostra_errore = True
                                app.tipo_errore = Error.EMPTY
                                app.tempo_errore = pygame.time.get_ticks()
                        except Exception as e:
                            app.mostra_errore = True
                            app.tipo_errore = Error.EXCEPTION
                            app.messaggio_errore = str(e)
                            app.tempo_errore = pygame.time.get_ticks()
                            traceback.print_exc()
                    else:
                        app.mostra_errore = True
                        app.tipo_errore = Error.INVALID
                        app.messaggio_errore = os.path.basename(file_low)
                        app.tempo_errore = pygame.time.get_ticks()
                
                # ================================================================
                # KEYBOARD INPUT (only active after file is loaded)
                # ================================================================
                
                if event.type == KEYDOWN:
                    # DEBUG: stampa stato corrente e tasto premuto
                    print(f"Tasto premuto, stato attuale: {app.stato_presentazione}")
                    
                    if event.key == K_p:
                        app.in_pausa = not app.in_pausa
                        app.tempo_inizio_stato = pygame.time.get_ticks()
                        app.aggiorna_layout()
                    if event.key == K_SPACE:
                        app.avanti = True
                    if event.key == K_r:
                        app.set_word_index(0)
                        app.stato_presentazione = State.SHOW_WORD
                        app.tempo_inizio_stato = pygame.time.get_ticks()
                        app.in_pausa = False
                        app.avanti = False
                        app.aggiorna_layout()
                    if event.key == K_i:
                        app.iconifize()
                    if event.key in (K_RETURN, K_KP_ENTER) and app.stato_presentazione == State.MENU_START:
                        print("Cambio a INTRO_TABLE")  # DEBUG
                        app.stato_presentazione = State.INTRO_TABLE
                        app.tempo_inizio_stato = pygame.time.get_ticks()
                        continue
                    elif event.key in (K_RETURN, K_KP_ENTER) and app.stato_presentazione == State.INTRO_TABLE:
                        app.stato_presentazione = State.INTRO_BOOK_OPEN
                        app.tempo_inizio_stato = pygame.time.get_ticks()
                        app.book_animation_completed = False
                        continue
                    elif event.key in (K_RETURN, K_KP_ENTER) and app.stato_presentazione == State.INTRO_BOOK_OPEN:
                        app.stato_presentazione = State.FILE
                        app.tempo_inizio_stato = pygame.time.get_ticks()
                        continue
                    elif event.key in (K_RETURN, K_KP_ENTER) and app.stato_presentazione == State.ISTRUCTION:
                        app.stato_presentazione = State.SHOW_WORD
                        app.tempo_inizio_stato = pygame.time.get_ticks()
                        app.in_pausa = False
                        app.avanti = False
                    # NOTE: F key works only OUTSIDE the instructions screen
                    if event.key == K_f and app.stato_presentazione != State.ISTRUCTION:
                        app.get_full_screen()
                        app.aggiorna_layout()
                    if event.key == K_RIGHT:
                        app.go()
                    if event.key == K_LEFT:
                        app.back()
                    if event.key == K_e:
                        app.reset() 

                # ================================================================
                # MOUSE INPUT (only relevant if slider exists)
                # ================================================================
                
                if app.file_caricato:
                    if event.type == MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = event.pos
                        if abs(mouse_x - app.posizione_cursore) < 20 and abs(mouse_y - app.y_slider) < 20:
                            app.slider_drag = True

                    if event.type == MOUSEMOTION and app.slider_drag:
                        mouse_x, mouse_y = event.pos
                        X_MIN = app.x_slider
                        X_MAX = app.x_slider + app.slider_width
                        if mouse_x < X_MIN:
                            app.posizione_cursore = X_MIN
                        elif mouse_x > X_MAX:
                            app.posizione_cursore = X_MAX
                        else:
                            app.posizione_cursore = mouse_x
                        fattore = (app.posizione_cursore - X_MIN) / (X_MAX - X_MIN)
                        app.durata_parola_ms = settings.DURATA_MIN + fattore * (settings.DURATA_MAX - settings.DURATA_MIN)

                    if event.type == MOUSEBUTTONUP:
                        app.slider_drag = False
                
                # ================================================================
                # WINDOW RESIZE
                # ================================================================
                
                if event.type == VIDEORESIZE:
                    # NOTE: Block resize in instructions screen
                    if app.stato_presentazione == State.ISTRUCTION:
                        continue

                    if event.w < settings.MIN_WIDTH:
                        app.screen_width = settings.MIN_WIDTH
                    else:    
                        app.screen_width = event.w
                    if event.h < settings.MIN_HEIGHT:
                        app.screen_height = settings.MIN_HEIGHT
                    else:
                        app.screen_height = event.h
                    app.screen = pygame.display.set_mode((app.screen_width, app.screen_height), RESIZABLE)
                    app.aggiorna_layout()
                    if app.stato_presentazione == State.FILE:
                        app.disegna_schermata_attesa()
                    if app.stato_presentazione == State.ISTRUCTION:
                        app.disegna_schermata_istruzioni()
                    if app.stato_presentazione in (State.SHOW_WORD, State.SHOW_MASK, State.END):
                        continue
                    app.updating()

            # ====================================================================
            # ERROR DISPLAY (if any error occurred)
            # ====================================================================
            if app.mostra_errore:
                time_occurred = pygame.time.get_ticks() - app.tempo_errore
                if time_occurred < 5000:
                    renderer = error_renderers.get(app.tipo_errore)
                    if renderer:
                        renderer()
                    app.updating()
                    clock.tick(60)
                    continue  # Skip normal rendering
                else:
                    app.mostra_errore = False

            # ====================================================================
            # GAME LOGIC & RENDERING
            # ====================================================================
            
            if app.stato_presentazione == State.INTRO_TABLE:
                actual = pygame.time.get_ticks()
                elapsed = actual - app.tempo_inizio_stato
                if elapsed > settings.INTRO_TABLE_DURATION:
                    app.stato_presentazione = State.INTRO_BOOK_OPEN
                    app.tempo_inizio_stato = pygame.time.get_ticks()
                    app.book_animation_completed = False


            # Waiting mode (no file loaded) 
            if app.stato_presentazione in (State.MENU_START, State.INTRO_TABLE, State.INTRO_BOOK_OPEN):
                # USA LO STATO CORRENTE, non sempre MENU_START
                renderer = state_renderers.get(app.stato_presentazione)
                if renderer:
                    renderer()
                app.updating()
                clock.tick(60)
                continue  

            # Instructions mode
            if app.stato_presentazione == State.ISTRUCTION:
                state_renderers[State.ISTRUCTION]()
                app.updating()
                clock.tick(60)
                continue  

            # Pause mode
            if app.in_pausa:
                app.disegna_schermata_di_pausa()
                app.updating()
                clock.tick(60)
                continue

            # PRESENTATION MODE (only if file loaded and not in instructions)
            if not app.in_pausa:
                tempo_attuale = pygame.time.get_ticks()
                tempo_trascorso = tempo_attuale - app.tempo_inizio_stato
                updater = state_updaters.get(app.stato_presentazione)
                if updater:
                    updater(tempo_trascorso)

            # RENDERING (presentation mode)
            app.color()
            app.disegna_slider()

            renderer = state_renderers.get(app.stato_presentazione)
            if renderer:
                renderer()

            if app.stato_presentazione != State.END:
                app.word_panel()
                app.phrases_panel()
            else:
                app.ended_words_panel()
            app.updating()
            clock.tick(60)

        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()
            pygame.quit()
            sys.exit()

    clock.tick(60)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
