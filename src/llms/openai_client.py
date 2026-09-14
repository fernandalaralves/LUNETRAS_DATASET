import os
import base64
import json

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def _encode_image(caminho_imagem: str) -> str:
    with open(caminho_imagem, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def classificar_com_openai(
    caminho_imagem: str,
    modelo: str = "gpt-4o-mini",
    prompt: str = "P1"
) -> dict:
    """
    Classifica uma produção escrita infantil usando a OpenAI.

    prompt:
        "P1" ou "P2"

    Retorno:
        {
            "classificacao": ...,
            "justificativa": ...,
            "confianca": ...
        }
    """

    # ---------------------------------------------------------
    # 1. Selecionar o prompt
    # ---------------------------------------------------------

    if prompt.upper() == "P1":

        from .prompt_P1 import (
            PROMPT_P1_SISTEMA,
            PROMPT_P1_USUARIO
        )

        prompt_sistema = PROMPT_P1_SISTEMA
        prompt_usuario = PROMPT_P1_USUARIO

    elif prompt.upper() == "P2":

        from .prompt_P2 import (
            PROMPT_P2_SISTEMA,
            PROMPT_P2_USUARIO
        )

        prompt_sistema = PROMPT_P2_SISTEMA
        prompt_usuario = PROMPT_P2_USUARIO

    else:

        return {
            "classificacao": "ERRO",
            "justificativa": (
                f"Prompt inválido: '{prompt}'. "
                "Use 'P1' ou 'P2'."
            ),
            "confianca": 0.0
        }

    try:

        # -----------------------------------------------------
        # 2. Ler imagem
        # -----------------------------------------------------

        imagem_b64 = _encode_image(caminho_imagem)

        extensao = caminho_imagem.split(".")[-1].lower()

        if extensao in ["jpg", "jpeg"]:
            media_type = "image/jpeg"
        elif extensao == "png":
            media_type = "image/png"
        elif extensao == "webp":
            media_type = "image/webp"
        else:
            media_type = "image/jpeg"

        # -----------------------------------------------------
        # 3. Fazer chamada para OpenAI
        # -----------------------------------------------------

        resposta = client.chat.completions.create(
            model=modelo,
            temperature=0.0,
            response_format={
                "type": "json_object"
            },
            messages=[
                {
                    "role": "system",
                    "content": prompt_sistema
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": (
                                    f"data:{media_type};"
                                    f"base64,{imagem_b64}"
                                )
                            }
                        },
                        {
                            "type": "text",
                            "text": prompt_usuario
                        }
                    ]
                }
            ]
        )

        # -----------------------------------------------------
        # 4. Obter resposta
        # -----------------------------------------------------

        conteudo = resposta.choices[0].message.content

        # -----------------------------------------------------
        # 5. Converter para JSON
        # -----------------------------------------------------

        resultado = json.loads(conteudo)

        # -----------------------------------------------------
        # 6. Validar campos
        # -----------------------------------------------------

        classificacao = resultado.get("classificacao")

        justificativa = resultado.get(
            "justificativa",
            ""
        )

        confianca = resultado.get(
            "confianca",
            0.0
        )

        if classificacao is None:
            raise ValueError(
                "A resposta da OpenAI não contém "
                "o campo 'classificacao'."
            )

        return {
            "classificacao": classificacao,
            "justificativa": justificativa,
            "confianca": float(confianca)
        }

    except Exception as e:

        return {
            "classificacao": "ERRO",
            "justificativa": (
                f"Erro na chamada OpenAI: {str(e)}"
            ),
            "confianca": 0.0
        }