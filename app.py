import streamlit as st
import pandas as pd
import os

# പേജ് സെറ്റിംഗ്സ്
st.set_page_config(page_title="HIBA SHOPPING CENTER", layout="wide")

# ലോഗിൻ വിവരങ്ങൾ
USER_CREDENTIALS = {"admin": "hiba123", "staff": "staff123"}

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# ലോഗിൻ വിൻഡോ
if not st.session_state['logged_in']:
    st.title("🔐 HIBA SHOPPING CENTER - Login")
    user = st.text_input("User Name")
    pw = st.text_input("Password", type="password")
    if st.button("Login"):
        if user in USER_CREDENTIALS and USER_CREDENTIALS[user] == pw:
            st.session_state['logged_in'] = True
            st.session_state['user_role'] = user
            st.rerun()
        else:
            st.error("Username അല്ലെങ്കിൽ Password തെറ്റാണ്!")

else:
    st.sidebar.title(f"Welcome, {st.session_state['user_role'].upper()}")
    choice = st.sidebar.radio("Menu", ["Dashboard", "Daily Entry", "Master Upload", "Logout"])

    if choice == "Logout":
        st.session_state['logged_in'] = False
        st.rerun()

    file_path = 'shop_data.csv'

    if choice == "Dashboard":
        st.title("📊 Business Overview")
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
            years = sorted(df['DATE'].dt.year.unique(), reverse=True)
            if years:
                year = st.sidebar.selectbox("Select Year", years)
                year_df = df[df['DATE'].dt.year == year]
                st.metric(f"Total Sale - {year}", f"{year_df['SALE'].sum():,.3f} OMR")
                st.dataframe(year_df, use_container_width=True)
            else:
                st.info("ഫയലിൽ ഡാറ്റയൊന്നും കാണുന്നില്ല.")
        else:
            st.info("ഡാറ്റ ലഭ്യമല്ല. ദയവായി ഡാറ്റ ചേർക്കുക.")

    elif choice == "Daily Entry":
        st.title("📝 Daily Entry")
        with st.form("entry_form"):
            d = st.date_input("Date")
            s = st.number_input("Sale", format="%.3f")
            p = st.number_input("Purchase", format="%.3f")
            if st.form_submit_button("Save"):
                new_data = pd.DataFrame([[d, s, p]], columns=['DATE', 'SALE', 'PURCHASE'])
                new_data.to_csv(file_path, mode='a', header=not os.path.exists(file_path), index=False)
                st.success("വിജയകരമായി സേവ് ചെയ്തു!")

    elif choice == "Master Upload":
        st.title("📂 Master File Upload")
        uploaded_file = st.file_uploader("നിങ്ങളുടെ CSV ഫയൽ ഇവിടെ അപ്‌ലോഡ് ചെയ്യുക", type=['csv'])
        if uploaded_file:
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success("ഫയൽ അപ്‌ലോഡ് ചെയ്തു!")