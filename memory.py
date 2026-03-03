from sqlalchemy import create_engine, text
import os

engine = create_engine(
    f"mysql+pymysql://{os.getenv('DB_USER')}:@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

def load_memory(session_id:int) -> str:
    print(session_id)
    with engine.connect() as conn:
        query = conn.execute(text("""
            SELECT role, message FROM chat_history WHERE session_id = :session_id ORDER BY created_at ASC 
        """), {"session_id":session_id})
        result = query.fetchall()
    
    history = []
    for role, message in result:
        history.append({"role": role, "message" : message})

    return history

def save_memory(session_id:int, user_id:int, role:str, message:str) -> str:
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO chat_history (session_id, user_id, role, message)
            VALUES (:session_id, :user_id, :role, :message)
        """), {"session_id":session_id, "user_id":user_id, "role":role, "message":message})
        conn.commit()
    return "Memory saved successfully"