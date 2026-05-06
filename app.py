import streamlit as st
import time
import pandas as pd
import json
from openai import OpenAI

# Impostazioni pagina
st.set_page_config(page_title="AI Quoting Engine - Packaging Service", page_icon="📦", layout="wide")

# --- SIDEBAR PER LA API KEY ---
st.sidebar.title("Impostazioni AI ⚙️")
st.sidebar.markdown("Per motivi di sicurezza, inserisci la tua chiave API qui. Non verrà salvata nel server.")
api_key = st.sidebar.text_input("Inserisci OpenAI API Key", type="password")

st.title("📦 Packaging Service Srl - AI Quoting Engine Dinamico")
st.markdown("---")

# Area di Input
st.subheader("📩 1. Acquisizione Richiesta Cliente (Dinamica)")
email_cliente = st.text_area(
    "Scrivi o fai dettare al cliente un'email di prova modificando le quantità:", 
    height=150, 
    value="Buongiorno, ci servirebbero urgentemente 15 imballaggi completi. Ogni set deve avere la base in Polycell 90mm (A_BASE) e la copertura 60mm (I_SUP). Includete il bancale a 2 vie e le viti 5x60 (ne servono 4 per scatola). Grazie, Marco."
)

if st.button("🤖 Elabora Preventivo dal Vivo", type="primary", use_container_width=True):
    if not api_key:
        st.error("⚠️ Inserisci la tua API Key di OpenAI nella barra laterale a sinistra per procedere!")
    else:
        client = OpenAI(api_key=api_key)
        
        with st.status("Connessione al cervello AI in corso...", expanded=True) as status:
            st.write("🧠 Lettura e comprensione delle quantità richieste...")
            
            # IL VERO PROMPT CHE GUIDA L'AI
            prompt_sistema = """Sei il motore di preventivazione AI di Packaging Service Srl. 
            Hai accesso a questa Distinta Base (BOM):
            - A_BASE (Polycell bianco 90mm): 1.84 € / pezzo
            - I_SUP (Polycell bianco 60mm): 0.50 € / pezzo
            - Bancale 2 vie (brutti): 10.00 € / pezzo
            - Viti 5x60: 0.27 € / pezzo
            - Assemblaggio base: 13.00 € (costo fisso da aggiungere UNA SOLA VOLTA al totale del lotto)

            Il tuo compito:
            1. Trova nell'email quali di questi componenti servono e in che quantità (es. se servono 15 imballi e ogni imballo ha 4 viti, le viti sono 60).
            2. Calcola i costi totali esatti di produzione.
            3. Aggiungi il margine del 40% (Prezzo di vendita = Costo di produzione * 1.4).
            4. Genera una mail commerciale di risposta.
            5. RISPONDI ESATTAMENTE ED ESCLUSIVAMENTE IN FORMATO JSON con questa struttura:
            {
              "voci_preventivo":[
                {"codice": "A_BASE", "descrizione": "Polycell 90mm", "qta": 15, "costo_unitario": 1.84, "costo_totale": 27.60}
              ],
              "costo_assemblaggio": 13.00,
              "costo_produzione_totale": 0.00,
              "margine_netto": 0.00,
              "prezzo_vendita_finale": 0.00,
              "bozza_email": "Oggetto: Preventivo... \\n\\nGentile..."
            }"""

            try:
                # Chiamata vera alle API di OpenAI
                response = client.chat.completions.create(
                    model="gpt-4o", # Usa l'ultimo modello intelligente
                    messages=[
                        {"role": "system", "content": prompt_sistema},
                        {"role": "user", "content": email_cliente}
                    ],
                    response_format={ "type": "json_object" } # Obbliga a rispondere in JSON
                )
                
                st.write("⚙️ Incrocio dati con ERP e calcolo matematico dei margini...")
                
                # Legge e decodifica la risposta dell'AI
                risultato = json.loads(response.choices[0].message.content)
                
                st.write("✅ Generazione preventivo e bozza completata!")
                status.update(label="Preventivo Dinamico Generato!", state="complete", expanded=False)
                
                # --- MOSTRIAMO I RISULTATI A SCHERMO ---
                st.markdown("---")
                st.subheader("📊 2. Cruscotto Economico (Vista Interna)")
                
                col1, col2, col3 = st.columns(3)
                col1.metric(label="Costo di Produzione", value=f"€ {risultato['costo_produzione_totale']:.2f}".replace('.', ','))
                col2.metric(label="Margine Netto (40%)", value=f"€ {risultato['margine_netto']:.2f}".replace('.', ','))
                col3.metric(label="Prezzo di Vendita (da proporre)", value=f"€ {risultato['prezzo_vendita_finale']:.2f}".replace('.', ','), delta="Calcolato live")
                
                st.write(" ")
                st.markdown("**Dettaglio Distinta Base (elaborato dall'AI):**")
                
                df = pd.DataFrame(risultato['voci_preventivo'])
                
                # Formattiamo la tabella
                df['costo_unitario'] = df['costo_unitario'].apply(lambda x: f"€ {float(x):.2f}".replace('.', ','))
                df['costo_totale'] = df['costo_totale'].apply(lambda x: f"€ {float(x):.2f}".replace('.', ','))
                df.rename(columns={"codice": "Codice ERP", "descrizione": "Descrizione", "qta": "Quantità Rilevata", "costo_unitario": "Costo Unit. (€)", "costo_totale": "Totale (€)"}, inplace=True)
                
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                st.markdown("---")
                st.subheader("📧 3. Bozza Email Commerciale")
                st.text_area("L'AI ha scritto questa email basandosi sui calcoli reali appena fatti:", value=risultato['bozza_email'], height=350)
                
            except Exception as e:
                status.update(label="Errore di connessione", state="error", expanded=True)
                st.error("Assicurati che la chiave API sia corretta e attiva.")
                st.write(e)
