import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. നിങ്ങളുടെ ഗൂഗിൾ ഷീറ്റ് ലിങ്ക് താഴെ നൽകുക
url = "https://docs.google.com/spreadsheets/d/1pyFeXlE59TjtyrYzoar8X6bH02ZBmRP43m3lmj0GfkI/edit?usp=sharing"

# പേജ് സെറ്റിംഗ്സ്
st.set_page_config(page_title="HIBA SHOPPING CENTER", layout="wide")

# കണക്ഷൻ സെറ്റ് ചെയ്യുന്നു
conn = st.connection("gsheets", type=GSheetsConnection)

# ലോഗിൻ വിവരങ്ങൾ
USER_CREDENTIALS = {"admin": "hiba123", "staff": "staff123"}

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("🔐 HIBA SHOPPING CENTER - Login")
    user = st.text_input("User Name")
    pw = st.text_input("Password", type="password")
    if st.button("Login"):
        if user in USER_CREDENTIALS and USER_CREDENTIALS[user] == pw:
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("Invalid Username or Password")
else:
    choice = st.sidebar.radio("Menu", ["Dashboard", "Daily Entry", "Logout"])

    if choice == "Logout":
        st.session_state['logged_in'] = False
        st.rerun()

    if choice == "Dashboard":
        st.title("📊 Business Dashboard")
        try:
            df = conn.read(spreadsheet=url)
            st.dataframe(df, use_container_width=True)
        except:
            st.info("ഡാറ്റ ലഭ്യമല്ല. Daily Entry വഴി പുതിയത് ചേർക്കുക.")

    elif choice == "Daily Entry":
        st.title("📝 Daily Data Entry")
        with st.form("entry_form"):
            date = st.date_input("Date")
            sale = st.number_input("Total Sale", format="%.3f")
            purchase = st.number_input("Total Purchase", format="%.3f")
            
            if st.form_submit_button("Save to Google Sheets"):
                try:
                    existing_data = conn.read(spreadsheet=url)
                except:
                    existing_data = pd.DataFrame(columns=["DATE", "SALE", "PURCHASE"])
                
                new_row = pd.DataFrame([{"DATE": str(date), "SALE": sale, "PURCHASE": purchase}])
                updated_df = pd.concat([existing_data, new_row], ignore_index=True)
                
                conn.update(spreadsheet=url, data=updated_df)
                st.success("വിജയകരമായി ഗൂഗിൾ ഷീറ്റിൽ സേവ് ചെയ്തു!")
