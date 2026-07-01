import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
import base64
import folium
import time
import random
from streamlit_folium import st_folium
import streamlit.components.v1 as components
# Sayfa Ayarları
st.set_page_config(page_title="Hormonlar", layout="wide")

# -------------------------
# CSS 
# -------------------------
st.markdown(""" 
<style> 
   /* Ana Arka Plan - Açık koyu gri */ 
      .stApp { 
         background-color: #343a40; 
         color: #ffffff; 
    }

    /* SOL TARAF (SIDEBAR) BEYAZ */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
    }

    /* Sidebar Marka Başlığı Stili */
.sidebar-brand-title {
    font-size: 1.5rem !important; /* Yazı boyutunu büyüttük */
    color: #000000 !important;    /* Tam siyah yaptık */
    font-weight: 800 !important;  /* Ekstra kalın yaptık */
    line-height: 1.2 !important;
    text-align: center;
    margin-top: 15px;
    margin-bottom: 20px;
    text-transform: uppercase;    /* Hepsini büyük harf yap */
    letter-spacing: 1px;          /* Harf arası boşluk ile modern görünüm */
}

    .card-icon { font-size: 3rem; margin-bottom: 15px; }
    
    /* Türk Bayrağı Özel İkon */
    .tr-flag-container {
        width: 60px;
        height: 40px;
        margin: 0 auto 15px auto; /* Ortalamak için */
        background-image: url('https://upload.wikimedia.org/wikipedia/commons/b/b4/Flag_of_Turkey.svg');
        background-size: cover;
        background-position: center;
        border-radius: 4px;
        box-shadow: 0 4px 10px rgba(227, 10, 23, 0.4);
     }

    .card-title { color: #3498db; font-weight: bold; font-size: 1.1rem; margin-bottom: 10px; }
    .card-text { font-size: 0.85rem; opacity: 0.8; line-height: 1.4; }
    
    /* Sol Alt Açıklama Kutusu (Siyah, Büyük ve Görünür) */
    .sidebar-footer {
        font-size: 1.1rem !important;
        color: #000000 !important;
        font-weight: 600 !important;
        text-align: center;
        padding: 15px;
        background-color: #f1f5f9;
        border-radius: 12px;
        margin-top: 20px;
        border: 2px solid #000000;
        line-height: 1.5;
    }

    /* GÜNÜN BİLGİSİ KUTUSU (Belirgin Siyah) */
    .fact-box {
        background: #ffffff !important;
        border-radius: 15px;
        padding: 25px 35px;
        border-left: 10px solid #000000 !important;
        margin-top: 50px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }

    .fact-box h4 {
        color: #000000 !important;
        font-size: 1.6rem !important;
        font-weight: 800 !important;
        margin-bottom: 5px !important;
    }

    .fact-box p {
        color: #1a1a1a !important;
        font-size: 1.2rem !important;
        line-height: 1.6;
    }

    /* Keşif Kartları */
    .explore-card {
       background: rgba(255, 255, 255, 0.05);
       border: 1px solid rgba(255, 255, 255, 0.1);
       border-radius: 20px;
       padding: 20px;
       text-align: center;
       
       /* DEĞİŞİKLİK BURADA: */
       height: 240px;            /* min-height yerine sabit height verdik */
       display: flex;            /* İçeriği dikeyde yaymak için */
       flex-direction: column;   /* İçindekileri alt alta diz */
       justify-content: center;  /* İçindekileri dikeyde ortala */
       align-items: center;      /* Yatayda ortala */
       
       transition: transform 0.3s;
   }

    .explore-card:hover {
       transform: translateY(-10px);
       background: rgba(255, 255, 255, 0.1);
       border-color: #a5f3fc;
   }

    /* Üstteki tanıtım metninin altındaki boşluğu siler */
    .stMarkdown p {
        margin-bottom: 5px !important;
    }

    /* "Keşfe Nereden Başlayacaksınız?" başlığının üst ve alt boşluğunu ayarlar */
    .discovery-title {
        margin-top: -10px !important;  /* Negatif değer yukarı çeker */
        margin-bottom: 20px !important;
        text-align: center;
    }
    /* Üstteki tanıtım yazılarının (paragraf) alt boşluğunu tamamen kaldırır */
    .stMarkdown div p {
        margin-bottom: 0px !important;
        padding-bottom: 0px !important;
    }
</style>
""", unsafe_allow_html=True)
# -------------------------
# SIDEBAR İÇERİĞİ (SOL TARAF)
# -------------------------
with st.sidebar:

    with open("anatomy.mp4", "rb") as f:
        video_bytes = f.read()
        video_base64 = base64.b64encode(video_bytes).decode()

    st.markdown(f"""
<video width="100%" autoplay loop muted playsinline>
    <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
</video>
""", unsafe_allow_html=True)
    
    menu = st.selectbox(
        "📍 Sayfanızı Seçin",
         ["Ana Sayfa", "🎯Hormonlar","🟠 Kortizol","🔵 İnsülin", "🟣 Tiroksin","🟢 Parathormon–Kalsitonin"]
    )

    st.markdown("---")
    # 4. Sol Alt Açıklama Metni (Siyah ve Büyük Stil)
    st.markdown("""
        <div class="sidebar-footer">
            Bu platform, insan fizyolojisini dijital dünyada modellemek amacıyla başlatılan **BioTwin-Systems** serisinin ilk modülüdür. Şu an yayında olan **Endokrin Sistem** modülüdür. 
    
    **Gelecek Planları:**
    * 🫀 Dolaşım ve Solunum Sistemi Simülasyonları
           
    Çalışmamız, eğitimde dijital ikiz kullanımını yaygınlaştırmak için geliştirilmeye devam etmektedir.
    </div>
    """, unsafe_allow_html=True)
# -------------------------
# SAĞ TARAF (ANA SAYFA) İÇERİĞİ
# -------------------------
if menu == "Ana Sayfa":

    # GLOBAL FONT AYARI
    st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    }

    .hero-title{
        font-size:3.4rem;
        font-weight:800;
        color:white;
        margin-bottom:10px;
        letter-spacing:0.5px;
    }

    .hero-subtitle{
        font-size:1.8rem;
        color:#cbd5e1;
        margin-bottom:30px;
        font-weight:500;
    }

    .hero-text{
        font-size:1.15rem;
        color:#e2e8f0;
        max-width:900px;
        margin:auto;
        line-height:1.7;
    }
    </style>
    """, unsafe_allow_html=True)

    # HERO BÖLÜMÜ
    st.markdown("""
    <div style="text-align:center; padding:60px 0;">
    
    <div class="hero-title">
    🧠BioTwin-Systems
    </div>

    <div class="hero-subtitle">
    Endokrin Sistem Dijital İkizi
    </div>

    <div class="hero-text">
    Hormon sentezi, geri bildirim mekanizmaları ile hormon azlığı veya fazlalığının yol açtığı klinik tabloları modelleyen dinamik simülasyon platformu.
    </div>

    </div>
    """, unsafe_allow_html=True)

    # 3. İNTERAKTİF KEŞİF KARTLARI
    st.markdown('<h3 class="discovery-title">Keşfe Hangi Hormonla Başlayacaksın?</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("""
            <div class="explore-card">
                <div class="card-icon">🎯</div>
                <div class="card-title">Hormonlar</div>
                <p style="font-size: 0.9rem;">Hormonlar Nasıl Çalışır? Keşfet.</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="explore-card">
                <div class="card-icon">🟠</div>
                <div class="card-title">Kortizol</div>
                <p style="font-size: 0.9rem;">Stres anlarında vücudunu yöneten görünmez kahramanı keşfet.</p>
            </div>
        """, unsafe_allow_html=True)    
    with col3:
        st.markdown("""
            <div class="explore-card">
                <div class="card-icon">🔵</div>
                <div class="card-title">İnsülin</div>
                <p style="font-size: 0.9rem;">Kan şekerini dengede tutan hormonları keşfet.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown("""
            <div class="explore-card">
                <div class="card-icon">🟣</div>
                <div class="card-title">Tiroksin</div>
                <p style="font-size: 0.9rem;">Metabolizma hızını yöneten görünmez gücü keşfet.</p>
            </div>
        """, unsafe_allow_html=True)
        
          
         
    with col5:
        st.markdown("""
            <div class="explore-card">
                <div class="card-icon">🟢</div>
                <div class="card-title">Parathormon–Kalsitonin</div>
                <p style="font-size: 0.9rem;">Kalsiyum dengesini yöneten iki güçlü hormonu keşfet.</p>
            </div>
        """, unsafe_allow_html=True)

    
    # 4. GÜNÜN KELİMESİ (Sözlük Kutusu)
    kelimeler = [
    {
        "kelime": "hormon",
        "dil": "Türkçe",
        "anlam": "Vücuttaki hücreler arasında iletişimi sağlayan kimyasal habercilerdir."
    },
    {
        "kelime": "Endokrin sistem",
        "dil": "Türkçe",
        "anlam": "Hormonları üreten ve düzenleyen sistemdir."
    },
    {
        "kelime": "Hedef Organ",
        "dil": "Türkçe",
        "anlam": "Bir hormonun etkisini gösterdiği, üzerinde özel hormon alıcıları bulunan organ veya hücrelerdir."
    },
    {
        "kelime": "Homeostazi",
        "dil": "Türkçe",
        "anlam": "Vücudun iç dengesini (kan şekeri, sıcaklık, su dengesi gibi) koruma durumudur."
    },
    {
        "kelime": "Geri Bildirim",
        "dil": "Türkçe",
        "anlam": "Feedback, Hormon üretiminin vücudun ihtiyacına göre artırılıp azaltılmasını sağlayan kontrol mekanizmasıdır"
    },
]

    gunun_kelimesi = random.choice(kelimeler)


    st.markdown(f"""
        <div style="background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 15px; border-left: 5px solid #3498db; margin-top: 20px;">
            <b style="color: #3498db; font-size: 1.1rem;">🧠 Bilgi Notu: {gunun_kelimesi['kelime']}</b> 
            <span style="color: #a0a0a0; font-size: 0.9rem; margin-left: 5px;">({gunun_kelimesi['dil']})</span>
            <p style="margin-top: 10px; font-size: 1rem; line-height: 1.5;">{gunun_kelimesi['anlam']}</p>
        </div>
    """, unsafe_allow_html=True)
    
# -------------------------
