import streamlit as st
import anthropic
from datetime import datetime

st.set_page_config(page_title="ReelScript AI", page_icon="🎬", layout="centered")

st.markdown("""
<style>
.stButton>button {
    background-color: #FF4B4B;
    color: white;
    font-weight: bold;
    border-radius: 10px;
    padding: 10px 24px;
}
</style>
""", unsafe_allow_html=True)

if 'roteiros_gerados' not in st.session_state:
    st.session_state.roteiros_gerados = 0
if 'historico' not in st.session_state:
    st.session_state.historico = []

def gerar_roteiro(api_key, nicho, duracao, tom, objetivo, tema_extra=""):
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        tema = f"{nicho} - {tema_extra}" if tema_extra else nicho
        
        prompt = f"""Crie um roteiro VIRAL para Reels/TikTok de {duracao} segundos sobre {tema}.

Tom: {tom} | Objetivo: {objetivo}

ESTRUTURA:

🎯 GANCHO (0-3s):
- Frase impactante que para o scroll
- Curiosidade/polêmica

📖 DESENVOLVIMENTO ({int(duracao*0.7)}s):
- 3-5 pontos principais
- Transições sugeridas

🔥 CTA (últimos 3s):
- Ação para o espectador

🎵 TRILHA:
- Estilo musical
- Trending sounds

🎬 DICAS DE GRAVAÇÃO:
- Enquadramentos
- Cortes/efeitos

💡 HASHTAGS:
- 5-8 hashtags em alta

Seja ESPECÍFICO e PRÁTICO."""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text
    
    except Exception as e:
        return f"❌ Erro: {str(e)}"

st.title("🎬 ReelScript AI")
st.subheader("Gerador de Roteiros Virais")

api_key = st.text_input("🔑 API Key da Claude:", type="password", 
                        help="Pegue em: https://console.anthropic.com")

if not api_key:
    st.warning("⚠️ Cole sua API Key acima para continuar")
    st.info("📌 console.anthropic.com → API Keys → Create Key")
    st.stop()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Gerados", st.session_state.roteiros_gerados)
with col2:
    restantes = max(0, 3 - st.session_state.roteiros_gerados)
    st.metric("Restantes", restantes)
with col3:
    st.metric("Status", "🟢" if restantes > 0 else "🔴")

st.markdown("---")

if st.session_state.roteiros_gerados >= 3:
    st.error("🚫 Limite atingido!")
    st.info("💎 Premium: Ilimitado por R$ 24,90/mês")
    st.stop()

with st.form("form"):
    st.subheader("⚙️ Configure o Roteiro")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        nicho = st.selectbox("🎯 Nicho:", [
            "💰 Finanças", "🧠 Desenvolvimento", "💪 Fitness",
            "🚀 Empreendedorismo", "❤️ Relacionamentos",
            "🍳 Culinária", "🤖 Tech & IA", "✈️ Viagens"
        ])
        duracao = st.selectbox("⏱️ Duração:", [15, 30, 60, 90])
    
    with col_b:
        tom = st.selectbox("🎭 Tom:", [
            "Energético", "Educativo", "Humorístico",
            "Inspirador", "Polêmico"
        ])
        objetivo = st.selectbox("🎯 Objetivo:", [
            "Viralizar", "Educar", "Vender", "Crescer", "Engajar"
        ])
    
    tema_extra = st.text_input("💡 Tema específico (opcional):", 
                               placeholder="Ex: ganhar dinheiro com IA")
    
    submitted = st.form_submit_button("✨ GERAR ROTEIRO", use_container_width=True)

if submitted:
    with st.spinner("🎬 Criando roteiro..."):
        roteiro = gerar_roteiro(api_key, nicho, duracao, tom, objetivo, tema_extra)
        
        st.session_state.roteiros_gerados += 1
        st.session_state.historico.append({
            'data': datetime.now().strftime("%d/%m %H:%M"),
            'nicho': nicho,
            'duracao': duracao,
            'roteiro': roteiro
        })
        
        st.success("✅ Roteiro criado!")
        st.markdown("### 📝 SEU ROTEIRO:")
        st.markdown(roteiro)
        
        col_x, col_y = st.columns(2)
        with col_x:
            st.download_button("📥 Baixar", roteiro, 
                             f"roteiro_{duracao}s.txt", "text/plain")
        with col_y:
            if st.button("🔄 Nova Variação"):
                st.rerun()

if st.session_state.historico:
    with st.expander("📚 Histórico"):
        for i, item in enumerate(reversed(st.session_state.historico[-5:])):
            st.markdown(f"**{i+1}.** {item['data']} - {item['nicho']} ({item['duracao']}s)")

st.markdown("---")
st.caption("🔒 Seguro | Powered by Claude AI")
