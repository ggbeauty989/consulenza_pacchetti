import streamlit as st
from anthropic import Anthropic

st.set_page_config(
    page_title="Beauty Secrets by GG",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
[data-testid="stSidebar"] { background:#fff5f7; }
.main-header {
    background: linear-gradient(135deg,#f8c8d4,#e8a0b0);
    padding:1.2rem 2rem; border-radius:12px;
    margin-bottom:1.5rem; text-align:center;
}
.main-header h1{color:#6b2d3e;font-size:1.8rem;margin:0}
.main-header p{color:#8b4558;margin:0.2rem 0 0;font-size:0.95rem}
.consulenza-box {
    background:#fff5f7; border:1.5px solid #f0c8d4;
    border-radius:12px; padding:1.5rem 2rem; margin-top:1rem;
}
.step-label {
    font-size:0.72rem; font-weight:600; letter-spacing:0.08em;
    text-transform:uppercase; color:#b06080; margin-bottom:0.3rem;
}
.big-btn > button {
    background:linear-gradient(135deg,#d4548a,#b03070) !important;
    color:white !important; font-size:1.05rem !important;
    font-weight:600 !important; border:none !important;
    border-radius:10px !important; padding:0.7rem 2rem !important;
    width:100% !important;
}
.tratt-row {
    display:flex; align-items:center; gap:10px;
    padding:6px 0; border-bottom:0.5px solid #f0e0e8;
}
.price-pill {
    background:#fde8ed; color:#8b4558;
    padding:2px 10px; border-radius:12px;
    font-size:0.8rem; font-weight:600; white-space:nowrap;
}
.metric-card {
    background:#fff; border:1px solid #f0c8d4;
    border-radius:10px; padding:0.9rem 1.2rem; text-align:center;
}
.metric-card .val{font-size:1.5rem;font-weight:700;color:#6b2d3e}
.metric-card .lbl{font-size:0.75rem;color:#b06080;margin-top:2px}
</style>
""", unsafe_allow_html=True)

# ── Trattamenti ────────────────────────────────────────────────────────────────
TRATTAMENTI_CORPO = [
    {"nome":"Lipolaser","cats":["anticellulite","dimagrante","lipedema"],"prezzo":70},
    {"nome":"Ultraslim","cats":["anticellulite","dimagrante","tonificante","lipedema"],"prezzo":70},
    {"nome":"Vaculight","cats":["anticellulite","dimagrante","tonificante","lipedema"],"prezzo":50},
    {"nome":"Radiofrequenza corpo","cats":["anticellulite","dimagrante","tonificante"],"prezzo":70},
    {"nome":"FitSculptor","cats":["anticellulite","dimagrante","tonificante","lipedema"],"prezzo":95},
    {"nome":"Electraskin","cats":["anticellulite","tonificante"],"prezzo":50},
    {"nome":"DrainPro motion","cats":["anticellulite","dimagrante","tonificante","lipedema"],"prezzo":90},
    {"nome":"Derma current brush","cats":["anticellulite","tonificante"],"prezzo":70},
    {"nome":"Pressoterapia","cats":["anticellulite","lipedema","drenaggio"],"prezzo":20},
    {"nome":"Madera massage","cats":["anticellulite","tonificante","lipedema"],"prezzo":70},
    {"nome":"Hot stone massage","cats":["relax"],"prezzo":70},
    {"nome":"Massaggio linfodrenante","cats":["anticellulite","lipedema","drenaggio"],"prezzo":60},
    {"nome":"Massaggio dimagrante","cats":["dimagrante","lipedema"],"prezzo":60},
    {"nome":"Massaggio tonificante","cats":["anticellulite","dimagrante","tonificante","lipedema"],"prezzo":60},
    {"nome":"Massaggio decontratturante","cats":["decontrattura","relax"],"prezzo":50},
    {"nome":"Vibra luxe","cats":["anticellulite","dimagrante","tonificante","lipedema"],"prezzo":20},
    {"nome":"Lampada collagene","cats":["anticellulite","dimagrante","tonificante","lipedema"],"prezzo":25},
    {"nome":"Ultralift corpo","cats":["anticellulite","dimagrante","tonificante"],"prezzo":200},
    {"nome":"Adipo burn slim","cats":["anticellulite","dimagrante","tonificante","lipedema"],"prezzo":200},
    {"nome":"Bendaggi","cats":["anticellulite","dimagrante","tonificante","lipedema"],"prezzo":40},
    {"nome":"Fanghi","cats":["anticellulite","dimagrante","tonificante","lipedema"],"prezzo":55},
    {"nome":"Cold therapy","cats":["anticellulite","dimagrante","tonificante","lipedema"],"prezzo":60},
    {"nome":"Stretch fix (smagliature)","cats":["tonificante","smagliature"],"prezzo":150},
    {"nome":"Ioniq corpo","cats":["tonificante","smagliature"],"prezzo":150},
    {"nome":"Beauty Waves","cats":["anticellulite","dimagrante","tonificante","lipedema"],"prezzo":90},
]

TRATTAMENTI_VISO = [
    {"nome":"Pure Balance","cats":["purificante","illuminante"],"prezzo":60},
    {"nome":"Clear Spot","cats":["purificante","illuminante","schiarente"],"prezzo":60},
    {"nome":"Even tone","cats":["purificante","tonificante","antirughe","rimpolpante","idratante","illuminante","schiarente"],"prezzo":60},
    {"nome":"Pulizia viso base","cats":["rimpolpante","idratante","illuminante"],"prezzo":40},
    {"nome":"Pulizia del viso ultrasonica","cats":["rimpolpante","idratante","illuminante"],"prezzo":60},
    {"nome":"Hydraskin purity & lift","cats":["purificante","tonificante","antirughe","rimpolpante","idratante","illuminante"],"prezzo":150},
    {"nome":"Jelly skin experience","cats":["rimpolpante","idratante","illuminante"],"prezzo":45},
    {"nome":"Viso regale glow like gold","cats":["rimpolpante","idratante","illuminante"],"prezzo":70},
    {"nome":"Sguardo di luce eye gold ritual","cats":["antirughe","rimpolpante","idratante","illuminante","contorno occhi"],"prezzo":15},
    {"nome":"Peeling viso","cats":["purificante","antirughe","illuminante","schiarente"],"prezzo":60},
    {"nome":"Rituale Idratazione Hanami viso","cats":["rimpolpante","idratante"],"prezzo":65},
    {"nome":"Rituale Detox Illuminante Hanami viso","cats":["purificante","rimpolpante","idratante","illuminante"],"prezzo":60},
    {"nome":"Luxury Glow Hanami viso","cats":["purificante","tonificante","antirughe","illuminante","schiarente"],"prezzo":90},
    {"nome":"Pori zero trattamento niacinamide","cats":["purificante","illuminante"],"prezzo":60},
    {"nome":"Luce vitale trattamento alla vitamina C","cats":["purificante","idratante","illuminante","schiarente"],"prezzo":60},
    {"nome":"Renewal peel trattamento retinolo pro","cats":["purificante","tonificante","antirughe","illuminante"],"prezzo":60},
    {"nome":"Black pore clean naso","cats":["purificante","illuminante"],"prezzo":15},
    {"nome":"Led mask viso","cats":["purificante","tonificante","antirughe","rimpolpante","illuminante","acne"],"prezzo":30},
    {"nome":"Radiofrequenza viso","cats":["tonificante","antirughe","rimpolpante"],"prezzo":50},
    {"nome":"Radiofrequenza viso con infrarossi","cats":["tonificante","antirughe","rimpolpante"],"prezzo":70},
    {"nome":"Veicolazione trasdermica","cats":["tonificante","antirughe","rimpolpante"],"prezzo":50},
    {"nome":"Ossigenoterapia viso","cats":["purificante","idratante","illuminante","acne"],"prezzo":40},
    {"nome":"Scrub ad ultrasuoni","cats":["purificante","illuminante"],"prezzo":40},
    {"nome":"Ioniq viso","cats":["purificante","tonificante","antirughe"],"prezzo":150},
    {"nome":"Hyaluron lips","cats":["rimpolpante","idratante","labbra"],"prezzo":150},
    {"nome":"Hyaluron rughe","cats":["antirughe","rimpolpante"],"prezzo":150},
    {"nome":"Ultralift viso","cats":["tonificante","antirughe","rimpolpante"],"prezzo":200},
    {"nome":"Zero chin","cats":["tonificante","doppio mento"],"prezzo":200},
    {"nome":"Glowinfuse (biorivitalizzazione)","cats":["tonificante","antirughe","rimpolpante","idratante","illuminante","schiarente"],"prezzo":150},
]

SCONTI_CORPO = {4:0.10, 8:0.20, 15:0.30, 32:0.50}
SCONTI_VISO  = {4:0.15, 8:0.25, 15:0.35, 20:0.50}

SYSTEM_PROMPT = """Sei Lily, esperta consulente estetica di "Beauty Secrets by GG".
Quando ricevi i dati di una cliente devi:
1. Consigliare i trattamenti più adatti (SOLO dalla lista fornita) specificando quante sedute per ciascuno
2. Proporre il pacchetto più conveniente (4/8/15/30 sedute con relativi sconti)
3. Calcolare il totale scontato, acconto 30% ed € a seduta
4. Proporre la scaletta delle sedute (ordine, frequenza settimanale, motivazioni)
5. Redigere la scheda cliente completa e professionale
6. Aggiungere consigli domiciliari personalizzati

Rispondi SEMPRE in italiano, con tono professionale ma caldo.
Struttura la risposta con sezioni chiare usando titoli in grassetto.
Non inventare trattamenti non presenti nella lista."""

# ── Sessione ───────────────────────────────────────────────────────────────────
for k, v in {"messages":[], "api_key_ok":False, "client":None}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ✨ Beauty Secrets by GG")
    st.markdown("---")

    # API Key
    api_key_resolved = None
    try:
        api_key_resolved = st.secrets["ANTHROPIC_API_KEY"]
    except (KeyError, FileNotFoundError):
        pass

    if api_key_resolved:
        try:
            st.session_state.client = Anthropic(api_key=api_key_resolved)
            st.session_state.api_key_ok = True
            st.success("✅ Connessa a Claude!")
        except Exception:
            st.error("❌ API key non valida")
            st.session_state.api_key_ok = False
    else:
        st.markdown("### 🔑 API Key")
        api_key_input = st.text_input("API key Anthropic", type="password", placeholder="sk-ant-...")
        if api_key_input:
            try:
                st.session_state.client = Anthropic(api_key=api_key_input)
                st.session_state.api_key_ok = True
                st.success("✅ Connessa!")
            except Exception:
                st.error("❌ Chiave non valida")
                st.session_state.api_key_ok = False

    st.markdown("---")
    st.markdown("### 👤 Dati cliente")
    nome = st.text_input("Nome e cognome", placeholder="es. Maria Rossi")
    c1, c2 = st.columns(2)
    with c1:
        eta = st.number_input("Età", 16, 99, 35)
    with c2:
        data = st.date_input("Data", format="DD/MM/YYYY")
    tipo_pelle = st.selectbox("Tipo di pelle",
        ["—","Grassa","Mista","Normale","Secca","Sensibile","Disidratata","Matura"])
    fototipo = st.selectbox("Fototipo",
        ["—","I – molto chiaro","II – chiaro","III – medio",
         "IV – olivastro","V – scuro","VI – molto scuro"])
    note = st.text_area("Note (allergie, patologie…)", height=80,
        placeholder="es. pacemaker, gravidanza, pelle reattiva…")

# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <h1>✨ Beauty Secrets by GG</h1>
  <p>Consulenza estetica professionale — Lily AI</p>
</div>""", unsafe_allow_html=True)

if not st.session_state.api_key_ok:
    st.info("👈 Inserisci la API key nella barra laterale per iniziare.")
    st.stop()

# ── TABS ───────────────────────────────────────────────────────────────────────
tab_corpo, tab_viso, tab_chat = st.tabs(
    ["🏃 Trattamenti Corpo", "💆 Trattamenti Viso", "💬 Chat con Lily"])


def build_lista_trattamenti(lista):
    return "\n".join(
        f"- {t['nome']} | categorie: {', '.join(t['cats'])} | €{t['prezzo']} a seduta"
        for t in lista
    )

def build_sconti_str(sconti):
    return " | ".join(f"{n} sed. –{int(s*100)}%" for n, s in sconti.items())

def render_tab(tipo, trattamenti, inestetismi_options, sconti, key_prefix):
    """Render comune per tab corpo e viso."""
    etichetta = "corpo" if tipo == "CORPO" else "viso"

    # ── Step 1: inestetismi ─────────────────────────────────────────────────
    st.markdown(f'<div class="step-label">Step 1 — Inestetismi e obiettivi {etichetta}</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    sel_ines = []
    for i, opt in enumerate(inestetismi_options):
        with cols[i % 4]:
            if st.checkbox(opt, key=f"{key_prefix}_ines_{i}"):
                sel_ines.append(opt)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Step 2: pulsante genera ─────────────────────────────────────────────
    st.markdown('<div class="step-label">Step 2 — Genera la consulenza</div>', unsafe_allow_html=True)

    if not nome:
        st.warning("⚠️ Inserisci il nome della cliente nella barra laterale prima di procedere.")
        return

    col_btn, col_info = st.columns([2, 3])
    with col_btn:
        genera = st.button(
            f"✨ Genera consulenza {etichetta} con Lily",
            key=f"btn_{key_prefix}",
            use_container_width=True
        )
    with col_info:
        if sel_ines:
            st.info(f"Inestetismi selezionati: **{', '.join(sel_ines)}**")
        else:
            st.caption("Seleziona almeno un inestetismo per una consulenza mirata.")

    # ── Generazione ─────────────────────────────────────────────────────────
    if genera:
        if not sel_ines:
            st.warning("Seleziona almeno un inestetismo o obiettivo.")
            return

        lista_str = build_lista_trattamenti(trattamenti)
        sconti_str = build_sconti_str(sconti)

        prompt = f"""Devi fare la consulenza estetica {etichetta} per questa cliente:

DATI CLIENTE:
- Nome: {nome}
- Età: {eta} anni
- Tipo di pelle: {tipo_pelle}
- Fototipo: {fototipo}
- Inestetismi / obiettivi: {', '.join(sel_ines)}
- Note / controindicazioni: {note or 'nessuna'}

TRATTAMENTI DISPONIBILI ({etichetta.upper()}:
{lista_str}

PACCHETTI E SCONTI DISPONIBILI:
{sconti_str}

Genera una consulenza completa strutturata così:
**1. ANALISI E DIAGNOSI** — valuta la situazione della cliente
**2. TRATTAMENTI CONSIGLIATI** — elenca ogni trattamento con numero di sedute consigliate e motivazione
**3. SCALETTA DELLE SEDUTE** — proponi l'ordine e la frequenza (es. settimanale/bisettimanale)
**4. PREVENTIVO** — calcola totale a prezzo pieno, pacchetto consigliato con sconto, totale scontato, acconto 30%, € a seduta
**5. SCHEDA CLIENTE** — scheda professionale completa da consegnare
**6. CONSIGLI DOMICILIARI** — skincare/lifestyle per potenziare i risultati"""

        with st.spinner(f"Lily sta elaborando la consulenza {etichetta} per {nome}…"):
            response = st.session_state.client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=2500,
                system=SYSTEM_PROMPT,
                messages=[{"role":"user","content":prompt}]
            )
            result = response.content[0].text

        st.session_state[f"result_{key_prefix}"] = result
        # Salva in chat per riferimento futuro
        st.session_state.messages.append({
            "role": "user",
            "content": f"[Consulenza {tipo} generata per {nome}]"
        })
        st.session_state.messages.append({
            "role": "assistant",
            "content": result
        })

    # ── Mostra risultato ────────────────────────────────────────────────────
    if f"result_{key_prefix}" in st.session_state:
        st.markdown("---")
        st.markdown('<div class="step-label">Consulenza di Lily</div>', unsafe_allow_html=True)
        with st.container():
            st.markdown(st.session_state[f"result_{key_prefix}"])

        st.markdown("---")
        # Bottoni azione dopo la consulenza
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Rigenera consulenza", key=f"regen_{key_prefix}"):
                del st.session_state[f"result_{key_prefix}"]
                st.rerun()
        with col2:
            if st.button("💬 Fai una domanda a Lily su questa consulenza",
                         key=f"goto_chat_{key_prefix}"):
                st.info("Vai alla tab **💬 Chat con Lily** per approfondire!")


# ═══ TAB CORPO ════════════════════════════════════════════════════════════════
with tab_corpo:
    render_tab(
        tipo="CORPO",
        trattamenti=TRATTAMENTI_CORPO,
        inestetismi_options=[
            "Cellulite", "Dimagrimento", "Tonificazione", "Lipedema",
            "Smagliature", "Relax / benessere", "Contratture muscolari",
            "Ritenzione / drenaggio"
        ],
        sconti=SCONTI_CORPO,
        key_prefix="corpo"
    )

# ═══ TAB VISO ════════════════════════════════════════════════════════════════
with tab_viso:
    render_tab(
        tipo="VISO",
        trattamenti=TRATTAMENTI_VISO,
        inestetismi_options=[
            "Pelle grassa / impura", "Pori dilatati", "Perdita di tono",
            "Rughe / segni del tempo", "Mancanza di volume", "Disidratazione",
            "Incarnato spento", "Macchie / iperpigmentazione",
            "Contorno occhi", "Labbra (volume)", "Doppio mento", "Acne / brufoli"
        ],
        sconti=SCONTI_VISO,
        key_prefix="viso"
    )

# ═══ TAB CHAT ════════════════════════════════════════════════════════════════
with tab_chat:
    st.markdown("### 💬 Chatta con Lily")
    st.caption("Approfondisci la consulenza, chiedi varianti, strategie di vendita o qualsiasi domanda sui trattamenti.")

    for msg in st.session_state.messages:
        if msg["content"].startswith("[Consulenza"):
            continue
        avatar = "✨" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    if prompt_chat := st.chat_input("Scrivi a Lily…"):
        st.session_state.messages.append({"role":"user","content":prompt_chat})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt_chat)

        contesto = f"\n[Cliente attuale: {nome}, {eta} anni, pelle {tipo_pelle}]" if nome else ""
        msgs_api = [{"role":m["role"],"content":m["content"]}
                    for m in st.session_state.messages[:-1]]
        msgs_api.append({"role":"user","content":prompt_chat + contesto})

        with st.chat_message("assistant", avatar="✨"):
            with st.spinner("Lily sta scrivendo…"):
                resp = st.session_state.client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=1500,
                    system=SYSTEM_PROMPT,
                    messages=msgs_api
                )
                reply = resp.content[0].text
                st.markdown(reply)

        st.session_state.messages.append({"role":"assistant","content":reply})

    if st.session_state.messages:
        if st.button("🗑️ Cancella conversazione"):
            st.session_state.messages = []
            st.rerun()
