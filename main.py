from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4, UUID
import models, auth, database, myfxbook
from dotenv import load_dotenv
import os

app = FastAPI()

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
cursor = database.cursor
conn = database.conn

@app.post("/api/register")
def register_user(user: models.RegisterInput):
    cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="User already exists")
    user_id = str(uuid4())
    hashed = auth.hash_password(user.password)
    cursor.execute("INSERT INTO users (id, email, full_name, password) VALUES (%s, %s, %s, %s)",
                   (user_id, user.email, user.full_name, hashed))
    conn.commit()
    return {"user_id": user_id}

@app.post("/api/login")
def login_user(data: models.LoginInput):
    cursor.execute("SELECT * FROM users WHERE email = %s", (data.email,))
    user = cursor.fetchone()
    if not user or not auth.verify_password(data.password, user['password']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth.create_access_token({"sub": str(user['id'])})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/api/evaluation")
def submit_evaluation(result: models.EvaluationResult):
    cursor.execute("SELECT * FROM users WHERE id = %s", (str(result.user_id),))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="User not found")
    cursor.execute("INSERT INTO evaluations (user_id, score, passed) VALUES (%s, %s, %s)",
                   (str(result.user_id), result.score, result.passed))
    conn.commit()
    return {"message": "Evaluation recorded"}

@app.get("/api/evaluation/{user_id}")
def get_evaluation(user_id: UUID):
    cursor.execute("SELECT * FROM evaluations WHERE user_id = %s", (str(user_id),))
    result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    return result

@app.get("/api/myfxbook/accounts")
def get_fxbook_accounts():
    session = myfxbook.login_myfxbook()
    return myfxbook.get_accounts(session)

@app.get("/api/myfxbook/performance/{account_id}")
def fxbook_performance(account_id: int):
    session = myfxbook.login_myfxbook()
    return myfxbook.get_account_performance(session, account_id)