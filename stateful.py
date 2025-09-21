import os
import openai
import psycopg2
from dotenv import load_dotenv
import os
import psycopg2
from dotenv import load_dotenv\

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

client = openai.OpenAI(api_key=OPENAI_API_KEY, base_url="Url, dont need if is from openai"
)

def get_conversation_history(user_id, limit=5):
    """Retrieves the last few conversation turns for a given user."""
    history = []
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        query = """
            SELECT user_manager, ai_response
            FROM conversation
            WHERE user_id = %s
            ORDER BY timestamp DESC
            LIMIT %s;
            """
        cur.execute(query, (user_id, limit))
        rows = cur.fetchall()
        for row in reversed(rows):
            history.append({"role": "user", "content": row[0]})
            history.append({"role": "assistant", "content": row[1]})
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f'error in the conversation: {error}')
    finally:
        if conn is not None:
            conn.close()
    return history
def save_conversation(user_id, user_manager, ai_response):
    """saves new conversation turn to the database."""
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        insert_query = """INSERT INTO conversation (user_id, user_manager, ai_response) VALUES(%s,%s,%s);
        """
        cur.execute(insert_query, (user_id, user_manager, ai_response))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f'Error saving conversation: {error}')
    finally:
        if conn is not None:
            conn.close()

def get_ai_response(user_id, user_manager):
    """Generates a response from the AI, using conversation history as context."""
    history = get_conversation_history(user_id)

    menssages = [{"role": "system", "content": "You are a helpful assistant."}]

    menssages.extend(history)

    menssages.append({"role": "user", "content": user_manager})

    try:
        response = client.chat.completions.create(
            model="",
            messages=menssages,
            temperature=0.7,
        )
        ai_message = response.choices[0].message.content

        save_conversation(user_id, user_manager, ai_message)

        return ai_message
    except Exception as e:
        return f"Erro getting AI response: {e}"
if __name__ == "__main__":
    user_id = "test_user_123"
    print("Stateful AI is ready. Type 'exit' to end the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        ai_response = get_ai_response(user_id, user_input)
        print(f"AI: {ai_response}")