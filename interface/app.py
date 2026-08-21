import threading
import customtkinter as ctk
import os
import random
import pygame
import queue

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

COLOR_BG = "#030a12"
COLOR_PANEL = "#071726"
COLOR_BORDER = "#00f0ff"
COLOR_TEXT_NEON = "#00ffff"
COLOR_TEXT_DIM = "#589bb0"

class CacauApp(ctk.CTk):
    def __init__(self, fila_comunicacao=None, fila_comandos=None):
        super().__init__()
        self.fila_gui = fila_comunicacao
        self.fila_comandos = fila_comandos
        
        self.title("CACAU IA - PAINEL DE CONTROLE v2.3")
        self.geometry("1100x700")
        self.minsize(900, 600)
        self.configure(fg_color=COLOR_BG)
        self.resizable(True, True)
        
        self._criar_interface()

        caminho_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pasta_sons = os.path.join(caminho_base, ".funcoes", "efeitos_sonoros")
        
        self._tocar_som_inicial(pasta_sons)

        if self.fila_gui:
            self.after(100, self._escutar_fila_gui)

    def _escutar_fila_gui(self):
        """Verifica continuamente se há mensagens do terminal para exibir na tela."""
        if self.fila_gui:
            while not self.fila_gui.empty():
                try:
                    mensagem = self.fila_gui.get_nowait()
                    tipo = mensagem.get("tipo")
                    conteudo = mensagem.get("conteudo")

                    if tipo == "resposta":
                        self._adicionar_mensagem(f"{conteudo}")
                    elif tipo == "metricas":
                        self._aplicar_texto_metricas(conteudo)
                    elif tipo == "erro":
                        self._adicionar_mensagem(f"[ERRO]: {conteudo}")
                except queue.Empty:
                    break
            
        self.after(100, self._escutar_fila_gui)

    def _tocar_som_inicial(self, pasta_sons):
        def tocar():
            try:
                extensoes = ('.mp3', '.wav', '.ogg')
                if not os.path.exists(pasta_sons):
                    return

                sons = [os.path.join(pasta_sons, f) for f in os.listdir(pasta_sons) if f.lower().endswith(extensoes)]
                
                if not sons:
                    return

                random.shuffle(sons)
                pygame.mixer.init()

                for som in sons:
                    try:
                        pygame.mixer.music.load(som)
                        pygame.mixer.music.play()
                        break
                    except Exception as e:
                        pass

            except Exception:
                pass

        threading.Thread(target=tocar, daemon=True).start()

    def _criar_interface(self):
        self.header = ctk.CTkLabel(
            self, 
            text="❖ CACAU IA ❖", 
            font=ctk.CTkFont(family="Courier", size=20, weight="bold"),
            text_color=COLOR_TEXT_NEON
        )
        self.header.pack(pady=(15, 10))
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=10)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=0, minsize=380)
        self.main_container.grid_rowconfigure(0, weight=1)

        self._montar_painel_chat()
        self._montar_painel_voz_e_status()

    def _montar_painel_chat(self):
        self.frame_chat = ctk.CTkFrame(
            self.main_container, 
            fg_color=COLOR_PANEL, 
            border_color=COLOR_BORDER, 
            border_width=1
        )
        self.frame_chat.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        lbl_chat = ctk.CTkLabel(
            self.frame_chat, 
            text="[ HISTÓRICO DE CHAT & ANÁLISE ]", 
            font=ctk.CTkFont(family="Courier", size=14, weight="bold"),
            text_color=COLOR_TEXT_NEON
        )
        lbl_chat.pack(anchor="w", padx=15, pady=10)

        self.area_chat = ctk.CTkTextbox(
            self.frame_chat, 
            fg_color="#020d18", 
            text_color=COLOR_TEXT_NEON,
            font=ctk.CTkFont(family="Courier", size=12),
            border_color=COLOR_BORDER,
            border_width=1
        )
        self.area_chat.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        self.frame_input = ctk.CTkFrame(self.frame_chat, fg_color="transparent")
        self.frame_input.pack(fill="x", padx=15, pady=(0, 15))
        self.btn_enviar = ctk.CTkButton(
            self.frame_input, 
            text="ENVIAR ➔", 
            fg_color="#005577", 
            hover_color=COLOR_BORDER,
            text_color="#ffffff",
            font=ctk.CTkFont(family="Courier", size=12, weight="bold"),
            command=self.enviar_mensagem_interface,
            width=110
        )
        self.btn_enviar.pack(side="right", padx=(10, 0))

        self.campo_texto = ctk.CTkEntry(
            self.frame_input, 
            placeholder_text="Digite um comando para a Cacau...", 
            fg_color="#020d18",
            text_color=COLOR_TEXT_NEON,
            border_color=COLOR_BORDER,
            font=ctk.CTkFont(family="Courier", size=12)
        )
        self.campo_texto.pack(side="left", fill="x", expand=True)
        self.campo_texto.bind("<Return>", lambda e: self.enviar_mensagem_interface())

    def _montar_painel_voz_e_status(self):
        self.frame_direita = ctk.CTkFrame(
            self.main_container, 
            fg_color=COLOR_PANEL, 
            border_color=COLOR_BORDER, 
            border_width=1,
            width=380
        )
        self.frame_direita.grid(row=0, column=1, sticky="nsew")

        lbl_voz = ctk.CTkLabel(
            self.frame_direita, 
            text="[ COMANDO DE VOZ & FALA ]", 
            font=ctk.CTkFont(family="Courier", size=14, weight="bold"),
            text_color=COLOR_TEXT_NEON
        )
        lbl_voz.pack(anchor="w", padx=15, pady=10)

        self.btn_mic = ctk.CTkButton(
            self.frame_direita, 
            text="🎙 FALAR AGORA (MIC INATIVO)", 
            fg_color="#0a2a3a", 
            hover_color="#104e6e",
            border_color=COLOR_BORDER,
            border_width=1,
            text_color=COLOR_TEXT_NEON,
            font=ctk.CTkFont(family="Courier", size=12, weight="bold"),
            height=40,
            command=self.alternar_microfone
        )
        self.btn_mic.pack(fill="x", padx=15, pady=5)

        self.lbl_wave = ctk.CTkLabel(
            self.frame_direita, 
            text="||| | ||||| ||| |||||| |||| |", 
            font=ctk.CTkFont(family="Courier", size=18, weight="bold"),
            text_color=COLOR_TEXT_DIM
        )
        self.lbl_wave.pack(pady=5)

        self.frame_stats = ctk.CTkFrame(self.frame_direita, fg_color="#020d18", border_color=COLOR_BORDER, border_width=1)
        self.frame_stats.pack(fill="both", expand=True, padx=15, pady=(5, 15))

        lbl_stats_title = ctk.CTkLabel(
            self.frame_stats, 
            text="MÉTRICAS DO SISTEMA", 
            font=ctk.CTkFont(family="Courier", size=11, weight="bold"),
            text_color=COLOR_TEXT_NEON
        )
        lbl_stats_title.pack(anchor="w", padx=10, pady=(5, 0))

        self.lbl_metrics = ctk.CTkTextbox(
            self.frame_stats, 
            fg_color="transparent",
            text_color=COLOR_TEXT_DIM,
            font=ctk.CTkFont(family="Courier", size=11),
            activate_scrollbars=True
        )
        self.lbl_metrics.pack(fill="both", expand=True, padx=5, pady=5)

    def _aplicar_texto_metricas(self, texto):
        self.lbl_metrics.configure(state="normal")
        self.lbl_metrics.delete("1.0", "end")
        self.lbl_metrics.insert("1.0", texto)
        self.lbl_metrics.configure(state="disabled")

    def alternar_microfone(self):
        if "INATIVO" in self.btn_mic.cget("text"):
            self.btn_mic.configure(text="🔴 OUVINDO...", fg_color="#880000")
            self.lbl_wave.configure(text_color=COLOR_TEXT_NEON)
        else:
            self.btn_mic.configure(text="🎙 FALAR AGORA (MIC INATIVO)", fg_color="#0a2a3a")
            self.lbl_wave.configure(text_color=COLOR_TEXT_DIM)

    def enviar_mensagem_interface(self, event=None):
        texto = self.campo_texto.get().strip()
        if not texto:
            return "break"

        self.campo_texto.delete(0, "end")
        self._adicionar_mensagem(f"VOCÊ: {texto}")
        
        if self.fila_comandos:
            self.fila_comandos.put(texto)
        
        return "break"

    def _adicionar_mensagem(self, mensagem):
        self.area_chat.configure(state="normal")
        self.area_chat.insert("end", mensagem + "\n\n")
        self.area_chat.configure(state="disabled")
        self.area_chat.see("end")

    def run(self):
        self.mainloop()