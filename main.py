"""
Tachistostory - Main Entry Point
Speed reading training application using tachistoscope technique.
"""

import pygame 
import pygame
from pygame.locals import (
    QUIT, KEYDOWN, K_SPACE, K_RETURN, K_p, K_r, K_f, K_i,
    MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, VIDEORESIZE,
    K_KP_ENTER, RESIZABLE
)
import sys
import os
import traceback
import settings
from game import Tachistostory

# ============================================================================
# GAME INITIALIZATION
# ============================================================================
def main():
    app = Tachistostory()
    app.get_screen()
    app.caption_window()
    app.get_font()  
    app.load_assets() 
    app.disegna_schermata_attesa() 
    app.helper_slider(settings.DURATA_MIN, settings.DURATA_MAX)
    app.tempo_inizio_stato = pygame.time.get_ticks()

    # ============================================================================
    # MAIN GAME LOOP
    # ============================================================================

    running = True

    while running:
        try:
            #Clock timing
            clock = pygame.time.Clock()
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
                                app.stato_presentazione = 'istruzioni'
                                app.num_parole = len(app.lista_parole)
                                app.tempo_inizio_stato = pygame.time.get_ticks()
                                app.get_full_screen()
                                app.aggiorna_layout()  
                            else:
                                print('Document not readable or empty. Please try again')
                        except Exception as e:
                            print(f"An error occurred: {e}, please try again")
                            traceback.print_exc()

                    elif file_low.endswith('.txt'):
                        try:
                            run = app.carica_parola_da_txt(file_low)
                            if run:
                                nome_path_completo = str(os.path.basename(file_low))
                                app.nome_file = nome_path_completo.replace('.txt', '')
                                app.file_caricato = True
                                app.stato_presentazione = 'istruzioni'
                                app.num_parole = len(app.lista_parole)
                                app.tempo_inizio_stato = pygame.time.get_ticks()
                                app.get_full_screen()
                                app.aggiorna_layout()  
                        except Exception as e:
                            print(f"An error occurred: {e}, please try again")
                            traceback.print_exc()
                    else:
                        print(f'{file} is not valid. Please try again')
                
                # ================================================================
                # KEYBOARD INPUT (only active after file is loaded)
                # ================================================================
                
                if event.type == KEYDOWN and app.file_caricato:
                    if event.key == K_p:
                        app.in_pausa = not app.in_pausa
                        app.tempo_inizio_stato = pygame.time.get_ticks()
                        app.aggiorna_layout()
                    if event.key == K_SPACE:
                        app.avanti = True
                    if event.key == K_r:
                        app.indice_parola = 0
                        app.parola_corrente = app.lista_parole[0]
                        app.parola_mascherata = app.maschera_parola(app.parola_corrente)
                        app.stato_presentazione = 'show_word'
                        app.tempo_inizio_stato = pygame.time.get_ticks()
                        app.in_pausa = False
                        app.avanti = False
                        app.aggiorna_layout()
                    if event.key == K_i:
                        app.iconifize()
                    if event.key in (K_RETURN, K_KP_ENTER) and app.stato_presentazione == 'istruzioni':
                        app.stato_presentazione = "show_word"
                        app.tempo_inizio_stato = pygame.time.get_ticks()
                        app.in_pausa = False
                        app.avanti = False
                    # NOTE: F key works only OUTSIDE the instructions screen
                    if event.key == K_f and app.stato_presentazione != 'istruzioni':
                        app.get_full_screen()
                        app.aggiorna_layout()

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
                    if app.stato_presentazione == 'istruzioni':
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
                    if app.stato_presentazione == 'attesa_file':
                        app.disegna_schermata_attesa()
                    if app.stato_presentazione == 'istruzioni':
                        app.disegna_schermata_istruzioni()
                    if app.stato_presentazione in ('show_word', 'show_mask', 'fine'):
                        continue
                    app.updating()

            # ====================================================================
            # GAME LOGIC & RENDERING
            # ====================================================================
            
            # Waiting mode (no file loaded)
            if not app.file_caricato:
                # WAITING SCREEN MODE
                app.disegna_schermata_attesa()
                app.updating()
                continue  

            # Instructions mode
            if app.stato_presentazione == 'istruzioni':
                app.disegna_schermata_istruzioni()
                app.updating()
                continue  

            # Pause mode
            if app.in_pausa:
                app.disegna_schermata_di_pausa()
                app.updating()
                continue

            # PRESENTATION MODE (only if file loaded and not in instructions)
            if not app.in_pausa:
                tempo_attuale = pygame.time.get_ticks()
                tempo_trascorso = tempo_attuale - app.tempo_inizio_stato
                
                if app.stato_presentazione == 'show_word':
                    if tempo_trascorso >= app.durata_parola_ms:
                        app.stato_presentazione = 'show_mask'
                        app.tempo_inizio_stato = pygame.time.get_ticks()

                elif app.stato_presentazione == 'show_mask':
                    if tempo_trascorso >= app.durata_maschera_ms and app.avanti:
                        app.indice_parola += 1
                        if app.indice_parola < len(app.lista_parole):
                            app.parola_corrente = app.lista_parole[app.indice_parola]
                            app.parola_mascherata = app.maschera_parola(app.parola_corrente)
                            app.stato_presentazione = 'show_word'
                            app.tempo_inizio_stato = pygame.time.get_ticks()
                        else:
                            app.stato_presentazione = 'fine'

            # RENDERING (presentation mode)
            app.color()
            app.disegna_slider()

            if app.stato_presentazione == 'show_word':
                app.scrivi_testo_centrato(app.parola_corrente)
            elif app.stato_presentazione == 'show_mask':
                app.scrivi_testo_centrato(app.parola_mascherata)
            elif app.stato_presentazione == 'fine':
                app.scrivi_testo_centrato('End of list')

            app.pannello_informativo()
            app.updating()

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

