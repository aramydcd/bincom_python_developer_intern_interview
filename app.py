import streamlit as st
from model import get_polling_unit_results, get_all_lgas, get_lga_totals, save_new_result,audit_trail
import sqlite3
import pandas as pd



# Page Configuration
st.set_page_config(page_title="Bincom Assessment", layout="wide")

st.title("Bincom Assessment")

# Navigation Tab
tab1,tab2,tab3 = st.tabs(["Question 1: Polling Unit", "Question 2: LGA Totals","Question 3: Store Results"])


with tab1:
    # --- QUESTION 1 CODE ---
    st.title("Polling Unit Result Viewer")
    st.markdown("Enter a Polling Unit Unique ID below to see the results for all parties.")

    # User Input
    unit_id = st.number_input("Enter Polling Unit Unique ID (e.g., 8, 9, 10...)", min_value=1, value=8)

    if st.button("Fetch Results"):
        # Call our SQL function
        results_df = get_polling_unit_results(unit_id)
        
        if not results_df.empty:
            st.success(f"Displaying results for Polling Unit ID: {unit_id}")
            
            col1,col2 = st.columns(2,border=True)
            
            # Display the data in a clean table
            col1.dataframe(results_df, hide_index=True, use_container_width=True)
            
            # Bonus: Show a bar chart for better visualization
            col2.bar_chart(results_df.set_index('Party'))
        else:
            st.warning("No results found for this Polling Unit ID. Please try another one.")
            
with tab2:
    # --- QUESTION 2 CODE ---
    st.title("LGA Total Results")
    
    lgas = get_all_lgas() # Should return a dataframe with lga_id and lga_name
    lga_options = {row['lga_name']: row['lga_id'] for _, row in lgas.iterrows()}
    
    selected_lga = st.selectbox("Select Local Government below to see the results for all parties.", options=list(lga_options.keys()))
    lga_id = lga_options[selected_lga]

    if st.button("Calculate Total Scores"):
        df_lga = get_lga_totals(lga_id)
        
        if not df_lga.empty:
            st.info(f"Summary for {selected_lga}")
            c1, c2 = st.columns(2, border=True)
            c1.dataframe(df_lga, hide_index=True, use_container_width=True)
            c2.bar_chart(df_lga.set_index('Party'))
        else:
            st.warning("No data found for this LGA.")
            
with tab3:
    st.title("Store New Polling Unit Results")
    st.markdown("Use this form to add scores for a new polling unit.")

    with st.form("add_result_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            new_pu_id = st.number_input("Polling Unit Unique ID", min_value=1)
            new_party = st.selectbox("Party", ["PDP", "DPP", "ACN", "PPA", "CDC", "JP", "ANPP", "LABO", "CPP"])
        with col2:
            new_score = st.number_input("Score", min_value=0)
            entered_by = st.text_input("Entered By (Your Name)")

        submitted = st.form_submit_button("Save Result to Database")

        if submitted:
            success = save_new_result(new_pu_id, new_party, new_score, entered_by)
            if success:
                st.success("Result successfully recorded!")
            else:
                st.error("Failed to save result. Check database connection.")
            
    st.divider()
    st.subheader("Recent Database Activity")
    
    if st.button("Refresh Audit Trail"):
        recent_data = audit_trail(5)
        if not recent_data.empty:
            st.write("Last 5 entries saved to the database:")
            st.dataframe(recent_data, hide_index=True, use_container_width=True)
        else:
            st.info("No recent entries found.")