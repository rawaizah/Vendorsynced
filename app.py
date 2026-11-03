import streamlit as st
import pandas as pd

st.set_page_config(page_title="VendorSynced", page_icon="🔗", layout="wide")

st.title("🔗 VendorSynced")
st.write("Sync. Manage. Scale — Lovable style on Streamlit")

if 'vendors' not in st.session_state:
    st.session_state.vendors = [
        {"Vendor": "Royal Catering", "Category": "Catering", "Status": "Synced", "Cost": 150000},
        {"Vendor": "Bloom Decor", "Category": "Decor", "Status": "Pending", "Cost": 85000},
        {"Vendor": "Click Studio", "Category": "Photography", "Status": "Synced", "Cost": 60000},
    ]

df = pd.DataFrame(st.session_state.vendors)

c1, c2, c3 = st.columns(3)
c1.metric("Total Vendors", len(df))
c2.metric("Synced", 2)
c3.metric("Total Budget", f"Rs. {df['Cost'].sum()}")

st.divider()
st.subheader("All Vendors")
st.table(df)

st.subheader("Add New Vendor")
with st.form("add", clear_on_submit=True):
    name = st.text_input("Vendor Name")
    cat = st.selectbox("Category", ["Catering","Decor","Photography","Music","Venue"])
    cost = st.number_input("Cost", 0, step=1000)
    if st.form_submit_button("Save & Sync"):
        if name:
            st.session_state.vendors.append({"Vendor":name, "Category":cat, "Status":"Synced", "Cost":cost})
            st.success("Added!")
            st.rerun()
