import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# വെബ്സൈറ്റ് ടൈറ്റിൽ
st.set_page_config(page_title="Hiba Shop Manager", layout="centered")

st.title("📝 Hiba Shop Daily Entry")

# ലോഗിൻ സിസ്റ്റം
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    with st.form("login_form"):
        username = st.text_input("User Name")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if username == "admin" and password == "hiba123":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid Username or Password")
else:
    # ഗൂഗിൾ ഷീറ്റ് കണക്ഷൻ
    # Secrets-ൽ നൽകിയിരിക്കുന്ന ലിങ്ക് വഴി കണക്ട് ചെയ്യുന്നു
    conn = st.connection("gsheets", type=GSheetsConnection)

    # നിലവിലുള്ള ഡാറ്റ വായിക്കുന്നു
    try:
        existing_data = conn.read(ttl=0)
    except:
        existing_data = pd.DataFrame(columns=["DATE", "SALE", "PURCHASE"])

    # ഡാറ്റ എന്ട്രി ഫോം
    with st.form("entry_form", clear_on_submit=True):
        date = st.date_input("Date", datetime.now())
        sale = st.number_input("Total Sale", min_value=0.0, step=0.1)
        purchase = st.number_input("Total Purchase", min_value=0.0, step=0.1)
        
        submitted = st.form_submit_button("Save to Google Sheet")

        if submitted:
            # പുതിയ ഡാറ്റ ഒരു റോ ആയി ഉണ്ടാക്കുന്നു
            new_entry = pd.DataFrame([{"DATE": str(date), "SALE": sale, "PURCHASE": purchase}])
            
            # നിലവിലുള്ള ഡാറ്റയുമായി ചേർക്കുന്നു
            updated_df = pd.concat([existing_data, new_entry], ignore_index=True)
            
            # ഷീറ്റിലേക്ക് സേവ് ചെയ്യുന്നു
            try:
                conn.update(spreadsheet=st.secrets["connections"]["gsheets"]["spreadsheet"], data=updated_df)
                st.success("Data successfully saved!")
            except Exception as e:
                st.error(f"Error: {e}")

    # Logout ബട്ടൺ
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
