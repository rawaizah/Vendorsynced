import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="VendorSynced", page_icon="🔗", layout="wide")

st.title("🔗 VendorSynced")
st.caption("Sync. Manage. Scale — Lovable style on Streamlit")

if 'vendors' not in st.session_state:
    st.session_state.vendors = [
        {"Vendor": "Royal Catering", "Category": "Catering", "Status": "Synced ✅", "Cost": 150000, "Contact": "0300-1234567"},
        {"Vendor": "Bloom Decor", "Category": "Decor", "Status": "Pending ⏳", "Cost": 85000, "Contact": "0321-7654321"},
        {"Vendor": "Click Studio", "Category": "Photography", "Status": "Synced ✅", "Cost": 60000, "Contact": "0333-1112233"},
    ]

df = pd.DataFrame(st.session_state.vendors)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Vendors", len(df))
c2.metric("Synced", len(df[df['Status'].str.contains("Synced")]))
c3.metric("Total Budget", f"Rs. {df['Cost'].sum():,}")

tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "👥 Vendors", "➕ Add Vendor"])

with tab1:
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.bar_chart(df.groupby("Category")["Cost"].sum())

with tab2:
    st.dataframe(df, use_container_width=True, hide_index=True)

with tab3:
    with st.form("add", clear_on_submit=True):
        name = st.text_input("Vendor Name")
        cat = st.selectbox("Category", ["Catering","Decor","Photography","Music","Venue"])
        cost = st.number_input("Cost", min_value=0, step=1000)
        if st.form_submit_button("Save & Sync"):
            st.session_state.vendors.append({"Vendor":name, "Category":cat, "Status":"Synced ✅", "Cost":cost, "Contact":""})
            st.success("Added!")
            st.rerun()
