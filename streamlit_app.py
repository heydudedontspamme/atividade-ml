import streamlit as st
import os
from google import genai
from google.genai import types

# Remove hardcoded API key and fetch it from Streamlit secrets
api_key = st.secrets["google_gemini_api_key"]

# Page Configuration
st.set_page_config(
    page_title="Resume Spinner",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .stTextArea textarea {
        font-size: 1.1rem;
        border-radius: 10px;
    }
    .stButton button {
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
    }
    div[data-testid="stExpander"] {
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        background-color: #f8fafc;
    }
    .success-box {
        padding: 1rem;
        background-color: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 10px;
        color: #166534;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- Translations ---
TRANSLATIONS = {
    "en": {
        "title": "Resume Spinner",
        "subtitle": "Corporate Translation Engine",
        "sidebar_title": "Configuration",
        "language_label": "Language / Idioma",
        "step1_title": "1. Input Reality",
        "step1_desc": "Describe what actually happened. Be honest. We won't judge.",
        "placeholder": "e.g., I accidentally deleted the entire user database...",
        "button_spin": "Spin It ✨",
        "button_loading": "Generating Synergy...",
        "result_title": "2. Corporate Translation",
        "truth_label": "THE TRUTH",
        "spin_label": "THE SPIN",
        "history_title": "History",
        "history_subtitle": "Your track record of \"success\"",
        "error_input": "Please enter an experience to spin.",
        "error_api": "Failed to synergize the output stream.",
        "success_msg": "Successfully spun!",
        "footer": "© 2024 CorpSpeak Inc. Synergizing backward overflow."
    },
    "pt-br": {
        "title": "Resume Spinner",
        "subtitle": "Motor de Tradução Corporativa",
        "sidebar_title": "Configuração",
        "language_label": "Language / Idioma",
        "step1_title": "1. Realidade",
        "step1_desc": "Descreva o que realmente aconteceu. Seja honesto. Não vamos julgar.",
        "placeholder": "ex: Eu deletei acidentalmente todo o banco de dados de usuários...",
        "button_spin": "Transformar ✨",
        "button_loading": "Gerando Sinergia...",
        "result_title": "2. Tradução Corporativa",
        "truth_label": "A REALIDADE",
        "spin_label": "VERSÃO CORPORATIVA",
        "history_title": "Histórico",
        "history_subtitle": "Seu histórico de \"sucesso\"",
        "error_input": "Por favor, insira uma experiência.",
        "error_api": "Falha ao conectar à matriz de sinergia.",
        "success_msg": "Transformado com sucesso!",
        "footer": "© 2024 CorpSpeak Inc. Sinergizando o fluxo reverso."
    }
}

# --- State Management ---
if "language" not in st.session_state:
    st.session_state.language = "en"
if "history" not in st.session_state:
    st.session_state.history = []

# --- Sidebar ---
with st.sidebar:
    st.title("⚙️ " + TRANSLATIONS[st.session_state.language]["sidebar_title"])
    
    # Language Toggle
    lang_choice = st.radio(
        TRANSLATIONS[st.session_state.language]["language_label"],
        ["English", "Português (BR)"],
        index=0 if st.session_state.language == "en" else 1
    )
    
    st.session_state.language = "en" if lang_choice == "English" else "pt-br"
    
    st.divider()
    st.markdown(f"**{TRANSLATIONS[st.session_state.language]['history_title']}**")
    
    if not st.session_state.history:
        st.caption("No history yet." if st.session_state.language == "en" else "Nenhum histórico.")
    else:
        for idx, item in enumerate(st.session_state.history):
            with st.expander(f"{item['original'][:25]}...", expanded=False):
                st.caption(item['timestamp'])
                st.write(f"**Original:** {item['original']}")
                st.write(f"**Spin:** {item['spun']}")
                st.code(item['spun'], language=None)

# --- Main Content ---
t = TRANSLATIONS[st.session_state.language]

st.title(f"💼 {t['title']}")
st.caption(t['subtitle'])
st.divider()

col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader(t['step1_title'])
    st.info(t['step1_desc'])
    
    user_input = st.text_area(
        "Input", 
        placeholder=t['placeholder'], 
        height=150, 
        label_visibility="collapsed"
    )
    
    spin_btn = st.button(t['button_spin'], type="primary", use_container_width=True)

    if spin_btn:
        if not user_input.strip():
            st.error(t['error_input'])
        else:
            try:
                client = genai.Client(api_key=api_key)
                
                with st.spinner(t['button_loading']):
                    # Prompt Construction
                    if st.session_state.language == 'pt-br':
                        sys_instruct = """
                            Você é um especialista em Redação de Currículos e Comunicação Corporativa, especializado em "Corporate Speak".
                            Seu objetivo é pegar uma experiência de trabalho negativa e reescrevê-la como um ponto de currículo brilhante.
                            Regras:
                            1. Transforme falhas em "pivôs estratégicos".
                            2. Transforme preguiça em "maximização de eficiência".
                            3. Transforme demissão em "conclusão de ciclo contratual".
                            4. Use palavras como: sinergia, alavancar, orquestrar, liderar, mudança de paradigma, stakeholders, KPI.
                            5. A saída DEVE ser um único ponto de lista conciso, mas prolixo, em PORTUGUÊS DO BRASIL.
                        """
                    else:
                        sys_instruct = """
                            You are an expert Resume Writer and Corporate Communications Specialist specializing in "Corporate Speak". 
                            Your goal is to take a negative work experience and rewrite it into a glowing resume bullet point.
                            Rules:
                            1. Turn failures into "strategic pivots".
                            2. Turn laziness into "efficiency maximization".
                            3. Turn getting fired into "seeking new challenges".
                            4. Use words like: synergize, leverage, orchestrate, spearhead, paradigm shift, stakeholders, KPI.
                            5. The output MUST be a single, concise, but wordy bullet point.
                        """

                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=user_input,
                        config=types.GenerateContentConfig(
                            system_instruction=sys_instruct,
                            temperature=0.9,
                            top_p=0.95,
                            top_k=40
                        )
                    )
                    
                    result_text = response.text.strip()
                    
                    # Add to history
                    import datetime
                    st.session_state.history.insert(0, {
                        "original": user_input,
                        "spun": result_text,
                        "timestamp": datetime.datetime.now().strftime("%H:%M")
                    })
                    
                    # Trigger a rerun to update history sidebar immediately
                    st.rerun()
                    
            except Exception as e:
                st.error(f"{t['error_api']} ({str(e)})")

# Display Results (if any)
with col2:
    if st.session_state.history:
        latest = st.session_state.history[0]
        
        st.subheader(t['result_title'])
        
        container = st.container(border=True)
        with container:
            st.caption(t['truth_label'])
            st.write(f"_{latest['original']}_")
            
            st.divider()
            
            st.caption(t['spin_label'])
            st.markdown(f"#### {latest['spun']}")
            
            # Streamlit code block enables one-click copy
            st.code(latest['spun'], language=None)
            st.success(t['success_msg'])

st.divider()
st.markdown(f"<div style='text-align: center; color: #94a3b8;'>{t['footer']}</div>", unsafe_allow_html=True)
