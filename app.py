import streamlit as st
import pandas as pd

# Nastavení stránky
st.set_page_config(page_title="Katalog Škoda Fabia", layout="wide")

@st.cache_data
def load_data():
    # Načtení dat (soubor musí být ve stejné složce)
    df = pd.read_excel("Py_F_data.xlsx")
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()

    # --- FILTRY (Pořadí: Generace -> Karoserie -> Motor) ---
    st.sidebar.header("🔍 Výběr vozu")
    
    # 1. Výběr generace
    seznam_gen = sorted(df['generace'].unique())
    v_gen = st.sidebar.selectbox("1. Vyberte generaci:", seznam_gen)
    
    # 2. Výběr karoserie (jen ty, které jsou v dané generaci)
    maska_gen = df['generace'] == v_gen
    seznam_kar = df[maska_gen]['karoserie'].unique().tolist()
    # Seřadíme podle tvého přání: Hatchback, Combi, Sedan (pokud existují)
    poradi = ["Hatchback", "Combi", "Sedan"]
    seznam_kar = sorted(seznam_kar, key=lambda x: poradi.index(x) if x in poradi else 99)
    v_kar = st.sidebar.selectbox("2. Vyberte karoserii:", seznam_kar)
    
    # 3. Výběr motoru
    maska_kar = (df['generace'] == v_gen) & (df['karoserie'] == v_kar)
    seznam_mot = df[maska_kar]['Motor'].unique().tolist()
    v_mot = st.sidebar.selectbox("3. Vyberte motorizaci:", seznam_mot)

    # Získání dat vybraného auta
    auto = df[maska_kar & (df['Motor'] == v_mot)].iloc[0]

    # --- ZOBRAZENÍ ---
    st.title(f"Škoda Fabia {v_gen} {v_kar}")
    st.subheader(f"Motor: {v_mot}")
    st.write(f"📅 **Rok výroby / Modelový rok:** {auto.get('Rok', '-')}")
    st.markdown("---")

    # Rozdělení do skupin pomocí sloupců
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("⚙️ Motor a pohon")
        st.write(f"**Objem:** {auto.get('Objem [l]', '-')} l")
        st.write(f"**Výkon:** {auto.get('Výkon [kW]', '-')} kW")
        st.write(f"**Točivý moment:** {auto.get('Točivý moment [Nm]', '-')} Nm")
        st.write(f"**Zdvihový objem:** {auto.get('Zdvihový objem v [cm³]', '-')} cm³")
        st.write(f"**Počet válců:** {auto.get('Počet válců', '-')}")
        st.write(f"**Typ:** {auto.get('Typ', '-')}")
        st.write(f"**Pohon:** {auto.get('Pohon', '-')}")
        st.write(f"**Převodovka:** {auto.get('Převodovka', '-')}")
        st.write(f"**Spojka:** {auto.get('Spojka', '-')}")

        st.subheader("🏁 Rychlost a dynamika")
        st.write(f"**Nejvyšší rychlost:** {auto.get('Nejvyšší rychlost [km/h]', '-')} km/h")
        st.write(f"**Zrychlení 0-100 km/h:** {auto.get('Zrychlení 0 - 100 km/h', '-')} s")

    with col2:
        st.subheader("⛽ Palivo a emise")
        st.write(f"**Typ paliva:** {auto.get('Typ paliva', '-')}")
        st.write(f"**Kombinovaná spotřeba:** {auto.get('Kombinovaná spotřeba paliva [l/100 km]', '-')} l/100 km")
        st.write(f"**Emisní hodnoty CO2:** {auto.get('Emisní hodnoty CO2 [g/km]', '-')} g/km")
        st.write(f"**Exhalační norma:** {auto.get('Exhalační norma', '-')}")

        st.subheader("⚖️ Hmotnosti")
        st.write(f"**Celková hmotnost:** {auto.get('Celková hmotnost [kg]', '-')} kg")
        st.write(f"**Pohotovostní hmotnost:** {auto.get('Pohotovostní hmotnost [kg]', '-')} kg")

        st.subheader("📦 Objemy")
        st.write(f"**Zavazadlový prostor:** {auto.get('Objem zavazadlového prostoru [l]', '-')} l")
        st.write(f"**Palivová nádrž:** {auto.get('Objem palivové nádrže [l]', '-')} l")

    st.markdown("---")
    st.subheader("💰 Dostupná výbava a dobové ceny")
    
    # Definujeme, co jsou technické parametry (ty už jsme vypsali výše)
    technika = [
        'Motor', 'generace', 'karoserie', 'Objem [l]', 'Výkon [kW]', 'Točivý moment [Nm]',
        'Zdvihový objem v [cm³]', 'Počet válců', 'Typ', 'Pohon', 'Převodovka', 'Spojka',
        'Nejvyšší rychlost [km/h]', 'Zrychlení 0 - 100 km/h', 'Typ paliva',
        'Kombinovaná spotřeba paliva [l/100 km]', 'Emisní hodnoty CO2 [g/km]',
        'Exhalační norma', 'Celková hmotnost [kg]', 'Pohotovostní hmotnost [kg]',
        'Objem zavazadlového prostoru [l]', 'Objem palivové nádrže [l]', 'Rok'
    ]
    
    # Najdeme všechny ostatní sloupce (výbavy) a vypíšeme jen ty s cenou
    vsechny_sloupce = df.columns.tolist()
    vybavy = [col for col in vsechny_sloupce if col not in technika]
    
    nalezena_cena = False
    col_v1, col_v2, col_v3 = st.columns(3)
    index = 0
    
    for v in vybavy:
        cena = auto.get(v)
        # Podmínka: Vypiš jen pokud tam není nula, prázdno nebo pomlčka
        if pd.notna(cena) and str(cena).strip() not in ["0", "0.0", "-", ""]:
            nalezena_cena = True
            # Rozdělíme výpis do 3 sloupců pro úsporu místa
            target_col = [col_v1, col_v2, col_v3][index % 3]
            target_col.write(f"✅ **{v}:** {cena} Kč")
            index += 1
            
    if not nalezena_cena:
        st.info("Pro tuto motorizaci nejsou v databázi k dispozici žádné ceny výbav.")

except Exception as e:
    st.error(f"Chyba při zpracování dat: {e}")
# --- PATIČKA ---
st.sidebar.markdown("---")
st.sidebar.caption(f"""
**Právní doložka a prohlášení:** Tento web je neoficiální projekt vytvořený výhradně pro účely maturitní práce a edukaci v oblasti analýzy dat. Projekt je vytvořen v souladu s § 35 odst. 3 zákona č. 121/2000 Sb. (Autorský zákon) o užití školního díla pro potřeby školy a pro účely výuky.

1. **Zdroje dat:** Veškeré technické parametry a dobové ceny byly čerpány z veřejně dostupných archivů a oficiálních materiálů Škoda Auto.  
2. **Aktualita:** Data mají informativní charakter a mohou se lišit od reálných historických nabídek. Autor neručí za případné chyby v datech.  
3. **Autorská práva:** Užití ochranných známek slouží výhradně k identifikaci produktů a nepředstavuje spojení s držitelem práv. Ochranná známka Škoda a názvy modelů jsou majetkem společnosti Škoda Auto a.s.  
4. **Neziskovost:** Projekt není využíván ke komerčním účelům ani k žádné formě výdělku.

**Autor:** Vojtěch Hendrych  
**Škola:** SPŠ strojnická, Betlémská 287/4, Praha 1  
**Školní rok:** 2025/2026
""")
