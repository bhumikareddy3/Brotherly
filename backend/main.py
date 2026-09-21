import os
import re
from typing import Literal, Optional

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, field_validator
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from auth import create_access_token, decode_access_token, hash_password, verify_password
from ai.mentor import get_mentor_response
from database.db import (
    create_database,
    create_user,
    get_user_by_email,
    get_user_by_id,
    save_assessment,
    save_chat,
    get_chats,
    get_total_assessments,
    get_total_chats,
    get_all_assessments,
    get_latest_assessment,
)
from recommendation.action_plans import get_action_plan
from recommendation.career_paths import get_career_path
from recommendation.profiles import generate_profile
from recommendation.rules import get_recommendation
from recommendation.scoring import calculate_scores

app = FastAPI(title="Brotherly API")

GOOGLE_CLIENT_ID = "750860405732-64hbjc31bug369207fi18envrhuv5iu6.apps.googleusercontent.com"

ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://brotherly-ten.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_database()

class RegisterIn(BaseModel):
    name: str
    email: EmailStr
    password: str

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v):
        if not v.strip():
            raise ValueError("Name is required.")
        return v.strip()

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters.")
        return v

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class GoogleAuthIn(BaseModel):
    credential: str

class AuthOut(BaseModel):
    token: str
    user: dict

def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated.")

    token = authorization.removeprefix("Bearer ").strip()
    user_id = decode_access_token(token)

    if user_id is None:
        raise HTTPException(status_code=401, detail="Your session has expired. Please log in again.")

    user = get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Account not found.")

    return user

@app.post("/api/auth/register", response_model=AuthOut)
def register(payload: RegisterIn):
    if get_user_by_email(payload.email):
        raise HTTPException(status_code=409, detail="An account with this email already exists.")

    password_hash = hash_password(payload.password)
    user_id = create_user(payload.name, payload.email, password_hash)

    token = create_access_token(user_id)
    return {"token": token, "user": {"id": user_id, "name": payload.name, "email": payload.email.lower()}}

@app.post("/api/auth/login", response_model=AuthOut)
def login(payload: LoginIn):
    user = get_user_by_email(payload.email)

    if user is None or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password.")

    token = create_access_token(user["id"])
    return {
        "token": token,
        "user": {"id": user["id"], "name": user["name"], "email": user["email"]},
    }

@app.post("/api/auth/google", response_model=AuthOut)
def google_auth(payload: GoogleAuthIn):
    try:
        idinfo = id_token.verify_oauth2_token(
            payload.credential,
            google_requests.Request(),
            GOOGLE_CLIENT_ID
        )
        email = idinfo["email"].lower()
        name = idinfo.get("name", email.split("@")[0])
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Google authentication token.")

    user = get_user_by_email(email)
    if user is None:
        user_id = create_user(name, email, "OAUTH_GOOGLE_USER")
    else:
        user_id = user["id"]
        name = user["name"]

    token = create_access_token(user_id)
    return {
        "token": token,
        "user": {"id": user_id, "name": name, "email": email},
    }

@app.get("/api/auth/me")
def me(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}

class AssessmentIn(BaseModel):
    name: str
    age: int
    education: str
    current_status: str
    experience: int
    current_role: Optional[str] = ""
    savings: str
    dependents: Literal["Yes", "No"]
    income_stability: int
    income_reduction: int
    financial_pressure: int
    risk_uncertainty: int
    risk_opportunity: int
    risk_failure: int
    risk_relocation: int
    risk_decision: int
    environment: str
    leadership: Literal["Yes", "Sometimes", "No"]
    work_type: str
    self_discipline: int
    initiative: int
    interest: str
    priority: str
    built_project: Literal["Yes", "No"]
    sold_service: Literal["Yes", "No"]
    long_term_goal: str

class AssessmentContext(BaseModel):
    primary: Optional[str] = None
    secondary: Optional[str] = None
    career_path: Optional[str] = None
    scores: Optional[dict] = None
    profile: Optional[list] = None

class ChatIn(BaseModel):
    message: str
    context: Optional[AssessmentContext] = None

@app.post("/api/assessment")
def submit_assessment(payload: AssessmentIn, current_user: dict = Depends(get_current_user)):
    if not payload.name.strip():
        raise HTTPException(status_code=400, detail="Name is required.")

    data = payload.model_dump()

    scores = calculate_scores(data)
    primary, secondary = get_recommendation(scores)
    career_path = get_career_path(scores, data)
    profile = generate_profile(data, scores)
    plan = get_action_plan(primary)

    warning = None
    try:
        save_assessment(
            current_user["id"],
            data["name"], data["age"], data["education"], data["current_status"],
            data["experience"], primary, secondary, career_path, scores,
        )
    except Exception as error:
        warning = f"Your result is ready, but it could not be added to history: {error}"

    return {
        "primary": primary,
        "secondary": secondary,
        "career_path": career_path,
        "scores": scores,
        "profile": profile,
        "plan": plan,
        "name": data["name"],
        "warning": warning,
    }

@app.get("/api/dashboard")
def dashboard(current_user: dict = Depends(get_current_user)):
    latest = get_latest_assessment(current_user["id"])
    if latest is None:
        return {"has_data": False}

    all_assessments = get_all_assessments(current_user["id"])
    chat_count = get_total_chats(current_user["id"])

    return {
        "has_data": True,
        "latest": latest,
        "total_assessments": len(all_assessments),
        "chat_count": chat_count,
        "plan": get_action_plan(latest["primary_recommendation"]),
    }

@app.get("/api/history")
def history(current_user: dict = Depends(get_current_user)):
    assessments = get_all_assessments(current_user["id"])
    return {"assessments": assessments}

@app.post("/api/mentor/chat")
def mentor_chat(payload: ChatIn, current_user: dict = Depends(get_current_user)):
    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="Message is required.")

    context = payload.context.model_dump() if payload.context else {}

    try:
        answer = get_mentor_response(payload.message, context)
    except Exception:
        raise HTTPException(
            status_code=502,
            detail="I couldn't reach the mentor service just now. Check the API key and connection, then try again.",
        )

    try:
        save_chat(current_user["id"], payload.message, answer)
    except Exception:
        pass

    return {"reply": answer}

@app.get("/api/chats")
def chats(current_user: dict = Depends(get_current_user)):
    rows = get_chats(current_user["id"])
    return {
        "chats": [
            {"user_message": r[0], "ai_response": r[1], "created_at": r[2]}
            for r in rows
        ]
    }

@app.get("/api/health")
def health():
    return {"status": "ok"}