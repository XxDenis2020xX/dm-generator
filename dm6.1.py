import customtkinter as ctk
import random

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class DungeonApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("DM Virtual - Solo Adventurer's Toolbox")
        self.geometry("620x640")

        # --- TÍTULO ---
        self.label_titulo = ctk.CTkLabel(self, text="DM VIRTUAL", font=("Roboto", 28, "bold"), text_color="#1255C4")
        self.label_titulo.pack(pady=15)

        # --- PANTALLA DE TEXTO ---
        self.pantalla = ctk.CTkTextbox(self, width=600, height=280, font=("Consolas", 16))
        self.pantalla.pack(pady=10)
        self.pantalla.configure(state="disabled")
        self.mostrar_texto("SISTEMA DM VIRTUAL INICIADO\nEncuentros vinculados automáticamente al Cap. 15.")

        # --- SECCIÓN ORÁCULO ---
        self.frame_oraculo = ctk.CTkFrame(self)
        self.frame_oraculo.pack(pady=5, fill="x", padx=20)
        ctk.CTkLabel(self.frame_oraculo, text="ORÁCULO: SELECCIONA PROBABILIDAD", font=("Arial", 16, "bold")).pack(pady=5)
        self.frame_prob_btns = ctk.CTkFrame(self.frame_oraculo, fg_color="transparent")
        self.frame_prob_btns.pack(pady=5)

        probs = [("Imp (-6)", -6), ("M.Imp (-4)", -4), ("Prob (-2)", -2), ("Pos (0)", 0), ("Prob (+2)", 2), ("M.Prob (+4)", 4), ("Cert (+6)", 6)]
        for texto, valor in probs:
            ctk.CTkButton(self.frame_prob_btns, text=texto, width=75, height=35, command=lambda v=valor, t=texto: self.oraculo(v, t)).pack(side="left", padx=3)

        # --- SECCIÓN GENERADORES ---
        self.frame_gen = ctk.CTkFrame(self)
        self.frame_gen.pack(pady=10, fill="x", padx=20)

        self.btn_escenario = ctk.CTkButton(self.frame_gen, text="ESCENARIO / ENCUENTRO", fg_color="#6ECC85", hover_color="#196325", text_color="black", font=("Arial", 13, "bold"), command=self.encuentro_camino)
        self.btn_escenario.pack(pady=5, padx=10, side="left", expand=True)

        self.btn_npc = ctk.CTkButton(self.frame_gen, text="GENERAR NPC (LISTA + LOOT)", fg_color="#C14BD6", hover_color="#4F1963", text_color="black", font=("Arial", 13, "bold"), command=self.generar_npc_completo)
        self.btn_npc.pack(pady=5, padx=10, side="left", expand=True)

        # --- SECCIÓN DADOS CON MODIFICADOR ---
        self.frame_dados_main = ctk.CTkFrame(self)
        self.frame_dados_main.pack(pady=10, fill="x", padx=20)
        
        self.frame_mod = ctk.CTkFrame(self.frame_dados_main, fg_color="transparent")
        self.frame_mod.pack(pady=5)
        ctk.CTkLabel(self.frame_mod, text="MODIFICADOR:", font=("Arial", 14)).pack(side="left", padx=5)
        self.entry_mod = ctk.CTkEntry(self.frame_mod, width=60)
        self.entry_mod.insert(0, "0")
        self.entry_mod.pack(side="left", padx=5)
        
        self.frame_dados_btns = ctk.CTkFrame(self.frame_dados_main, fg_color="transparent")
        self.frame_dados_btns.pack(pady=5, anchor="center")

        for d in [4, 6, 8, 10, 12, 20, 100]:
            ctk.CTkButton(self.frame_dados_btns, text=f"d{d}", width=55, command=lambda x=d: self.tirar_dado(x)).pack(side="left", padx=5, pady=5)

    def mostrar_texto(self, texto):
        self.pantalla.configure(state="normal")
        self.pantalla.delete("0.0", "end")
        self.pantalla.insert("0.0", texto)
        self.pantalla.configure(state="disabled")

    def obtener_tabla_dungeon(self):
        """Genera un evento de entorno cuando NO hay monstruos"""
        eventos = [
            "ATMÓSFERA: Las antorchas chisporrotean y una brisa fría recorre el pasillo.",
            "RUIDO: Escuchas el goteo constante de agua y un eco metálico lejano.",
            "PELIGRO: El suelo está inestable; escombros bloquean parcialmente el paso.",
            "PISTA: Encuentras marcas de garras recientes en la pared derecha.",
            "EXTRAÑO: Un olor a ozono satura el aire de repente.",
            "SISTEMA: Encuentras una consola con datos corruptos sobre el Site 15.",
            "CALMA: La zona parece segura para un descanso corto."
        ]
        return f"\n--- DETALLE DEL DUNGEON ---\n>> {random.choice(eventos)}"

    def obtener_tactica_monstruo(self):
        """Lógica interna de la Monster Intentions Table (Capítulo 15)"""
        d100 = random.randint(1, 100)
        distancia = (random.randint(1, 10) * 10) + 20
        
        if d100 <= 4: res = "HUYE: El monstruo está aterrado y escapa."
        elif d100 <= 9: res = "CURIOSO: Observa a distancia. Posible interacción pacífica."
        elif d100 <= 14: res = "ACECHO: Te sigue oculto esperando tu debilidad."
        elif d100 <= 19: res = "RANGO: Ataca a distancia y mantiene los pies de separación."
        elif d100 <= 24: res = "CAPTURA: Intenta dejarte inconsciente, no matarte."
        elif d100 <= 30: res = "ALERTA: Muy difícil de sorprender (Sigilo con desventaja)."
        else: res = "ATAQUE: Lucha agresiva y directa."
        
        return f"\n--- TÁCTICA MONSTRUO (Cap. 15 | d100: {d100}) ---\n>> {res}\n>> DISTANCIA INICIAL: {distancia} pies."

    def encuentro_camino(self):
        """Lógica exclusiva: O Monstruo (Cap 15) O Detalle de Dungeon"""
        encuentros = [
            ("Emboscada de Goblins", True),
            ("Un viajero herido que pide ayuda", False),
            ("Ruinas antiguas con guardianes", True),
            ("Un claro con agua pura y bendecida", False),
            ("Rastros de un monstruo hambriento", True),
            ("Un grupo de bandidos buscando pelea", True),
            ("Un mercader con su escolta", False),
            ("Un pasillo sospechosamente vacío", False)
        ]
        
        nombre, es_combate = random.choice(encuentros)
        mensaje = f"ESCENARIO: {nombre}\n"
        
        if es_combate:
            mensaje += self.obtener_tactica_monstruo()
        else:
            mensaje += self.obtener_tabla_dungeon()
            
        self.mostrar_texto(mensaje)

    def oraculo(self, mod, nombre):
        d20 = random.randint(1, 20)
        total = d20 + mod
        res = "NO." if total <= 6 else "TAL VEZ..." if total <= 12 else "SÍ."
        extra = ""
        if res == "TAL VEZ...":
            extra = f"\n\nEVENTO: {random.choice(['Sonido extraño', 'Cambio de clima', 'Presencia lejana'])}"
        self.mostrar_texto(f"ORÁCULO [{nombre}]\nTirada: {d20} + ({mod}) = {total}\n\nRESULTADO: {res}{extra}")

    def generar_npc_completo(self):
        """Generación de NPC con Nombre, Profesión, Edad y Género (Capítulo 13)"""
        nombres = ["Alaric", "Elowen", "Kaelen", "Thrain", "Lyra", "Korg", "Sana", "Marek", "Zora", "Valen"]
        profesiones = ["Mercader", "Guardia", "Erudito", "Artesano", "Cazador", "Sacerdote", "Pícaro", "Cocinero"]
        generos = ["Masculino", "Femenino"]
        edades = [f"{random.randint(18, 25)} (Joven)", f"{random.randint(26, 45)} (Adulto)", f"{random.randint(46, 75)} (Veterano)"]
        
        raza = random.choice(["Humano", "Elfo", "Enano", "Mediano", "Semi-Orco", "Tiefling"])
        nombre = random.choice(nombres)
        profesion = random.choice(profesiones)
        genero = random.choice(generos)
        edad = random.choice(edades)
        
        stats = {k: random.randint(8, 16) for k in ["Str", "Dex", "Con", "Int", "Wis", "Cha"]}
        
        desc = f"NOMBRE: {nombre}\n"
        desc += f"PERFIL: {genero} | {raza} | {profesion}\n"
        desc += f"EDAD: {edad}\n"
        desc += "-"*30 + "\n"
        for k, v in stats.items():
            desc += f"** {k}: {v}\n"
        desc += "-"*30 + f"\nLOOT: {random.randint(5, 50)} mo."
        
        self.mostrar_texto(desc)

    def tirar_dado(self, caras):
        try: mod_val = int(self.entry_mod.get())
        except: mod_val = 0
        base = random.randint(1, caras)
        self.mostrar_texto(f"DADO d{caras}\nBase: {base} | Mod: {mod_val}\n\n>>> TOTAL: {base + mod_val}")

if __name__ == "__main__":
    app = DungeonApp()
    app.mainloop()