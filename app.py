import streamlit as st
import time
import pandas as pd

# Impostazioni della pagina
st.set_page_config(page_title="AI Quoting Engine - Packaging Service", page_icon="📦", layout="wide")

# Intestazione personalizzata
st.title("📦 Packaging Service Srl - AI Quoting Engine 5.0")
st.markdown("---")

# Area di Input
st.subheader("📩 1. Acquisizione Richiesta Cliente")
email_cliente = st.text_area(
    "Testo dell'email in arrivo:", 
    height=150, 
    value="Buongiorno, ci servirebbero urgentemente 10 imballaggi. Ogni set deve essere composto da una base in Polycell bianco spessore 90mm (circa 550x170) per ammortizzare il prodotto, e la copertura superiore spessore 60mm (circa 270x100). Forniteci anche il pallet economico a 2 vie e le viti 5x60 (ne servono 4 per imballo). Attendo preventivo. Saluti, Mario."
)

# Bottone Magico
if st.button("🤖 Elabora Preventivo AI", type="primary", use_container_width=True):
    
    # --- EFFETTO ELABORAZIONE WOW ---
    with st.status("Inizializzazione Intelligenza Artificiale...", expanded=True) as status:
        st.write("🧠 Lettura e analisi semantica dell'email...")
        time.sleep(1.5)
        st.write("🔍 Estrazione quote e ricerca codici materiali in ERP (Distinta Base)...")
        time.sleep(1.5)
        st.write("⚙️ Calcolo dei tempi macchina CNC e costo operatore...")
        time.sleep(1.5)
        st.write("📈 Applicazione margine commerciale aziendale (40%)...")
        time.sleep(1)
        st.write("✍️ Generazione proposta commerciale in corso...")
        time.sleep(1.5)
        status.update(label="Preventivo Generato con Successo!", state="complete", expanded=False)
    
    st.markdown("---")
    
    # --- DASHBOARD RISULTATI ---
    st.subheader("📊 2. Cruscotto Economico (Vista Interna)")
    
    # Metriche
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Costo di Produzione", value="€ 147,20")
    col2.metric(label="Margine Netto (40%)", value="€ 58,88")
    col3.metric(label="Prezzo di Vendita Finale", value="€ 206,08", delta="Ottimizzato", delta_color="normal")
    
    st.write(" ")
    
    # Tabella Distinta Base
    st.markdown("**Dettaglio Distinta Base (BOM) calcolato dall'AI:**")
    dati_bom = {
        "Codice ERP":["A_BASE", "I_SUP", "Bancale 2 vie", "Viti 5x60", "Assemblaggio"],
        "Descrizione Materiale":["Polycell bianco 90mm", "Polycell bianco 60mm", "Pallet in legno", "Ferramenta di fissaggio", "Manodopera standard"],
        "Qtà":[10, 10, 10, 40, 1],
        "Costo Unitario":["€ 1,84", "€ 0,50", "€ 10,00", "€ 0,27", "€ 13,00"],
        "Costo Totale":["€ 18,40", "€ 5,00", "€ 100,00", "€ 10,80", "€ 13,00"]
    }
    df = pd.DataFrame(dati_bom)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # --- EMAIL COMMERCIALE ---
    st.subheader("📧 3. Bozza Email Commerciale (Pronta per l'invio)")
    bozza_email = """Oggetto: Preventivo Packaging Service - Fornitura 10 set imballaggio su misura

Gentile Mario,

La ringraziamo per aver contattato Packaging Service Srl. Abbiamo analizzato la sua richiesta e siamo pronti a fornirle la soluzione di imballo perfetta per proteggere il suo prodotto.

Di seguito il preventivo per la realizzazione di N. 10 set completi, composti esattamente secondo le sue specifiche, utilizzando il nostro Polycell bianco ad alta densità.

Dettaglio fornitura per singolo set:
- N. 1 Base in Polycell bianco (spessore 90mm, dim. 559x170)
- N. 1 Copertura superiore in Polycell bianco (spessore 60mm, dim. 270x100)
- N. 1 Bancale a 2 vie
- N. 4 Viti 5x60 per il fissaggio
- Assemblaggio incluso

Quotazione Economica:
- Prezzo per singolo set completo: 20,60 € + IVA
- Totale per l'intero lotto (10 set): 206,08 € + IVA

I nostri materiali in EPE sono riciclabili al 100% e lavorati con macchinari CNC per garantirle una precisione millimetrica. 

Rimango in attesa di una Sua gradita conferma per procedere con la messa in produzione.

Cordiali saluti,
Ufficio Commerciale - Packaging Service Srl
"""
    st.text_area("Copia o modifica il testo prima di inviare:", value=bozza_email, height=400)
    
    st.success("Tutti i dati sono stati salvati correttamente nel CRM aziendale.")
