from utils.db_connection import create_connection

def test_db():
    conn = create_connection()
    if conn:
        print("✅ Successfully connected to the database.")
        conn.close()
    else:
        print("❌ Failed to connect to the database.")

if __name__ == "__main__":
    test_db()
