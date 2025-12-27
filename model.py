import sqlite3
import pandas as pd



def get_polling_unit_results(unit_id):
    # Connect to the database we created in the previous step
    conn = sqlite3.connect('election_results.db')
    
    # Direct SQL query to get party names and scores
    # We use '?' as a placeholder to prevent SQL Injection
    query = """
    SELECT party_abbreviation AS Party, SUM(party_score) AS Score 
    FROM announced_pu_results 
    WHERE polling_unit_uniqueid = ?
    GROUP BY party_abbreviation
    """
    
    # Use pandas to run the SQL and return a table (DataFrame)
    df = pd.read_sql(query, conn, params=(unit_id,))
    conn.close()
    return df


def get_lga_totals(lga_id):
    conn = sqlite3.connect('election_results.db')
    query = """
        SELECT r.party_abbreviation AS Party, SUM(r.party_score) AS Score
        FROM announced_pu_results r
        JOIN polling_unit p ON r.polling_unit_uniqueid = p.uniqueid
        WHERE p.lga_id = ?
        GROUP BY r.party_abbreviation
    """
    df = pd.read_sql(query, conn, params=(lga_id,))
    conn.close()
    return df


def get_all_lgas():
    conn = sqlite3.connect('election_results.db')
    df = pd.read_sql("SELECT lga_id, lga_name FROM lga", conn)
    conn.close()
    return df


def save_new_result(pu_id, party, score, user):
    try:
        conn = sqlite3.connect('election_results.db')
        curr = conn.cursor()
        
        # Get the next result_id
        curr.execute("SELECT MAX(result_id) FROM announced_pu_results")
        max_id = curr.fetchone()[0] or 0
        new_id = max_id + 1
        
        curr.execute("""
            INSERT INTO announced_pu_results (result_id, polling_unit_uniqueid, party_abbreviation, party_score, entered_by_user, date_entered, user_ip_address)
            VALUES (?, ?, ?, ?, ?, datetime('now'), '127.0.0.1')
        """, (new_id, pu_id, party, score, user))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"DATABASE ERROR: {e}")
        return False
    
   
def audit_trail(limit=5):
    """
    Fetches the most recently added election results to verify 
    that new data is being saved correctly.
    """
    try:
        conn = sqlite3.connect('election_results.db')
        
        # We use '?' to pass the limit safely
        query = "SELECT * FROM announced_pu_results ORDER BY result_id DESC LIMIT ?"
        
        # Pass limit as a tuple: (limit,)
        debug_df = pd.read_sql(query, conn, params=(limit,))
        
        conn.close()
        return debug_df
    except Exception as e:
        print(f"Error fetching audit trail: {e}")
        return pd.DataFrame()