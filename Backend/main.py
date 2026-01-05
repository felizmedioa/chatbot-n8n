from fastapi import FastAPI #Lo principal de fastapi
from fastapi.middleware.cors import CORSMiddleware #Nos ayudará a configurar el CORS y los permisos
from pydantic import BaseModel #Nos ayudará a definir facilmente como objetos el contenido de las peticiones, ademas de ayudar con las validaciones

app = FastAPI();

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
);

class SolicitudPrompt(BaseModel):
    contenido: str;

class RespuestaChat(BaseModel):
    mensaje: str
    auth: str

@app.post("/realizar-pregunta")
def recibir_Prompt(prompt: SolicitudPrompt):
    return RespuestaChat(mensaje="Prompt Recibido con Exito", auth = "byJPuffs")