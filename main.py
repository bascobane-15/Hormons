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
    🩻 BioTwin-Systems
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
    st.markdown('<h3 class="discovery-title">Keşfe Nereden Başlayacaksın?</h3>', unsafe_allow_html=True)
    
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
elif menu == "🎯Hormonlar":
    
    st.title("🎯Hormonların Yolculuğu")
 
    st.write("""
    "Her hormonun bir görevi, her görevin bir hedefi vardır." 
    "Bu bölümde hormonların nerede üretildiğini, "
    "hangi organları etkilediğini"
    "ve vücudumuzun kusursuz iletişim sistemini nasıl yönettiklerini keşfedeceksiniz."
    """)
   
    st.markdown("<br><br>", unsafe_allow_html=True)   # Boşluğu artırır

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        st.video("endokrinbez.mp4")
    st.divider()
    st.subheader("Endokrin Bezler ve Hormonları")

    st.write("""
    Hormonlar Nasıl Çalışır?  
    """)
    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        st.video("https://youtu.be/Tn3c6wgNjB8?si=IOsnZpxByqttMYAm")

    st.divider()

    st.write("""
        "💡 Hormonlar sinir sistemiyle birlikte çalışarak vücudun iç dengesini (homeostazı) korur. "
         "Bu bölümde her hormonun görevini, salgılandığı bezi ve etkilediği organları keşfedeceksiniz."
     """)
    st.divider()

    # 🤖 BioTwin Dijital İkiz Simülasyonu

    st.subheader("🤖 BioTwin Dijital İkiz Simülasyonu")

    st.write("""
        "Günlük yaşamda vücudumuzda gerçekleşen hormonal değişimleri "
        "BioTwin modeli ile keşfedin."
     """)


    senaryo = st.selectbox(
        "🎯 Bir günlük yaşam senaryosu seçin:",
        [
            "🍔 Yemek yedim",
            "😨 Sınava girdim",
            "🏃 Egzersiz yaptım",
            "😴 Uyandım"
        ]
    )


    if st.button("🚀 BioTwin Analizini Başlat"):

        durum = st.empty()


        if senaryo == "🍔 Yemek yedim":

            durum.write("""
            "📡 Kan şekeri analiz ediliyor..."
            """)
            time.sleep(3)

            durum.write("""
            "🍬 Pankreas insülin salgılıyor..."
            """)
            time.sleep(3)

            durum.write("""
            "🧬 Hücreler glikoz almaya başladı..."
            """)
            time.sleep(3)

            durum.markdown("""
            <div style="
                background-color:#d9f2ff;
                padding:15px;
                border-radius:10px;
                border-left:8px solid #0077b6;
                color:#003049;
                font-size:18px;
                font-weight:bold;">
                🧬 Homeostazi sağlandı — Vücut dengesi korundu
            </div>
            """, unsafe_allow_html=True)


        elif senaryo == "😨 Sınava girdim":

            durum.write("""
            "📡 Stres seviyesi ölçülüyor..."
            """)
            time.sleep(3)

            durum.write("""
            "🔺 Böbreküstü bezleri kortizol salgılıyor..."
            """)
            time.sleep(3)

            durum.write("""
            "⚡ Vücut enerji hazırlıyor..."
            """)
            time.sleep(3)
            durum.markdown("""
            <div style="
                background-color:#d9f2ff;
                padding:15px;
                border-radius:10px;
                border-left:8px solid #0077b6;
                color:#003049;
                font-size:18px;
                font-weight:bold;">
                🧬 Homeostazi sağlandı — Stres yanıtı aktif
            
            </div>
            """, unsafe_allow_html=True)"


        elif senaryo == "🏃 Egzersiz yaptım":

            durum.write("""
            "📡 Enerji ihtiyacı hesaplanıyor..."
            """)
            time.sleep(3)

            durum.write("""
            "🧬 Glukagon devreye giriyor..."
            """)
            time.sleep(3)

            durum.write("""
            "💪 Kaslara enerji gönderiliyor..."
            """)
            time.sleep(3)

            durum.markdown("""
            <div style="
                background-color:#d9f2ff;
                padding:15px;
                border-radius:10px;
                border-left:8px solid #0077b6;
                color:#003049;
                font-size:18px;
                font-weight:bold;">
                🧬 Homeostazi sağlandı — Enerji dengesi kuruldu
            
            </div>
            """, unsafe_allow_html=True)"

        elif senaryo == "😴 Uyandım":

            durum.write("""
            "🌅 Biyolojik saat analiz ediliyor..."
            """)
            time.sleep(3)

            durum.write("""
            "🔺 Kortizol seviyesi yükseliyor..."
            """)
            time.sleep(3)

            durum.write("""
            "🧠 Vücut güne hazırlanıyor..."
            """)
            time.sleep(3)

            durum.markdown("""
            <div style="
                background-color:#d9f2ff;
                padding:15px;
                border-radius:10px;
                border-left:8px solid #0077b6;
                color:#003049;
                font-size:18px;
                font-weight:bold;">
                🧬 Homeostazi sağlandı — Vücut dengesi korundu
            </div>
            """, unsafe_allow_html=True) 
# ------------------------------------------------
# KORTİZOL SEKME
# ------------------------------------------------
elif menu == "🟠 Kortizol":
    st.title("🧬 Kortizol Hormonu")

    st.write("""
       "Kortizol, böbreküstü bezleri tarafından üretilen ve vücudun stres durumlarına "
       "uyum sağlamasına yardımcı olan önemli bir hormondur. 'Stres hormonu' olarak da bilinir. "
       "Enerji dengesini düzenler, kan şekerinin kontrolüne katkı sağlar ve bağışıklık sistemi "
       "yanıtını etkiler."   
   """)
   
    st.markdown("""
   ### 📌 Temel Bilgiler
   
   **🏥 Salgılandığı bez:** Böbreküstü bezleri  
   
   **⚡ Temel görevi:**  
   Stres anlarında vücudu harekete geçirmek, enerji kullanımını düzenlemek 
   ve iç dengenin (homeostaz) korunmasına yardımcı olmak.
   
   **🧠 Etkilediği sistemler:**  
   - Metabolizma  
   - Bağışıklık sistemi  
   - Stres yanıtı  
   
   💡 **Günün Notu:**  
   Kortizol seviyeleri sabah saatlerinde doğal olarak daha yüksektir. 
   Bu durum vücudun uyanmasına, enerji sağlamasına ve güne hazırlanmasına yardımcı olur.
   """)
    st.subheader(" 📌 Kortizol: Stres ve Sistemik Etkiler")
    
    # 1. GİRDİ ALANI
    stress = st.slider("Stres Düzeyi (Psikolojik/Fiziksel)", 0, 100, 50)
    
    # Matematiksel Hesaplama
    kortizol_seviyesi = stress * 1.15
    
    # 2. GÖRSEL GÖSTERGE (Gauge)
    import plotly.graph_objects as go
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = kortizol_seviyesi,
        title = {'text': "Kortizol Konsantrasyonu"},
        gauge = {
            'axis': {'range': [None, 120]},
            'bar': {'color': "darkred"},
            'steps' : [
                {'range': [0, 40], 'color': "#d9f2d9"},
                {'range': [40, 80], 'color': "#ffebcc"},
                {'range': [80, 120], 'color': "#ffcccc"}],
            'threshold': {'line': {'color': "black", 'width': 4}, 'value': 100}}))
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # 3. AKADEMİK BİLGİ ALANI (Ders Materyali Bölümü)
    st.subheader("📚 Klinik Bilgi Paneli: Kortizol Artışının Etkileri")
    
    col_info1, col_info2 = st.columns(2)

    with col_info1:
        st.markdown("""
        **1. Metabolik Etkiler:**
        * **Glukoneojenez:** Karaciğerde glikoz üretimini artırarak kan şekerini yükseltir.
        * **Protein Katabolizması:** Kas dokusunda protein yıkımına neden olur (kas zayıflığı).
        * **Lipoliz:** Yağların parçalanıp kanda serbest yağ asitlerinin artmasına yol açar.
        
        **2. Bağışıklık Sistemi:**
        * **İmmünsupresyon:** Lökosit aktivitesini baskılayarak bağışıklığı zayıflatır.
        * **Anti-inflamatuar:** Enflamasyonu (yangıyı) azaltır (Bu yüzden ilaç olarak kullanılır).
        """)

    with col_info2:
        st.markdown("""
        **3. Kardiyovasküler Etkiler:**
        * **Hipertansiyon:** Kan damarlarının adrenalin gibi maddelere duyarlılığını artırarak tansiyonu yükseltir.
        
        **4. Uzun Vadeli (Kronik) Sonuçlar:**
        * **Cushing Sendromu:** Kronik yüksek kortizol sonucu oluşan klinik tablo.
        * **Obezite:** Özellikle gövde ve yüz bölgesinde (ay dede yüzü) yağlanma.
        * **Osteoporoz:** Kemik yapımını azaltıp yıkımını hızlandırır.
        """)

    # 4. DİNAMİK ÖĞRENCİ NOTU
    if stress > 80:
        st.info("💡 **Eğitim Notu:** Şu anki yüksek değerler, vücudun 'Savaş veya Kaç' (Fight or Flight) modunda takılı kaldığını simüle ediyor. Bu durumda protein yıkımı (kas erimesi) maksimumdadır.")
       
    st.divider()
    st.caption("BioTwin-Systems | Eğitim Amaçlı Dijital İkiz Modeli")
# ------------------------------------------------
# İNSÜLİN SEKME
# ------------------------------------------------
elif menu == "🔵 İnsülin":
    st.subheader("🍬 İnsülin ve Glukagon Hormonları")

    st.write("""
          "İnsülin ve glukagon, pankreas tarafından salgılanan ve kandaki glikoz (şeker) "
          "düzeyini dengeleyen birbirine zıt görevli iki önemli hormondur."
     """)
      
    st.markdown("""
      ### 📌 İnsülin Hormonu
      
      **🏥 Salgılandığı yer:** Pankreas (Langerhans adacıkları - Beta hücreleri)  
      
      **⚡ Temel görevi:**  
      Kandaki glikoz miktarı yükseldiğinde hücrelerin glikozu almasını sağlar ve 
      kan şekerinin düşmesine yardımcı olur.
      
      **🧬 Etkilediği süreçler:**  
      - Glikozun hücrelere taşınması  
      - Enerji üretimi  
      - Glikojen depolanması  
           
      ---
      ### 📌 Glukagon Hormonu
      
      **🏥 Salgılandığı yer:** Pankreas (Langerhans adacıkları - Alfa hücreleri)  
      
      **⚡ Temel görevi:**  
      Kan şekeri düştüğünde depolanan glikojenin parçalanmasını sağlayarak 
      kandaki glikoz seviyesini yükseltir.
      
      **🧬 Etkilediği süreçler:**  
      - Glikojen yıkımı  
      - Kan şekeri düzenlenmesi  
      - Enerji dengesi  
      
      
      💡 **Günün Notu:**  
      İnsülin ve glukagon birlikte çalışarak kandaki şeker seviyesini dengede tutar 
      ve vücudun enerji ihtiyacını karşılamasına yardımcı olur.
      """)
    st.header("İnsülin ve Glukagon: Kan Şekeri Homeostazı")
    
    # 1. GİRDİ ALANI: Kan Glikoz Düzeyi
    # Tıbbi olarak normal açlık şekeri 70-100 mg/dL arasıdır.
    glikoz = st.slider("Kan Glikoz Seviyesi (mg/dL)", 40, 200, 90)
    
    # 2. HESAPLAMA MANTIĞI (Antagonist Model)
    # Glikoz arttıkça İnsülin artar, Glukagon azalır.
    insulin = max(0.0, (glikoz - 70) * 1.5) if glikoz > 70 else 0
    glukagon = max(0.0, (110 - glikoz) * 1.5) if glikoz < 110 else 0

    # 3. GÖRSELLEŞTİRME: Karşılaştırmalı Bar Grafik
    import plotly.graph_objects as go
    fig_kan_sekeri = go.Figure()
    fig_kan_sekeri.add_trace(go.Bar(
        x=['İnsülin (Anabolik)', 'Glukagon (Katabolik)'],
        y=[insulin, glukagon],
        marker_color=['#1f77b4', '#d62728'], # Mavi ve Kırmızı
        text=[f"Seviye: {insulin:.1f}", f"Seviye: {glukagon:.1f}"],
        textposition='auto'
    ))
    fig_kan_sekeri.update_layout(title="Hormonların Glikoz Seviyesine Yanıtı", yaxis_range=[0, 150])
    st.plotly_chart(fig_kan_sekeri, use_container_width=True)

    st.divider()

    # 4. AKADEMİK BİLGİ ALANI (Ders Materyali)
    st.subheader("📚 Klinik Bilgi Paneli: Glikoz Regülasyonu")
    
    col_ins1, col_ins2 = st.columns(2)

    with col_ins1:
        st.markdown("""
        **🔵 İnsülin (Beta Hücreleri):**
        * **Görevi:** Kan şekerini düşürmek.
        * **Mekanizma:** Glikozun hücre içine girişini sağlar (GLUT4 kapılarını açar).
        * **Depolama:** Glikozun fazlasını karaciğer ve kasta **Glikojen** olarak depolar.
        * **Sentez:** Protein ve yağ sentezini uyarır (Anabolik hormon).
        """)

    with col_ins2:
        st.markdown("""
        **🔴 Glukagon (Alfa Hücreleri):**
        * **Görevi:** Kan şekerini yükseltmek.
        * **Mekanizma:** Karaciğerdeki glikojenin parçalanmasını sağlar (**Glikojenoliz**).
        * **Üretim:** Karbonhidrat olmayan kaynaklardan (protein/yağ) glikoz üretir (**Glukoneojenez**).
        * **Yıkım:** Enerji açığı durumunda devreye girer (Katabolik hormon).
        """)

    # 5. KLİNİK DURUM ÖZETİ
    if glikoz > 140:
        st.error(f"⚠️ **Hiperglisemi:** Kan şekeri yüksek ({glikoz} mg/dL). İnsülin salgısı maksimumda, glikoz hücrelere taşınmaya çalışılıyor.")
    elif glikoz < 70:
        st.warning(f"⚠️ **Hipoglisemi:** Kan şekeri düşük ({glikoz} mg/dL). Glukagon devreye girerek karaciğerden kana şeker salınmasını uyarıyor.")
    else:
        st.success("✅ **Normoglisemi:** Kan şekeri ideal aralıkta. Homeostaz korunuyor.")
      
# ------------------------------------------------
# TİROKSİN SEKME
# ------------------------------------------------
elif menu == "🟣 Tiroksin":
    st.header("Tiroksin ve HPT Aksı: Negatif Feedback Mekanizması")
    
    # 1. GİRDİ ALANI: Tiroit Bezi Aktivitesi
    tiroit_aktivite = st.slider("Tiroit Bezi Çalışma Kapasitesi (%)", 0, 200, 100)
    
    # 2. FEEDBACK MANTIĞI (Dijital İkiz Hesaplaması)
    # Tiroksin (T4), tiroit bezinin aktivitesine bağlı üretilir.
    tiroksin = tiroit_aktivite * 0.5
    
    # Negatif Feedback: Tiroksin arttıkça Hipofiz'den salgılanan TSH azalır (Gaz-Fren ilişkisi).
    tsh = max(0.1, 100 - (tiroksin * 1.5))

    # 3. GÖRSEL METRİKLER
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.metric("Tiroksin (T4) Seviyesi", f"{tiroksin:.1f}", 
                  delta="Yüksek (Hiper)" if tiroksin > 65 else ("Düşük (Hipo)" if tiroksin < 35 else "Normal"))
    with col_t2:
        st.metric("TSH (Hipofiz Yanıtı)", f"{tsh:.1f}", 
                  delta="Baskılanmış" if tsh < 20 else ("Uyarıcı" if tsh > 80 else "Dengeli"), 
                  delta_color="inverse")

    # 4. GÖRSELLEŞTİRME: Bar Grafik
    import plotly.graph_objects as go
    fig_tiroit = go.Figure()
    fig_tiroit.add_trace(go.Bar(
        x=['TSH (Hipofiz Uyarıcı)', 'Tiroksin (Tiroit Yanıtı)'],
        y=[tsh, tiroksin],
        marker_color=['#9b59b6', '#3498db'], # Mor ve Mavi
        text=[f"TSH: {tsh:.1f}", f"T4: {tiroksin:.1f}"],
        textposition='auto'
    ))
    fig_tiroit.update_layout(title="HPT Aksı: Dinamik Geri Bildirim Dengesi", yaxis_range=[0, 150])
    st.plotly_chart(fig_tiroit, use_container_width=True)

    st.divider()
    
    # 5. AKADEMİK BİLGİ ALANI (Ders Materyali)
    st.subheader("📚 Klinik Bilgi Paneli: Tiroit Fizyopatolojisi")
    
    st.write("""
           "💡 **Negatif Feedback Mekanizması:** Kanda Tiroksin (T4) yükseldiğinde, Hipofiz bezi bunu algılar ve tiroit bezini daha fazla uyarmamak için TSH salgısını azaltır. Bu bir öz-denetim sistemidir.
    """)
    col_symp1, col_symp2 = st.columns(2)

    with col_symp1:
        st.error("🔥 Hipertiroidi (Zehirli Guatr)")
        st.markdown("""
        **Kanda T4 Yüksek, TSH Düşüktür.**
        * **Metabolizma:** Aşırı hızlanır, bazal enerji tüketimi artar.
        * **Kardiyovasküler:** Çarpıntı (Taşikardi) ve yüksek tansiyon.
        * **Sinir Sistemi:** Titreme (tremor), huzursuzluk ve uykusuzluk.
        * **Fiziksel:** Sıcağa tahammülsüzlük, aşırı terleme ve hızlı kilo kaybı.
        """)

    with col_symp2:
        st.warning("❄️ Hipotiroidi")
        st.markdown("""
        **Kanda T4 Düşük, TSH Yüksektir.**
        * **Metabolizma:** Yavaşlar, vücut ısısı düşer.
        * **Kilo:** İştahsızlığa rağmen kilo alma ve vücutta ödem.
        * **Zihinsel:** Unutkanlık, yavaş düşünme ve depresyon eğilimi.
        * **Fiziksel:** Soğuğa tahammülsüzlük, halsizlik ve cilt kuruluğu.
        """)

    # 6. ÖĞRENCİLER İÇİN ÖZET
    st.subheader("""
    **HPT Aksı Akış Şeması:
    **Hipotalamus (TRH) ➡️ Ön Hipofiz (TSH) ➡️ Tiroit Bezi (T4) ➡️ Hedef Dokular.
    """)
    
# ------------------------------------------------
# PARATHORMON – KALSİTONİN SEKME
# ------------------------------------------------

elif menu == "🟢 Parathormon–Kalsitonin":
    st.header("🦴 Parathormon ve Kalsitonin")

    st.write("""
       "Parathormon ve kalsitonin, kandaki kalsiyum düzeyini düzenleyen iki önemli "
       "hormondur. Birlikte çalışarak kemiklerin güçlenmesine ve sinir-kas sisteminin "
       "sağlıklı çalışmasına katkı sağlar."
    """)
   
    st.markdown("""
    ### 📌 Parathormon (PTH)
   
    **🏥 Salgılandığı bez:** Paratiroit bezleri
   
    **⚡ Temel görevi:**  
    Kan kalsiyum seviyesi düştüğünde kemiklerden kalsiyum salınımını artırır, böbreklerden kalsiyum geri emilimini destekler ve böylece kan kalsiyum düzeyini yükseltir.
   
    ---
   
    ### 📌 Kalsitonin
   
    **🏥 Salgılandığı bez:** Tiroit bezi (C hücreleri)
   
    **⚡ Temel görevi:**  
    Kan kalsiyum seviyesi yükseldiğinde kalsiyumun kemiklerde depolanmasını destekleyerek kan kalsiyum düzeyinin düşmesine yardımcı olur.
   
   ---
   
    ### 🧬 Birlikte Nasıl Çalışırlar?
   
    - 🟢 **Parathormon:** Kan kalsiyumunu **artırır.**
    - 🔵 **Kalsitonin:** Kan kalsiyumunu **azaltır.**
   
   💡 **Günün Notu:**  
    Parathormon ve kalsitonin birbirine zıt etki gösteren hormonlardır. Bu sayede kandaki kalsiyum seviyesi belirli sınırlar içinde tutularak kemik, kas ve sinir sisteminin sağlıklı çalışması sağlanır.
    """)
    st.header("Parathormon – Kalsitonin (Kalsiyum Dengesi)")

    st.markdown("""
    Parathormon (PTH) ve kalsitonin hormonları **antagonist** etki göstererek
    kandaki kalsiyum düzeyinin düzenlenmesini sağlar.
    """)

   # FİZYOLOJİK GİRDİ (Kalsiyum değerini 8-12 arasına çektik, daha gerçekçi)
    calcium = st.slider("Kandaki Kalsiyum Düzeyi (mg/dL)", 8.0, 12.0, 10.0)

    # HORMON DÜZEYLERİ (Antagonist Model)
    # Kalsiyum düştükçe PTH tavan yapar, kalsiyum arttıkça PTH sıfıra yaklaşır.
    parathormon = max(0.0, (12.0 - calcium) * 25) 
    
    # Kalsiyum arttıkça Kalsitonin tavan yapar.
    kalsitonin = max(0.0, (calcium - 8.0) * 25)
   # HORMON DÜZEYLERİ (Yuvarlama eklendi)
    parathormon = round(max(0.0, (12.0 - calcium) * 25), 1) 
    kalsitonin = round(max(0.0, (calcium - 8.0) * 25), 1)

    # GÖSTERİM (Metriklerin içinde de formatlama yapıyoruz)
    col1, col2 = st.columns(2)
    col1.metric("Parathormon (PTH)", f"{parathormon}")
    col2.metric("Kalsitonin", f"{kalsitonin}")

    # ANTİAGONİST HORMON GRAFİĞİ
   # PLOTLY İLE ETKİLEŞİMLİ GRAFİK
    import plotly.graph_objects as go

    fig = go.Figure()

    # Parathormon Çubuğu
    fig.add_trace(go.Bar(
        x=['Parathormon (PTH)', 'Kalsitonin'],
        y=[parathormon, kalsitonin],
        marker_color=['#FFA500', '#00CED1'], # Turuncu ve Turkuaz renkler
        text=[f"%{parathormon:.1f}", f"%{kalsitonin:.1f}"],
        textposition='auto',
    ))

    fig.update_layout(
        title_text='Hormonların Dinamik Dengesi',
        yaxis_range=[0, 100],
        template='plotly_white',
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

    # FİZYOLOJİK VE KLİNİK YORUM
    if parathormon > kalsitonin:
        st.warning("""
        ⚠️ **Parathormon Baskın**
        - Kemiklerden kana kalsiyum geçişi artar  
        - Kemik mineral yoğunluğu azalabilir  

        **İlişkili Durum:**  
        - Osteoporoz riski
        """)
    elif kalsitonin > parathormon:
        st.success("""
        ✅ **Kalsitonin Baskın**
        - Kalsiyum kemiklerde tutulur  
        - Kemik yapısı korunur
        """)
    else:
        st.write("""
        ℹ️ Kalsiyum dengede → İskelet sisteminde homeostazi sağlanıyor"
        """)
    # 5. AKADEMİK BİLGİ ALANI 
    st.subheader("📚 Klinik Bilgi Paneli")
    
    st.write("""
   
   🔹 **Parathormonun yetersiz salgılanması (Hipoparatiroidizm):**
   Kandaki kalsiyum düzeyi düşer. Kas krampları, kasılmalar, karıncalanma ve nöbetler görülebilir.
   
   🔹 **Parathormonun fazla salgılanması (Hiperparatiroidizm):**
   Kan kalsiyum düzeyi yükselir. Kemiklerde zayıflama, böbrek taşı, kas güçsüzlüğü ve yorgunluk gelişebilir.
   
   🔹 **Kalsitonin:**
   İnsanlarda kalsiyum dengesindeki etkisi parathormona göre daha sınırlıdır. Ancak yüksek düzeyleri bazı tiroit hastalıklarının değerlendirilmesinde klinik belirteç olarak kullanılabilir.
   
   ⚠️ **Unutmayın:** Parathormon ve kalsitonin birlikte çalışarak kandaki kalsiyum seviyesini dengeler. Bu denge; kemik sağlığı, kasların kasılması ve sinir iletimi için büyük önem taşır.
   """)

st.divider()
st.caption("BioTwin-Systems | Eğitim Amaçlı Dijital İkiz Modeli")
















































