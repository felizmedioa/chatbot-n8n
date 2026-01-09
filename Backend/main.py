from fastapi import FastAPI, HTTPException#Lo principal de fastapi
from fastapi.middleware.cors import CORSMiddleware #Nos ayudará a configurar el CORS y los permisos
from pydantic import BaseModel #Nos ayudará a definir facilmente como objetos el contenido de las peticiones, ademas de ayudar con las validaciones
import httpx #Para configurar y administrar los paquetes que enviamos a n8n

#ESTE BACKEND ESTA HECHO EN LENGUAJE PYTHON Y CON EL FRAMEWORK FASTAPI(O CREO QUE ES UNA LIBRERIA, NO ME ACUERDO)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

class SolicitudPrompt(BaseModel):
    contenido: str

class RespuestaChat(BaseModel):
    mensaje: str = "Texto por si falla el mensaje"
    auth: str = "Texto por si falla el auth"

@app.post("/realizar-pregunta")

async def consultarN8n(prompt: SolicitudPrompt):
    n8n_url = "https://igts-jl.app.n8n.cloud/webhook-test/prompt-process"#ESTE LINK ES DE PRUEBA, DEBES ACTIVAR EL WORKFLOW PARA QUE FUNCIONE

    envio = {
        "texto": prompt.contenido,
        "num": 1 
    }

    try:
        async with httpx.AsyncClient() as client :

            respuesta = await client.post(n8n_url, json = envio, timeout = 20.0)

            print(respuesta.status_code)
            print("Todo bien")
            #print(respuesta.respuestaNino)
            #print("Hasta acá está bien")

            respuesta.raise_for_status()
            #print("Hasta acá está bien")
            msg = respuesta.json()
            print("Si se pudo convertir la respuesta a json")
            print(msg)

            #respuestaUsuario = RespuestaChat(mensaje=msg["respuestaNino"], auth = "byJPuffs")

            return RespuestaChat(mensaje=msg["respuestaNino"], auth = "byJPuffs")

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code = e.response.status_code, detail = "Los httpx.HTTPStatusError son errores durante el envio (n8n)")
    except Exception as e:
        raise HTTPException(status_code = 500, detail = "Los Excpetion son errores en la conexión")
    

