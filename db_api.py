import os
from pathlib import Path

import psycopg
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()


class NoteIn(BaseModel):
    text: str = Field(min_length=1, max_length=500)


def connect_db():
    secret_path = os.getenv("DB_PASSWORD_FILE")

    if secret_path:
        password = Path(secret_path).read_text().strip()
    else:
        password = os.environ["DB_PASSWORD"]

    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        dbname=os.getenv("DB_NAME", "lab7"),
        user=os.getenv("DB_USER", "lab7"),
        password=password,
        connect_timeout=5,
    )


def init_db():
    with connect_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id BIGSERIAL PRIMARY KEY,
                text VARCHAR(500) NOT NULL
            )
        """)


@router.post("/notes", status_code=201)
def create_note(note: NoteIn):
    with connect_db() as conn:
        row = conn.execute(
            "INSERT INTO notes (text) VALUES (%s) RETURNING id, text",
            (note.text,),
        ).fetchone()

    return {"id": row[0], "text": row[1]}


@router.get("/notes/{note_id}")
def get_note(note_id: int):
    with connect_db() as conn:
        row = conn.execute(
            "SELECT id, text FROM notes WHERE id = %s",
            (note_id,),
        ).fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found",
        )

    return {"id": row[0], "text": row[1]}
