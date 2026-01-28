import streamlit as st
import requests
import json
import os
from urllib.parse import urlparse
# Importação da biblioteca de ordenação
try:
    from streamlit_sortables import sort_items
except ImportError:
    st.error("Erro: Biblioteca 'streamlit-sortables' não instalada. Pare o app e rode: pip install streamlit-sortables")
    st.stop()

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Cyberhub",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. GERENCIAMENTO DE DADOS ---
DATA_FILE = "cyberhub_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {
        "links": [
            {'name': 'Google', 'url': 'https://www.google.com', 'icon': 'https://www.google.com/s2/favicons?domain=google.com&sz=128'},
            {'name': 'GitHub', 'url': 'https://github.com', 'icon': 'https://www.google.com/s2/favicons?domain=github.com&sz=128'},
            {'name': 'YouTube', 'url': 'https://www.youtube.com', 'icon': 'https://www.google.com/s2/favicons?domain=youtube.com&sz=128'},
            {'name': 'Streamlit', 'url': 'https://streamlit.io', 'icon': 'https://www.google.com/s2/favicons?domain=streamlit.io&sz=128'},
            {'name': 'ChatGPT', 'url': 'https://chat.openai.com', 'icon': 'https://www.google.com/s2/favicons?domain=openai.com&sz=128'},
        ]
    }

def save_data():
    data = {"links": st.session_state['links']}
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def fetch_favicon(url):
    try:
        if not url.startswith('http'): url = 'https://' + url
        domain = urlparse(url).netloc
        return f"https://www.google.com/s2/favicons?domain={domain}&sz=128"
    except:
        return "https://cdn-icons-png.flaticon.com/512/25/25694.png"

def get_weather():
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=-25.4284&longitude=-49.2733&current_weather=true"
        response = requests.get(url)
        data = response.json()
        current = data['current_weather']
        return f"CWB // {current['temperature']}°C"
    except:
        return "Offline"

if 'data_loaded' not in st.session_state:
    saved_data = load_data()
    st.session_state['links'] = saved_data['links']
    st.session_state['data_loaded'] = True

# --- 3. CSS OTIMIZADO ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    html, body, [class*="css"], button, input, div, p, h1, h2, h3 {
        font-family: 'Orbitron', sans-serif !important;
    }

    /* Fundo Preto */
    .stApp {
        background-color: #000000;
    }

    /* Topo Colado */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
    }

    /* Widget de Tempo */
    .weather-widget {
        position: fixed;
        top: 15px;
        right: 20px;
        color: #0ff;
        border: 1px solid #0ff;
        padding: 5px 10px;
        border-radius: 6px;
        background: rgba(0,0,0,0.8);
        z-index: 99999;
        font-size: 0.9rem;
        font-weight: bold;
    }

    /* Cards */
    .cyber-link { text-decoration: none !important; }
    
    .cyber-card {
        background: rgba(20, 20, 30, 0.7);
        border: 1px solid #444;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        height: 120px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        transition: transform 0.2s;
        margin-bottom: 15px;
    }
    .cyber-card:hover {
        transform: scale(1.05);
        border-color: #0ff;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
    }
    .cyber-card img {
        width: 40px; 
        height: 40px; 
        margin-bottom: 8px;
        filter: drop-shadow(0 0 5px #0ff);
        object-fit: contain;
    }
    .cyber-card span {
        color: #fff;
        font-size: 0.9rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 100%;
    }

    /* Sidebar Clean */
    [data-testid="stSidebar"] {
        background-color: #050510;
        border-right: 1px solid #333;
    }
    .stButton button {
        background-color: #111 !important;
        color: #f0f !important;
        border: 1px solid #f0f !important;
    }
    .stButton button:hover {
        background-color: #f0f !important;
        color: #fff !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. BARRA LATERAL ---
with st.sidebar:
    st.header("⚙️ SETTINGS")
    
    # --- ÁREA DE REORDENAÇÃO (NOVA) ---
    with st.expander("🔄 REORDER LINKS", expanded=True):
        st.write("Drag items to reorder:")
        
        # Pega apenas os nomes para exibir na lista ordenável
        original_items = [item['name'] for item in st.session_state['links']]
        
        # Cria o componente de ordenação
        sorted_names = sort_items(original_items)
        
        # Se a ordem mudou, atualiza o estado
        if sorted_names != original_items:
            new_order_links = []
            # Reconstrói a lista de dicionários baseada na nova ordem dos nomes
            for name in sorted_names:
                # Encontra o dicionário original correspondente ao nome
                match = next((item for item in st.session_state['links'] if item['name'] == name), None)
                if match:
                    new_order_links.append(match)
            
            st.session_state['links'] = new_order_links
            save_data()
            st.rerun()

    # Adicionar Link
    st.subheader("Add Link")
    with st.form("add_form", clear_on_submit=True):
        new_name = st.text_input("Name")
        new_url = st.text_input("URL")
        new_icon = st.text_input("Custom Icon URL (Optional)")
        
        if st.form_submit_button("ADD"):
            if new_name and new_url:
                if not new_url.startswith('http'): new_url = 'https://' + new_url
                final_icon = new_icon if new_icon else fetch_favicon(new_url)
                st.session_state['links'].append({'name': new_name, 'url': new_url, 'icon': final_icon})
                save_data()
                st.rerun()

    st.write("---")
    # Remover Link
    st.subheader("Remove Link")
    if st.session_state['links']:
        current_names = [l['name'] for l in st.session_state['links']]
        to_remove = st.selectbox("Select link", current_names)
        
        if st.button("DELETE SELECTED"):
            st.session_state['links'] = [l for l in st.session_state['links'] if l['name'] != to_remove]
            save_data()
            st.rerun()

# --- 5. PÁGINA PRINCIPAL ---

# Widget de Tempo
st.markdown(f'<div class="weather-widget">{get_weather()}</div>', unsafe_allow_html=True)

# Título
st.markdown("<h1 style='text-align: center; margin-top: 0px; margin-bottom: 20px; color: #fff; text-shadow: 0 0 10px #f0f; font-size: 2.5rem;'>CYBERHUB</h1>", unsafe_allow_html=True)

# Grid de Links (5 COLUNAS)
links = st.session_state['links']
cols_per_row = 5

for i in range(0, len(links), cols_per_row):
    cols = st.columns(cols_per_row)
    for j in range(cols_per_row):
        if i + j < len(links):
            link = links[i+j]
            with cols[j]:
                st.markdown(f"""
                <a href="{link['url']}" target="_blank" class="cyber-link">
                    <div class="cyber-card">
                        <img src="{link['icon']}" onerror="this.src='https://cdn-icons-png.flaticon.com/512/25/25694.png'">
                        <span>{link['name']}</span>
                    </div>
                </a>
                """, unsafe_allow_html=True)
