import streamlit as st
from anthropic import Anthropic

# ── Configurazione pagina ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Beauty Secrets by GG – Consulenza Estetica",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS personalizzato ─────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #f8c8d4, #e8a0b0);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .main-header h1 { color: #6b2d3e; font-size: 2rem; margin: 0; }
    .main-header p  { color: #8b4558; margin: 0.3rem 0 0; font-size: 1rem; }
    .section-card {
        background: #fff5f7;
        border: 1px solid #f0c8d4;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
    }
    .section-card h3 { color: #8b4558; margin-bottom: 0.8rem; font-size: 1.05rem; }
    .price-tag {
        background: #fde8ed;
        color: #8b4558;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.82rem;
        font-weight: 600;
    }
    .badge-purificante  { background:#FBEAF0; color:#993556; padding:2px 8px; border-radius:10px; font-size:0.75rem; margin:1px; display:inline-block; }
    .badge-tonificante  { background:#FAEEDA; color:#854F0B; padding:2px 8px; border-radius:10px; font-size:0.75rem; margin:1px; display:inline-block; }
    .badge-antirughe    { background:#E6F1FB; color:#185FA5; padding:2px 8px; border-radius:10px; font-size:0.75rem; margin:1px; display:inline-block; }
    .badge-rimpolpante  { background:#EEEDFE; color:#534AB7; padding:2px 8px; border-radius:10px; font-size:0.75rem; margin:1px; display:inline-block; }
    .badge-idratante    { background:#E1F5EE; color:#0F6E56; padding:2px 8px; border-radius:10px; font-size:0.75rem; margin:1px; display:inline-block; }
    .badge-illuminante  { background:#FAECE7; color:#993C1D; padding:2px 8px; border-radius:10px; font-size:0.75rem; margin:1px; display:inline-block; }
    .badge-schiarente   { background:#F1EFE8; color:#5F5E5A; padding:2px 8px; border-radius:10px; font-size:0.75rem; margin:1px; display:inline-block; }
    .badge-anticellulite{ background:#E1F5EE; color:#0F6E56; padding:2px 8px; border-radius:10px; font-size:0.75rem; margin:1px; display:inline-block; }
    .badge-dimagrante   { background:#E6F1FB; color:#185FA5; padding:2px 8px; border-radius:10px; font-size:0.75rem; margin:1px; display:inline-block; }
    .badge-lipedema     { background:#FBEAF0; color:#993556; padding:2px 8px; border-radius:10px; font-size:0.75rem; margin:1px; display:inline-block; }
    .total-box {
        background: linear-gradient(135deg, #fde8ed, #f8c8d4);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-top: 1rem;
    }
    .total-box h2 { color: #6b2d3e; margin: 0; }
    .stChatMessage { border-radius: 10px; }
    div[data-testid="stSidebar"] { background: #fff5f7; }
</style>
""", unsafe_allow_html=True)

# ── Dati trattamenti CORPO ─────────────────────────────────────────────────────
TRATTAMENTI_CORPO = [
    {"nome": "Lipolaser",                               "cats": ["anticellulite","dimagrante","lipedema"],                               "prezzo": 70},
    {"nome": "Ultraslim",                               "cats": ["anticellulite","dimagrante","tonificante","lipedema"],                  "prezzo": 70},
    {"nome": "Vaculight",                               "cats": ["anticellulite","dimagrante","tonificante","lipedema"],                  "prezzo": 50},
    {"nome": "Radiofrequenza corpo",                    "cats": ["anticellulite","dimagrante","tonificante"],                             "prezzo": 70},
    {"nome": "FitSculptor",                             "cats": ["anticellulite","dimagrante","tonificante","lipedema"],                  "prezzo": 95},
    {"nome": "Electraskin",                             "cats": ["anticellulite","tonificante"],                                          "prezzo": 50},
    {"nome": "DrainPro motion",                         "cats": ["anticellulite","dimagrante","tonificante","lipedema"],                  "prezzo": 90},
    {"nome": "Derma current brush",                     "cats": ["anticellulite","tonificante"],                                          "prezzo": 70},
    {"nome": "Pressoterapia",                           "cats": ["anticellulite","lipedema","drenaggio"],                                 "prezzo": 20},
    {"nome": "Madera massage",                          "cats": ["anticellulite","tonificante","lipedema"],                               "prezzo": 70},
    {"nome": "Hot stone massage",                       "cats": ["relax"],                                                               "prezzo": 70},
    {"nome": "Massaggio linfodrenante",                 "cats": ["anticellulite","lipedema","drenaggio"],                                 "prezzo": 60},
    {"nome": "Massaggio dimagrante",                    "cats": ["dimagrante","lipedema"],                                               "prezzo": 60},
    {"nome": "Massaggio tonificante",                   "cats": ["anticellulite","dimagrante","tonificante","lipedema"],                  "prezzo": 60},
    {"nome": "Massaggio decontratturante",              "cats": ["decontrattura","relax"],                                               "prezzo": 50},
    {"nome": "Vibra luxe",                              "cats": ["anticellulite","dimagrante","tonificante","lipedema"],                  "prezzo": 20},
    {"nome": "Lampada collagene",                       "cats": ["anticellulite","dimagrante","tonificante","lipedema"],                  "prezzo": 25},
    {"nome": "Ultralift corpo (lifting non chirurgico)","cats": ["anticellulite","dimagrante","tonificante"],                             "prezzo": 200},
    {"nome": "Adipo burn slim (liposuzione non chir.)", "cats": ["anticellulite","dimagrante","tonificante","lipedema"],                  "prezzo": 200},
    {"nome": "Bendaggi",                                "cats": ["anticellulite","dimagrante","tonificante","lipedema"],                  "prezzo": 40},
    {"nome": "Fanghi",                                  "cats": ["anticellulite","dimagrante","tonificante","lipedema"],                  "prezzo": 55},
    {"nome": "Cold therapy",                            "cats": ["anticellulite","dimagrante","tonificante","lipedema"],                  "prezzo": 60},
    {"nome": "Stretch fix (smagliature)",               "cats": ["tonificante","smagliature"],                                           "prezzo": 150},
    {"nome": "Ioniq corpo",                             "cats": ["tonificante","smagliature"],                                           "prezzo": 150},
    {"nome": "Beauty Waves",                            "cats": ["anticellulite","dimagrante","tonificante","lipedema"],                  "prezzo": 90},
]

SCONTI_CORPO = {4: 0.10, 8: 0.20, 15: 0.30, 32: 0.50}

# ── Dati trattamenti VISO ──────────────────────────────────────────────────────
TRATTAMENTI_VISO = [
    {"nome": "Pure Balance",                                 "cats": ["purificante","illuminante"],                                                     "prezzo": 60},
    {"nome": "Clear Spot",                                   "cats": ["purificante","illuminante","schiarente"],                                         "prezzo": 60},
    {"nome": "Even tone",                                    "cats": ["purificante","tonificante","antirughe","rimpolpante","idratante","illuminante","schiarente"], "prezzo": 60},
    {"nome": "Pulizia viso base",                            "cats": ["rimpolpante","idratante","illuminante"],                                          "prezzo": 40},
    {"nome": "Pulizia del viso ultrasonica",                 "cats": ["rimpolpante","idratante","illuminante"],                                          "prezzo": 60},
    {"nome": "Hydraskin purity & lift",                      "cats": ["purificante","tonificante","antirughe","rimpolpante","idratante","illuminante"],   "prezzo": 150},
    {"nome": "Jelly skin experience",                        "cats": ["rimpolpante","idratante","illuminante"],                                          "prezzo": 45},
    {"nome": "Viso regale glow like gold",                   "cats": ["rimpolpante","idratante","illuminante"],                                          "prezzo": 70},
    {"nome": "Sguardo di luce eye gold ritual",              "cats": ["antirughe","rimpolpante","idratante","illuminante","contorno occhi"],              "prezzo": 15},
    {"nome": "Peeling viso",                                 "cats": ["purificante","antirughe","illuminante","schiarente"],                             "prezzo": 60},
    {"nome": "Rituale Idratazione Hanami viso",              "cats": ["rimpolpante","idratante"],                                                        "prezzo": 65},
    {"nome": "Rituale Detox Illuminante Hanami viso",        "cats": ["purificante","rimpolpante","idratante","illuminante"],                            "prezzo": 60},
    {"nome": "Luxury Glow Hanami viso",                      "cats": ["purificante","tonificante","antirughe","illuminante","schiarente"],               "prezzo": 90},
    {"nome": "Pori zero trattamento niacinamide",            "cats": ["purificante","illuminante"],                                                     "prezzo": 60},
    {"nome": "Luce vitale trattamento alla vitamina C",      "cats": ["purificante","idratante","illuminante","schiarente"],                            "prezzo": 60},
    {"nome": "Renewal peel trattamento retinolo pro",        "cats": ["purificante","tonificante","antirughe","illuminante"],                           "prezzo": 60},
    {"nome": "Black pore clean naso",                        "cats": ["purificante","illuminante"],                                                     "prezzo": 15},
    {"nome": "Led mask viso",                                "cats": ["purificante","tonificante","antirughe","rimpolpante","illuminante","acne"],       "prezzo": 30},
    {"nome": "Radiofrequenza viso",                          "cats": ["tonificante","antirughe","rimpolpante"],                                         "prezzo": 50},
    {"nome": "Radiofrequenza viso con infrarossi",           "cats": ["tonificante","antirughe","rimpolpante"],                                         "prezzo": 70},
    {"nome": "Veicolazione trasdermica",                     "cats": ["tonificante","antirughe","rimpolpante"],                                         "prezzo": 50},
    {"nome": "Ossigenoterapia viso",                         "cats": ["purificante","idratante","illuminante","acne"],                                  "prezzo": 40},
    {"nome": "Scrub ad ultrasuoni",                          "cats": ["purificante","illuminante"],                                                     "prezzo": 40},
    {"nome": "Ioniq viso",                                   "cats": ["purificante","tonificante","antirughe"],                                         "prezzo": 150},
    {"nome": "Hyaluron lips",                                "cats": ["rimpolpante","idratante","labbra"],                                              "prezzo": 150},
    {"nome": "Hyaluron rughe",                               "cats": ["antirughe","rimpolpante"],                                                      "prezzo": 150},
    {"nome": "Ultralift viso (lifting non chirurgico)",      "cats": ["tonificante","antirughe","rimpolpante"],                                         "prezzo": 200},
    {"nome": "Zero chin (liposuzione non chir. sotto mento)","cats": ["tonificante","doppio mento"],                                                    "prezzo": 200},
    {"nome": "Glowinfuse (biorivitalizzazione)",             "cats": ["tonificante","antirughe","rimpolpante","idratante","illuminante","schiarente"],   "prezzo": 150},
]

SCONTI_VISO = {4: 0.15, 8: 0.25, 15: 0.35, 20: 0.50}

INESTETISMI_CORPO = [
    "Cellulite", "Dimagrimento", "Tonificazione", "Lipedema",
    "Smagliature", "Relax / benessere", "Contratture muscolari", "Ritenzione / drenaggio"
]
INESTETISMI_VISO = [
    "Pelle grassa / impura", "Pori dilatati", "Perdita di tono", "Rughe / segni del tempo",
    "Mancanza di volume", "Disidratazione", "Incarnato spento", "Macchie / iperpigmentazione",
    "Contorno occhi", "Labbra (volume)", "Doppio mento", "Acne / brufoli"
]

# ── Funzioni di calcolo ────────────────────────────────────────────────────────
def calcola_pacchetti(trattamenti_sel, sconti):
    """Restituisce dict con totale scontato per ogni pacchetto."""
    totale_singolo = sum(t["prezzo"] * q for t, q in trattamenti_sel.items() if q > 0)
    risultati = {}
    for n_sed, sconto in sconti.items():
        tot = round(totale_singolo * (1 - sconto))
        tot_sed = sum(q for q in trattamenti_sel.values() if q > 0)
        a_sed = round(tot / tot_sed) if tot_sed > 0 else 0
        risultati[n_sed] = {"totale": tot, "sconto_pct": int(sconto * 100),
                            "a_seduta": a_sed, "acconto": round(tot * 0.3)}
    return totale_singolo, risultati

def formatta_riepilogo(nome, tipo_scheda, inestetismi, trattamenti_sel,
                       pacchetto_scelto, totale_singolo, calcoli):
    """Crea stringa riepilogativa per Claude."""
    tratt_str = "\n".join(
        f"  - {t['nome']} ×{q} (€{t['prezzo']} a seduta)"
        for t, q in trattamenti_sel.items() if q > 0
    )
    n_sed = pacchetto_scelto
    c = calcoli[n_sed]
    return f"""
SCHEDA {tipo_scheda.upper()} — {nome}
Inestetismi / obiettivi: {', '.join(inestetismi)}

Trattamenti selezionati:
{tratt_str}

Totale a prezzo pieno: €{totale_singolo}
Pacchetto scelto: {n_sed} sedute –{c['sconto_pct']}%
Totale scontato: €{c['totale']}
Acconto 30%: €{c['acconto']}
€ a seduta: €{c['a_seduta']}
"""

# ── Prompt di sistema per Claude ───────────────────────────────────────────────
SYSTEM_PROMPT = """Sei Lily, esperta consulente di estetica professionale per il centro "Beauty Secrets by GG".
Hai anni di esperienza in trattamenti viso e corpo: anticellulite, rimodellamento, anti-age, purificazione,
biorivitalizzazione, radiofrequenza e molto altro.

Il tuo compito è:
1. Consigliare i trattamenti più adatti in base agli inestetismi e alle esigenze della cliente
2. Redigere la scheda cliente in modo professionale
3. Spiegare il preventivo/pacchetto valorizzando il percorso estetico
4. Proporre una scaletta/sequenza ottimale dei trattamenti (ordine delle sedute, frequenza consigliata)
5. Rispondere a qualsiasi domanda sui trattamenti estetici con competenza e calore umano

Parla sempre in italiano, con tono professionale ma caldo e rassicurante.
Usa termini estetici corretti. Quando proponi la scaletta, indica l'ordine delle sedute,
la frequenza (es. 1 volta a settimana) e i motivi delle scelte.
Non inventare trattamenti non presenti nella lista fornita.
"""

# ── Stato sessione ─────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "messages": [],
        "api_key_ok": False,
        "client": None,
        "scheda_inviata": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ✨ Beauty Secrets by GG")
    st.markdown("---")

    # API Key
    st.markdown("### 🔑 API Key Claude")
    api_key_input = st.text_input(
        "Inserisci la tua API key Anthropic",
        type="password",
        placeholder="sk-ant-...",
        help="Ottienila su console.anthropic.com",
    )
    if api_key_input:
        try:
            test_client = Anthropic(api_key=api_key_input)
            st.session_state.client = test_client
            st.session_state.api_key_ok = True
            st.success("✅ Connessa a Claude!")
        except Exception:
            st.error("❌ Chiave non valida")
            st.session_state.api_key_ok = False

    st.markdown("---")

    # Dati cliente
    st.markdown("### 👤 Dati cliente")
    nome_cliente = st.text_input("Nome e cognome", placeholder="es. Maria Rossi")
    col1, col2 = st.columns(2)
    with col1:
        eta = st.number_input("Età", min_value=16, max_value=99, value=35, step=1)
    with col2:
        data_today = st.date_input("Data", format="DD/MM/YYYY")

    tipo_pelle = st.selectbox("Tipo di pelle", [
        "—", "Grassa", "Mista", "Normale", "Secca", "Sensibile", "Disidratata", "Matura"
    ])
    fototipo = st.selectbox("Fototipo", [
        "—", "I – molto chiaro", "II – chiaro", "III – medio",
        "IV – olivastro", "V – scuro", "VI – molto scuro"
    ])
    note_aggiuntive = st.text_area(
        "Note (allergie, patologie, gravidanza…)",
        placeholder="es. porta pacemaker, pelle reattiva…",
        height=80,
    )

# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <h1>✨ Beauty Secrets by GG</h1>
  <p>Consulenza estetica professionale — Viso & Corpo</p>
</div>
""", unsafe_allow_html=True)

if not st.session_state.api_key_ok:
    st.info("👈 Inserisci la tua API key nella barra laterale per iniziare.")

# ── TAB PRINCIPALE ─────────────────────────────────────────────────────────────
tab_corpo, tab_viso, tab_chat = st.tabs(["🏃 Trattamenti Corpo", "💆 Trattamenti Viso", "💬 Chat con Lily"])

# ═══════════════════════════════════════════════════════════════════
# TAB CORPO
# ═══════════════════════════════════════════════════════════════════
with tab_corpo:
    st.markdown("### Inestetismi e obiettivi corpo")
    cols = st.columns(4)
    inestetismi_corpo_sel = []
    for i, ines in enumerate(INESTETISMI_CORPO):
        with cols[i % 4]:
            if st.checkbox(ines, key=f"corpo_ines_{i}"):
                inestetismi_corpo_sel.append(ines)

    st.markdown("---")
    st.markdown("### Seleziona trattamenti e numero di sedute")

    # Filtro categoria
    cat_filter_c = st.radio(
        "Mostra per categoria:",
        ["Tutti", "Anticellulite", "Dimagrante", "Tonificante", "Lipedema"],
        horizontal=True,
        key="cat_filter_corpo"
    )
    cat_map_c = {
        "Tutti": None, "Anticellulite": "anticellulite",
        "Dimagrante": "dimagrante", "Tonificante": "tonificante", "Lipedema": "lipedema"
    }
    filtro_c = cat_map_c[cat_filter_c]

    tratt_corpo_sel = {}
    for t in TRATTAMENTI_CORPO:
        if filtro_c and filtro_c not in t["cats"]:
            continue
        col_nome, col_cats, col_prezzo, col_q = st.columns([3, 3, 1, 1])
        with col_nome:
            st.markdown(f"**{t['nome']}**")
        with col_cats:
            badges = " ".join(
                f'<span class="badge-{c}">{c}</span>' for c in t["cats"]
                if c in ["anticellulite","dimagrante","tonificante","lipedema","smagliature"]
            )
            st.markdown(badges, unsafe_allow_html=True)
        with col_prezzo:
            st.markdown(f'<span class="price-tag">€{t["prezzo"]}</span>', unsafe_allow_html=True)
        with col_q:
            q = st.number_input("", min_value=0, max_value=50, value=0, step=1,
                                key=f"q_corpo_{t['nome']}", label_visibility="collapsed")
        if q > 0:
            tratt_corpo_sel[t["nome"]] = {"nome": t["nome"], "prezzo": t["prezzo"], "q": q}

    # Pacchetti corpo
    st.markdown("---")
    st.markdown("### Pacchetto e preventivo")
    pkg_corpo = st.radio(
        "Seleziona il pacchetto:",
        ["4 sedute –10%", "8 sedute –20%", "15 sedute –30%", "30+ sedute –50%"],
        horizontal=True, key="pkg_corpo"
    )
    pkg_map_c = {"4 sedute –10%": 4, "8 sedute –20%": 8, "15 sedute –30%": 15, "30+ sedute –50%": 32}
    n_pkg_c = pkg_map_c[pkg_corpo]

    tratt_obj_c = {
        next(t for t in TRATTAMENTI_CORPO if t["nome"] == v["nome"]): v["q"]
        for v in tratt_corpo_sel.values()
    }
    totale_singolo_c, calcoli_c = calcola_pacchetti(tratt_obj_c, SCONTI_CORPO)

    if tratt_corpo_sel:
        c = calcoli_c[n_pkg_c]
        col1, col2, col3 = st.columns(3)
        col1.metric("Totale scontato", f"€{c['totale']}", f"–{c['sconto_pct']}% su €{totale_singolo_c}")
        col2.metric("Acconto 30%", f"€{c['acconto']}")
        col3.metric("€ a seduta", f"€{c['a_seduta']}")

        st.markdown("---")
        col_a, col_b, col_c = st.columns(3)

        with col_a:
            if st.button("🤖 Consigli AI sui trattamenti", key="btn_consigli_corpo",
                         disabled=not st.session_state.api_key_ok):
                prompt = f"""La cliente {nome_cliente or 'N/D'} ({eta} anni, pelle {tipo_pelle})
presenta i seguenti inestetismi/obiettivi corpo: {', '.join(inestetismi_corpo_sel) if inestetismi_corpo_sel else 'non specificati'}.
Note: {note_aggiuntive or 'nessuna'}.

Ha pre-selezionato questi trattamenti corpo:
{chr(10).join(f"- {v['nome']} ×{v['q']} (€{v['prezzo']} cad.)" for v in tratt_corpo_sel.values())}

Per favore:
1. Valuta se la selezione è adeguata agli obiettivi
2. Suggerisci eventuali trattamenti aggiuntivi o sostituzioni
3. Proponi una scaletta dettagliata delle sedute (ordine, frequenza, motivazione)
4. Dai consigli domiciliari per potenziare i risultati"""
                with st.spinner("Lily sta elaborando i consigli..."):
                    response = st.session_state.client.messages.create(
                        model="claude-sonnet-4-6",
                        max_tokens=1500,
                        system=SYSTEM_PROMPT,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    st.success("**Consigli di Lily:**")
                    st.markdown(response.content[0].text)

        with col_b:
            if st.button("📋 Genera scheda cliente", key="btn_scheda_corpo",
                         disabled=not st.session_state.api_key_ok):
                riepilogo = formatta_riepilogo(
                    nome_cliente or "N/D", "CORPO", inestetismi_corpo_sel,
                    tratt_obj_c, n_pkg_c, totale_singolo_c, calcoli_c
                )
                prompt = f"""Genera una scheda cliente professionale completa per un centro estetico.
Dati: {riepilogo}
Tipo di pelle: {tipo_pelle} | Fototipo: {fototipo} | Età: {eta} anni
Note: {note_aggiuntive or 'nessuna'}

La scheda deve includere: intestazione professionale, dati cliente, analisi degli inestetismi,
percorso trattamenti consigliato con motivazioni, preventivo dettagliato, note per la cliente,
e spazio per firma/data. Usa un formato elegante e professionale."""
                with st.spinner("Lily sta redigendo la scheda..."):
                    response = st.session_state.client.messages.create(
                        model="claude-sonnet-4-6",
                        max_tokens=1800,
                        system=SYSTEM_PROMPT,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    st.success("**Scheda cliente generata:**")
                    st.markdown(response.content[0].text)

        with col_c:
            if st.button("💰 Spiega il preventivo", key="btn_prev_corpo",
                         disabled=not st.session_state.api_key_ok):
                riepilogo = formatta_riepilogo(
                    nome_cliente or "N/D", "CORPO", inestetismi_corpo_sel,
                    tratt_obj_c, n_pkg_c, totale_singolo_c, calcoli_c
                )
                prompt = f"""Presenta questo preventivo alla cliente in modo persuasivo e professionale,
valorizzando il percorso estetico e spiegando il valore di ogni trattamento.
Includi anche i risultati attesi e i tempi previsti.

{riepilogo}"""
                with st.spinner("Lily sta preparando la presentazione..."):
                    response = st.session_state.client.messages.create(
                        model="claude-sonnet-4-6",
                        max_tokens=1200,
                        system=SYSTEM_PROMPT,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    st.success("**Presentazione preventivo:**")
                    st.markdown(response.content[0].text)
    else:
        st.info("Seleziona almeno un trattamento per calcolare il preventivo.")

# ═══════════════════════════════════════════════════════════════════
# TAB VISO
# ═══════════════════════════════════════════════════════════════════
with tab_viso:
    st.markdown("### Problematiche e obiettivi viso")
    cols = st.columns(4)
    inestetismi_viso_sel = []
    for i, ines in enumerate(INESTETISMI_VISO):
        with cols[i % 4]:
            if st.checkbox(ines, key=f"viso_ines_{i}"):
                inestetismi_viso_sel.append(ines)

    st.markdown("---")
    st.markdown("### Seleziona trattamenti e numero di sedute")

    cat_filter_v = st.radio(
        "Mostra per categoria:",
        ["Tutti", "Purificante", "Tonificante", "Antirughe", "Rimpolpante", "Idratante", "Illuminante", "Schiarente"],
        horizontal=True, key="cat_filter_viso"
    )
    cat_map_v = {
        "Tutti": None, "Purificante": "purificante", "Tonificante": "tonificante",
        "Antirughe": "antirughe", "Rimpolpante": "rimpolpante",
        "Idratante": "idratante", "Illuminante": "illuminante", "Schiarente": "schiarente"
    }
    filtro_v = cat_map_v[cat_filter_v]

    tratt_viso_sel = {}
    for t in TRATTAMENTI_VISO:
        if filtro_v and filtro_v not in t["cats"]:
            continue
        col_nome, col_cats, col_prezzo, col_q = st.columns([3, 3, 1, 1])
        with col_nome:
            st.markdown(f"**{t['nome']}**")
        with col_cats:
            cats_show = [c for c in t["cats"]
                         if c in ["purificante","tonificante","antirughe","rimpolpante",
                                  "idratante","illuminante","schiarente"]]
            badges = " ".join(f'<span class="badge-{c}">{c}</span>' for c in cats_show)
            st.markdown(badges, unsafe_allow_html=True)
        with col_prezzo:
            st.markdown(f'<span class="price-tag">€{t["prezzo"]}</span>', unsafe_allow_html=True)
        with col_q:
            q = st.number_input("", min_value=0, max_value=50, value=0, step=1,
                                key=f"q_viso_{t['nome']}", label_visibility="collapsed")
        if q > 0:
            tratt_viso_sel[t["nome"]] = {"nome": t["nome"], "prezzo": t["prezzo"], "q": q}

    # Pacchetti viso
    st.markdown("---")
    st.markdown("### Pacchetto e preventivo")
    st.caption("Sconti viso: 4 sed. –15% · 8 sed. –25% · 15 sed. –35% · 20+ sed. –50%")
    pkg_viso = st.radio(
        "Seleziona il pacchetto:",
        ["4 sedute –15%", "8 sedute –25%", "15 sedute –35%", "20+ sedute –50%"],
        horizontal=True, key="pkg_viso"
    )
    pkg_map_v = {"4 sedute –15%": 4, "8 sedute –25%": 8, "15 sedute –35%": 15, "20+ sedute –50%": 20}
    n_pkg_v = pkg_map_v[pkg_viso]

    tratt_obj_v = {
        next(t for t in TRATTAMENTI_VISO if t["nome"] == v["nome"]): v["q"]
        for v in tratt_viso_sel.values()
    }
    totale_singolo_v, calcoli_v = calcola_pacchetti(tratt_obj_v, SCONTI_VISO)

    if tratt_viso_sel:
        c = calcoli_v[n_pkg_v]
        col1, col2, col3 = st.columns(3)
        col1.metric("Totale scontato", f"€{c['totale']}", f"–{c['sconto_pct']}% su €{totale_singolo_v}")
        col2.metric("Acconto 30%", f"€{c['acconto']}")
        col3.metric("€ a seduta", f"€{c['a_seduta']}")

        st.markdown("---")
        col_a, col_b, col_c = st.columns(3)

        with col_a:
            if st.button("🤖 Consigli AI sui trattamenti", key="btn_consigli_viso",
                         disabled=not st.session_state.api_key_ok):
                prompt = f"""La cliente {nome_cliente or 'N/D'} ({eta} anni, pelle {tipo_pelle}, fototipo {fototipo})
presenta le seguenti problematiche viso: {', '.join(inestetismi_viso_sel) if inestetismi_viso_sel else 'non specificati'}.
Note: {note_aggiuntive or 'nessuna'}.

Ha pre-selezionato questi trattamenti viso:
{chr(10).join(f"- {v['nome']} ×{v['q']} (€{v['prezzo']} cad.)" for v in tratt_viso_sel.values())}

Per favore:
1. Valuta se la selezione è adeguata alle problematiche
2. Suggerisci eventuali trattamenti aggiuntivi o sostituzioni più efficaci
3. Proponi una scaletta dettagliata (ordine delle sedute, frequenza settimanale/mensile, motivazione)
4. Dai consigli su skincare domiciliare per potenziare i risultati"""
                with st.spinner("Lily sta elaborando i consigli..."):
                    response = st.session_state.client.messages.create(
                        model="claude-sonnet-4-6",
                        max_tokens=1500,
                        system=SYSTEM_PROMPT,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    st.success("**Consigli di Lily:**")
                    st.markdown(response.content[0].text)

        with col_b:
            if st.button("📋 Genera scheda cliente", key="btn_scheda_viso",
                         disabled=not st.session_state.api_key_ok):
                riepilogo = formatta_riepilogo(
                    nome_cliente or "N/D", "VISO", inestetismi_viso_sel,
                    tratt_obj_v, n_pkg_v, totale_singolo_v, calcoli_v
                )
                prompt = f"""Genera una scheda cliente professionale completa per un centro estetico (trattamenti viso).
Dati: {riepilogo}
Tipo di pelle: {tipo_pelle} | Fototipo: {fototipo} | Età: {eta} anni
Note: {note_aggiuntive or 'nessuna'}

La scheda deve includere: intestazione professionale del centro "Beauty Secrets by GG",
dati cliente, analisi della pelle e delle problematiche, percorso trattamenti con motivazioni cliniche,
preventivo dettagliato con sconti applicati, consigli domiciliari personalizzati, e spazio firma."""
                with st.spinner("Lily sta redigendo la scheda..."):
                    response = st.session_state.client.messages.create(
                        model="claude-sonnet-4-6",
                        max_tokens=1800,
                        system=SYSTEM_PROMPT,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    st.success("**Scheda cliente generata:**")
                    st.markdown(response.content[0].text)

        with col_c:
            if st.button("💰 Spiega il preventivo", key="btn_prev_viso",
                         disabled=not st.session_state.api_key_ok):
                riepilogo = formatta_riepilogo(
                    nome_cliente or "N/D", "VISO", inestetismi_viso_sel,
                    tratt_obj_v, n_pkg_v, totale_singolo_v, calcoli_v
                )
                prompt = f"""Presenta questo preventivo viso alla cliente in modo persuasivo e professionale,
valorizzando ogni trattamento, spiegando i benefici attesi e la progressione dei risultati seduta per seduta.

{riepilogo}
Tipo di pelle: {tipo_pelle} | Fototipo: {fototipo}"""
                with st.spinner("Lily sta preparando la presentazione..."):
                    response = st.session_state.client.messages.create(
                        model="claude-sonnet-4-6",
                        max_tokens=1200,
                        system=SYSTEM_PROMPT,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    st.success("**Presentazione preventivo:**")
                    st.markdown(response.content[0].text)
    else:
        st.info("Seleziona almeno un trattamento per calcolare il preventivo.")

# ═══════════════════════════════════════════════════════════════════
# TAB CHAT
# ═══════════════════════════════════════════════════════════════════
with tab_chat:
    st.markdown("### 💬 Chatta liberamente con Lily")
    st.caption("Fai qualsiasi domanda sui trattamenti, chiedi consigli, approfondimenti o strategie di vendita.")

    if not st.session_state.api_key_ok:
        st.warning("Inserisci prima la tua API key nella barra laterale.")
    else:
        # Mostra storico messaggi
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"], avatar="✨" if msg["role"] == "assistant" else "👤"):
                st.markdown(msg["content"])

        # Input utente
        if user_input := st.chat_input("Scrivi a Lily…"):
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user", avatar="👤"):
                st.markdown(user_input)

            # Contesto cliente nella chat
            contesto = ""
            if nome_cliente:
                contesto = f"\n[Contesto: stai lavorando con la cliente {nome_cliente}, {eta} anni, pelle {tipo_pelle}]"

            with st.chat_message("assistant", avatar="✨"):
                with st.spinner("Lily sta scrivendo..."):
                    messages_api = [
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages[:-1]
                    ]
                    messages_api.append({
                        "role": "user",
                        "content": user_input + contesto
                    })
                    response = st.session_state.client.messages.create(
                        model="claude-sonnet-4-6",
                        max_tokens=1200,
                        system=SYSTEM_PROMPT,
                        messages=messages_api
                    )
                    reply = response.content[0].text
                    st.markdown(reply)

            st.session_state.messages.append({"role": "assistant", "content": reply})

        if st.session_state.messages:
            if st.button("🗑️ Cancella conversazione"):
                st.session_state.messages = []
                st.rerun()
