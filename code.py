import streamlit as st
import sqlite3

# ---------- Database Setup ----------
def init_db():
    conn = sqlite3.connect("complaints.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS complaints (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    room_no TEXT,
                    category TEXT,
                    priority TEXT,
                    description TEXT
                )''')
    conn.commit()
    conn.close()

def add_complaint(username, room_no, category, priority, description):
    conn = sqlite3.connect("complaints.db")
    c = conn.cursor()
    c.execute("INSERT INTO complaints (username, room_no, category, priority, description) VALUES (?, ?, ?, ?, ?)",
              (username, room_no, category, priority, description))
    conn.commit()
    conn.close()

def view_complaints():
    conn = sqlite3.connect("complaints.db")
    c = conn.cursor()
    c.execute("SELECT * FROM complaints ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    return data

def delete_complaint(complaint_id):
    conn = sqlite3.connect("complaints.db")
    c = conn.cursor()
    c.execute("DELETE FROM complaints WHERE id=?", (complaint_id,))
    conn.commit()
    conn.close()

# ---------- Streamlit UI ----------
st.set_page_config(page_title="Hostel Complaint System", layout="centered")
st.title("🏠 Hostel Complaint Management System")

init_db()

menu = ["Submit Complaint", "View Complaints", "Delete Complaint"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------- Submit Complaint ----------
if choice == "Submit Complaint":
    st.subheader("✍️ Submit a Complaint")
    
    username = st.text_input("Enter Your Name")
    room = st.text_input("Room No")
    category = st.selectbox("Category", ["Wifi", "Laundry", "Electricity", "Water", "Other"])
    priority = st.radio("Priority", ["High", "Medium", "Low"])
    desc = st.text_area("Complaint Description")

    if st.button("Submit"):
        if username and room and desc:
            add_complaint(username, room, category, priority, desc)
            st.success("✅ Complaint Submitted Successfully!")
        else:
            st.error("⚠️ Please fill all fields.")

# ---------- View Complaints ----------
elif choice == "View Complaints":
    st.subheader("📋 All Complaints")
    rows = view_complaints()
    if rows:
        st.table(rows)
    else:
        st.info("No complaints found.")

# ---------- Delete Complaint ----------
elif choice == "Delete Complaint":
    st.subheader("🗑️ Delete a Complaint")
    complaint_id = st.number_input("Enter Complaint ID to Delete", min_value=1, step=1)

    if st.button("Delete"):
        delete_complaint(complaint_id)
        st.success(f"✅ Complaint ID {complaint_id} Deleted.")

