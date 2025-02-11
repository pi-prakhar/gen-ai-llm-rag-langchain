import sqlite3
import json
from rag_pipeline import get_rag_response

# Fetch user data from SQLite
def fetch_user_data(user_id):
    conn = sqlite3.connect('data/user_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    
    if user_data:
        return {
            "user_id": user_data[0],
            "cards": user_data[1],
            "spends": json.loads(user_data[2]),
            "credit_limits": json.loads(user_data[3]),
            "due_dates": json.loads(user_data[4]),
            "fees_waive_off_limits": json.loads(user_data[5])
        }
    return None

def generate_response(user_id, query):
    # Fetch user data
    user_data = fetch_user_data(user_id)
    if not user_data:
        return "User not found."

    # Format user details into a readable string
    user_context = f"""
    User Data:
    - Cards Owned: {', '.join(user_data["cards"].split(','))}
    - Monthly Dining Spends: {json.dumps(user_data["spends"], indent=2)}
    - Credit Limits: {json.dumps(user_data["credit_limits"], indent=2)}
    - Due Dates: {json.dumps(user_data["due_dates"], indent=2)}
    - Fees Waive-Off Limits: {json.dumps(user_data["fees_waive_off_limits"], indent=2)}
    """

    # Combine user data with the query to get a personalized response
    enhanced_query = f"""
    Context:
    {user_context}

    Question:
    {query}

    Summarize your answer in a few lines and in the format below with answer and reason like this chosen card,  reason (3 lines)
    """

    # Fetch RAG-based response with user data included
    rag_response, source_docs = get_rag_response(enhanced_query)

    # Final response format
    response = f"""
    {user_context}

    Question:
    {query}

    Answer:
    {rag_response}
    """

    return response  # Returns the final personalized answer

# Example usage
if __name__ == "__main__":
    user_id = "123"
    query = "Which card is best for Swiggy Dine Out? i have a bill of 4000 rupees"
    response = generate_response(user_id, query)
    print(response)
