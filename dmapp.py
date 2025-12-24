import streamlit as st
import random

# Configuración de la página para móvil y escritorio
st.set_page_config(page_title="DM Virtual - Site 15", page_icon="🎲", layout="centered")

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; font-weight: bold; }
    .stTextArea>div>div>textarea { font-family: 'Consolas', monospace; font-size: 16px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE APOYO (Mantenida del original) ---

def obtener_tabla_dungeon():
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

def obtener_tactica_monstruo():
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

# --- INTERFAZ STREAMLIT ---

st.title("🎲 DM VIRTUAL")
st.caption("SISTEMA DE APOYO - SOLO ADVENTURER'S TOOLBOX")

# Inicializar historial en la sesión para que no se borre al pulsar botones
if 'pantalla' not in st.session_state:
    st.session_state.pantalla = "SISTEMA DM VIRTUAL INICIADO\nEncuentros vinculados automáticamente al Cap. 15."

# Área de visualización (Consola)
st.text_area("LOG DE AVENTURA", value=st.session_state.pantalla, height=250, disabled=True, key="log_area")

# --- SECCIÓN ORÁCULO ---
st.subheader("🔮 Oráculo")
cols_orac = st.columns(4)
probs = [("Imp (-6)", -6), ("M.Imp (-4)", -4), ("Prob (-2)", -2), ("Pos (0)", 0), 
         ("Prob (+2)", 2), ("M.Prob (+4)", 4), ("Cert (+6)", 6)]

# Dividir botones del oráculo en filas para móvil
for i, (texto, valor) in enumerate(probs):
    with cols_orac[i % 4]:
        if st.button(texto):
            d20 = random.randint(1, 20)
            total = d20 + valor
            res = "NO." if total <= 6 else "TAL VEZ..." if total <= 12 else "SÍ."
            extra = f"\n\nEVENTO: {random.choice(['Sonido extraño', 'Cambio de clima', 'Presencia lejana'])}" if res == "TAL VEZ..." else ""
            st.session_state.pantalla = f"ORÁCULO [{texto}]\nTirada: {d20} + ({valor}) = {total}\n\nRESULTADO: {res}{extra}"
            st.rerun()

# --- SECCIÓN GENERADORES ---
st.subheader("🛠️ Generadores")
col_gen1, col_gen2 = st.columns(2)

with col_gen1:
    if st.button("🗺️ ESCENARIO", use_container_width=True):
        encuentros = [("Emboscada de Goblins", True), ("Viajero herido", False), ("Ruinas antiguas", True), 
                      ("Claro bendecido", False), ("Rastros de monstruo", True), ("Bandidos", True), 
                      ("Mercader", False), ("Pasillo vacío", False)]
        nombre, es_combate = random.choice(encuentros)
        mensaje = f"ESCENARIO: {nombre}\n"
        mensaje += obtener_tactica_monstruo() if es_combate else obtener_tabla_dungeon()
        st.session_state.pantalla = mensaje
        st.rerun()

with col_gen2:
    if st.button("👤 GENERAR NPC", use_container_width=True):
        nombres = ["Alaric", "Elowen", "Kaelen", "Thrain", "Lyra", "Korg", "Sana", "Marek", "Zora", "Valen"]
        profesiones = ["Mercader", "Guardia", "Erudito", "Artesano", "Cazador", "Sacerdote", "Pícaro", "Cocinero"]
        raza = random.choice(["Humano", "Elfo", "Enano", "Mediano", "Semi-Orco", "Tiefling"])
        stats = {k: random.randint(8, 16) for k in ["Str", "Dex", "Con", "Int", "Wis", "Cha"]}
        
        desc = f"NOMBRE: {random.choice(nombres)}\n"
        desc += f"PERFIL: {random.choice(['Masculino', 'Femenino'])} | {raza} | {random.choice(profesiones)}\n"
        desc += f"EDAD: {random.randint(18, 70)}\n" + "-"*20 + "\n"
        for k, v in stats.items(): desc += f"{k}: {v}  "
        desc += f"\nLOOT: {random.randint(5, 50)} mo."
        st.session_state.pantalla = desc
        st.rerun()

# --- SECCIÓN DADOS ---
st.subheader("🎲 Dados")
mod_val = st.number_input("Modificador de tirada", value=0, step=1)

cols_dados = st.columns(7)
dados = [4, 6, 8, 10, 12, 20, 100]

for i, caras in enumerate(dados):
    with cols_dados[i]:
        if st.button(f"d{caras}"):
            base = random.randint(1, caras)
            st.session_state.pantalla = f"DADO d{caras}\nBase: {base} | Mod: {mod_val}\n\n>>> TOTAL: {base + mod_val}"
            st.rerun()

st.divider()
st.info("Para instalar en Android: Abre en Chrome, toca los 3 puntos ⋮ y selecciona 'Instalar aplicación'.")