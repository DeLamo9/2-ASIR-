import os
import mysql.connector
import xmltodict
from fastapi import FastAPI, Request, Response
from datetime import date
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

@app.post("/api/impuestos", response_class=Response)
async def crear_impuesto(request: Request):
    global conn
    cur = conn.cursor()

    body = await request.body()
    try:
        data_dict = xmltodict.parse(body)
        impuesto = data_dict.get("Impuesto", {})
    except Exception as e:
        return Response(
            content=f"<error>XML invalido: {str(e)}</error>",
            media_type="application/xml",
            status_code=400
        )

    numero_impuesto = impuesto.get("numero_impuesto")
    cif_empresa = impuesto.get("cif_empresa")
    nif_cliente = impuesto.get("nif_cliente")
    total_a_recaudar = float(impuesto.get("total_a_recaudar", 0))
    datos = impuesto.get("datos", {})

    query = """
        INSERT INTO impuestos (numero_impuesto, cif_empresa, nif_cliente, total_a_recaudar, datos)
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (numero_impuesto, cif_empresa, nif_cliente, total_a_recaudar, str(datos))
    cur.execute(query, values)
    conn.commit()
    cur.close()

    response_xml = f"""
    <respuesta>
        <status>ok</status>
        <mensaje>Impuesto registrado correctamente</mensaje>
        <numero_impuesto>{numero_impuesto}</numero_impuesto>
    </respuesta>
    """
    
    return Response(content=response_xml.strip(), media_type="application/xml")

# http://localhost:8000/api/impuestos