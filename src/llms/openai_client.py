import os
import base64
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def _encode_image(caminho_imagem: str) -> str:
    with open(caminho_imagem, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def classificar_com_openai(caminho_imagem: str, modelo: str = "gpt-4o-mini") -> dict:
   
    from .prompt import PROMPT_SISTEMA, PROMPT_USUARIO

    imagem_b64 = _encode_image(caminho_imagem)
    extensao = caminho_imagem.split(".")[-1].lower()
    mime = "image/jpeg" if extensao in ["jpg", "jpeg"] else "image/png"

    resposta = client.chat.completions.create(
        model=modelo,
        messages=[
            {"role": "system", "content": PROMPT_SISTEMA},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": PROMPT_USUARIO},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime};base64,{imagem_b64}"
                        },
                    },
                ],
            },
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
    )

    conteudo = resposta.choices[0].message.content
    try:
        return json.loads(conteudo)
    except json.JSONDecodeError:
        return {"classificacao": "ERRO", "justificativa": conteudo, "confianca": 0.0}