import streamlit as st
import pandas as pd

st.set_page_config(page_title="VendorSynced", page_icon="🎉", layout="wide")

st.title("🎉 VendorSynced - Vendor Management")
st.write("Apne vendors ko asani se manage karein")

if 'vendors' not in st.session_state:
    st.session_state.vendors = []

with st.form("vendor_form"):
    st.subheader("Add New Vendor")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Vendor Name *")
        company = st.text_input("Company")
        category = st.selectbox("Category", ["Catering", "Decor", "Photography", "Music", "Other"])
    with col2:
        cost = st.number_input("Total Cost", min_value=0)
        advance = st.number_input("Advance Paid", min_value=0)
        phone = st.text_input("Phone")
    
    submitted = st.form_submit_button("➕ Add Vendor", use_container_width=True)
    if submitted:
        if not name:
            st.error("Name likhna zaroori hai!")
        else:
            st.session_state.vendors.append({
                "Name": name,
                "Company": company,
                "Category": category,
                "Cost": cost,
                "Advance": advance,
                "Balance": cost - advance,
                "Phone": phone
            })
            st.success(f"{name} add ho gaya!")
            st.rerun()

st.divider()

if st.session_state.vendors:
    df = pd.DataFrame(st.session_state.vendors)
    
    search = st.text_input("🔍 Search vendor...", placeholder="Name ya Company search karein")
    if search:
        df = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]
    
    st.dataframe(df, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Vendors", len(df))
    with col2:
        st.metric("Total Balance", f"Rs. {df['Balance'].sum()}")
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Excel (CSV) Download", csv, "vendorsynced.csv", "text/csv", use_container_width=True)
else:
    st.info("Abhi koi vendor nahi hai. Upar form se add karein.")
