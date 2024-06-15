import streamlit as st
import pandas as pd
import sqlite3
from datetime import date

# Initialize SQLite database connection
def create_connection():
    return sqlite3.connect('itinerary_planner.db')

def create_tables(conn):
    with conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS itinerary (
            id INTEGER PRIMARY KEY,
            destination TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            notes TEXT
        );
        """)

def add_itinerary(conn, destination, start_date, end_date, notes):
    with conn:
        conn.execute("""
        INSERT INTO itinerary (destination, start_date, end_date, notes)
        VALUES (?, ?, ?, ?)
        """, (destination, start_date, end_date, notes))

def view_itineraries(conn):
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM itinerary ORDER BY start_date")
        rows = cur.fetchall()
    return rows

# Streamlit interface
conn = create_connection()
create_tables(conn)

st.title("Travel Itinerary Planner")

menu = ["Add Itinerary", "View Itineraries"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Itinerary":
    st.subheader("Add New Itinerary")
    destination = st.text_input("Destination")
    start_date = st.date_input("Start Date", value=date.today())
    end_date = st.date_input("End Date", value=date.today())
    notes = st.text_area("Notes")
    
    if st.button("Add Itinerary"):
        add_itinerary(conn, destination, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), notes)
        st.success("Itinerary added successfully!")

elif choice == "View Itineraries":
    st.subheader("View Itineraries")
    itineraries = view_itineraries(conn)
    if itineraries:
        df = pd.DataFrame(itineraries, columns=["ID", "Destination", "Start Date", "End Date", "Notes"])
        st.dataframe(df)
    else:
        st.info("No itineraries found.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("By: Your Name")
st.sidebar.markdown("[GitHub Repo](https://github.com/yourusername/itinerary-planner)")