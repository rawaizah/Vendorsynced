import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="VendorSynced Pro Max", page_icon="🔗", layout="wide")

st.markdown("""
<style>
.header {background: linear-gradient(90deg, #4f46e5, #a855f7, #ec4899); padding:28px; border-radius:20px; color:white; margin-bottom:18px;}
.card {background:white; padding:18px; border-radius:14px; box-shadow:0 6px 18px rgba(0,0,0,0.07);}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header"><h1>🔗 VendorSynced — Pro Max</h1><p>Sync. Manage. Scale. | Lovable → Streamlit | Full Features Added</p></div>', unsafe_allow_html=True)

# --- DATA ---
if 'vendors' not in st.session_state:
    st.session_state.vendors = [
        {"id":1, "Vendor":"Royal Catering", "Category":"Catering", "Status":"Synced", "Cost":150000, "Contact":"0300-1234567", "Rating":5, "EventDate":str(date.today()), "Notes":"Best for weddings"},
        {"id":2, "Vendor":"Bloom Decor", "Category":"Decor", "Status":"Pending", "Cost":85000, "Contact":"0321-7654321", "Rating":4, "EventDate":str(date.today()), "Notes":"Theme decor"},
        {"id":3, "Vendor":"Click Studio", "Category":"Photography", "Status":"Synced", "Cost":60000, "Contact":"0333-1112233", "Rating":5, "EventDate":str(date.today()), "Notes":"4K video included"},
    ]

df = pd.DataFrame(st.session_state.vendors)

# --- TOP METRICS ---
m1,m2,m3,m4,m5 = st.columns(5)
m1.metric("Total Vendors", len(df))
m2.metric("Synced", len(df[df.Status=="Synced"]))
m3.metric("Pending", len(df[df.Status=="Pending"]))
m4.metric("Avg Rating", f"{df.Rating.mean():.1f} ⭐" if len(df)>0 else "0")
m5.metric("Total Budget", f"Rs. {df.Cost.sum():,}")

st.divider()

# --- TABS ---
tab_dash, tab_vendors, tab_add = st.tabs(["📊 Dashboard & Analytics", "👥 Vendors Manager", "➕ Add / Import"])

with tab_dash:
    c1,c2 = st.columns(2)
    with c1:
        st.subheader("Cost by Category")
        if not df.empty:
            st.bar_chart(df.groupby("Category")["Cost"].sum(), width="stretch")
    with c2:
        st.subheader("Status Split")
        if not df.empty:
            st.write(df["Status"].value_counts())
            st.progress(len(df[df.Status=="Synced"])/len(df) if len(df)>0 else 0)
            st.caption(f"{len(df[df.Status=='Synced'])}/{len(df)} Synced")

    st.subheader("Quick Sync")
    if st.button("🔄 Sync All Pending Vendors Now", width="stretch"):
        for v in st.session_state.vendors:
            if v["Status"]=="Pending": v["Status"]="Synced"
        st.success("All vendors synced! ✅")
        st.rerun()

with tab_vendors:
    c_search, c_cat, c_sort = st.columns([2,1,1])
    search = c_search.text_input("🔍 Search", placeholder="Name, notes...")
    cat_f = c_cat.selectbox("Category", ["All","Catering","Decor","Photography","Music","Venue","Lighting"])
    sort_f = c_sort.selectbox("Sort by", ["Cost High to Low","Cost Low to High","Rating"])

    fdf = df.copy()
    if search:
        fdf = fdf[fdf.apply(lambda r: search.lower() in str(r.values).lower(), axis=1)]
    if cat_f!="All":
        fdf = fdf[fdf.Category==cat_f]
    if sort_f=="Cost High to Low": fdf = fdf.sort_values("Cost", ascending=False)
    if sort_f=="Cost Low to High": fdf = fdf.sort_values("Cost")
    if sort_f=="Rating": fdf = fdf.sort_values("Rating", ascending=False)

    st.dataframe(fdf.drop(columns=["id"]), width="stretch", hide_index=True)

    st.write("**Actions:**")
    for _, row in fdf.iterrows():
        ca, cb, cc, cd = st.columns([3,1,1,1])
        ca.write(f"**{row.Vendor}** — {row.Category} — Rs.{row.Cost} — {row.Rating}⭐")
        if cb.button("✅ Toggle", key=f"t_{row.id}"):
            for v in st.session_state.vendors:
                if v["id"]==row.id: v["Status"]="Synced" if v["Status"]=="Pending" else "Pending"
            st.rerun()
        if cc.button("🗑️ Delete", key=f"d_{row.id}"):
            st.session_state.vendors=[v for v in st.session_state.vendors if v["id"]!=row.id]
            st.rerun()
        cd.link_button("WhatsApp", f"https://wa.me/{row.Contact.replace('-','').replace(' ','')}?text=Hi {row.Vendor} - VendorSynced se contact")

    col1,col2 = st.columns(2)
    csv = df.to_csv(index=False).encode('utf-8')
    col1.download_button("📥 Export CSV", csv, "vendorsynced.csv", "text/csv", width="stretch")
    if col2.button("⚠️ Clear All Vendors", width="stretch"):
        st.session_state.vendors=[]
        st.rerun()

with tab_add:
    with st.form("add_full", clear_on_submit=True):
        c1,c2,c3 = st.columns(3)
        name = c1.text_input("Vendor Name *")
        cat = c2.selectbox("Category", ["Catering","Decor","Photography","Music","Venue","Lighting","Other"])
        cost = c3.number_input("Cost Rs. *", 0, step=5000)
        c4,c5,c6 = st.columns(3)
        contact = c4.text_input("Contact / WhatsApp")
        rating = c5.slider("Rating ⭐", 1,5,5)
        ev_date = c6.date_input("Event Date", date.today())
        notes = st.text_area("Notes / Package Details")
        status = st.selectbox("Status", ["Synced","Pending"])
        if st.form_submit_button("🚀 Save Vendor + Sync", width="stretch"):
            if name and cost>0:
                new_id = max([v["id"] for v in st.session_state.vendors], default=0)+1
                st.session_state.vendors.append({"id":new_id,"Vendor":name,"Category":cat,"Status":status,"Cost":cost,"Contact":contact,"Rating":rating,"EventDate":str(ev_date),"Notes":notes})
                st.success(f"✅ {name} Added & {status}!")
                st.rerun()
            else:
                st.error("Name & Cost required")

st.caption("Made with ❤️ — vendorsynced-raw.streamlit.app — Pro Max Version")
