import os
import mysql.connector
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
conn = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    global conn
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "impuestos")
    )
    print("Conectado a MySQL")

class Impuesto(BaseModel):
    numero_impuesto: str
    cif_empresa: str
    nif_cliente: str
    total_a_recaudar: float
    datos: dict

@app.post("/api/impuestos")
def crear_impuesto(impuesto: Impuesto):
    global conn
    cur = conn.cursor()

    query = """
        INSERT INTO impuestos (numero_impuesto, cif_empresa, nif_cliente, total_a_recaudar, datos)
        VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        impuesto.numero_impuesto,
        impuesto.cif_empresa,
        impuesto.nif_cliente,
        impuesto.total_a_recaudar,
        json.dumps(impuesto.datos)
    )

    cur.execute(query, values)
    conn.commit()
    cur.close()

    return {"status": "ok", "mensaje": "Impuesto registrado correctamente"}

# http://localhost:8000/api/impuestos