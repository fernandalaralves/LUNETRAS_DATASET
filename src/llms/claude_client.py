import os
import base64
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def _encode_image(caminho_imagem: str) -> str:
    with open(caminho_imagem, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def classificar_com_claude(caminho_imagem: str, modelo: str = "claude-sonnet-4-5") -> dict:    
    from .prompt import PROMPT_SISTEMA, PROMPT_USUARIO

    imagem_b64 = _encode_image(caminho_imagem)
    extensao = caminho_imagem.split(".")[-1].lower()
    media_type = "image/jpeg" if extensao in ["jpg", "jpeg"] else "image/png"

    resposta = client.messages.create(
        model=modelo,
        max_tokens=500,
        temperature=0.0,
        system=PROMPT_SISTEMA,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": imagem_b64,
                        },
                    },
                    {"type": "text", "text": PROMPT_USUARIO},
                ],
            }
        ],
    )

    conteudo = resposta.content[0].text
    # Claude pode envolver o JSON em markdown, então limpamos
    conteudo_limpo = conteudo.strip().replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(conteudo_limpo)
    except json.JSONDecodeError:
        return {"classificacao": "ERRO", "justificativa": conteudo, "confianca": 0.0}