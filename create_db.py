import sqlite3

# Create a SQLite database
conn = sqlite3.connect('data/user_data.db')
cursor = conn.cursor()

# Create a table for user data
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    cards TEXT,
    spends TEXT,
    credit_limits TEXT,
    due_dates TEXT,
    fees_waive_off_limits TEXT
)
''')

# Insert sample user data
cursor.execute('''
INSERT INTO users (user_id, cards, spends, credit_limits, due_dates, fees_waive_off_limits)
VALUES ('123', 'HDFC Millenia, SBI SimplyClick', '{"HDFC Millenia": {"dining": 8000}, "SBI SimplyClick": {"dining": 2000}}', '{"HDFC Millenia": 50000, "SBI SimplyClick": 30000}', '{"HDFC Millenia": "2023-11-15", "SBI SimplyClick": "2023-11-20"}', '{"HDFC Millenia": 500, "SBI SimplyClick": 300}')
''')

conn.commit()
conn.close()
