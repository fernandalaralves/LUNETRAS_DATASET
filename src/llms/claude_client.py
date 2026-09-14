import os
import base64
import json

import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)


def _encode_image(caminho_imagem: str) -> str:
    with open(caminho_imagem, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def classificar_com_claude(
    caminho_imagem: str,
    modelo: str = "claude-sonnet-4-5",
    prompt: str = "P1"
) -> dict:
    """
    Classifica uma produção escrita infantil usando Claude.

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

        with open(caminho_imagem, "rb") as f:
            assinatura = f.read(12)

        if assinatura.startswith(b"\x89PNG\r\n\x1a\n"):
            media_type = "image/png"

        elif assinatura.startswith(b"\xff\xd8\xff"):
            media_type = "image/jpeg"

        elif assinatura.startswith(b"RIFF") and assinatura[8:12] == b"WEBP":
            media_type = "image/webp"

        else:
            raise ValueError(
        f"Formato de imagem não suportado: {caminho_imagem}"
    )

        # -----------------------------------------------------
        # 3. Fazer chamada para Claude
        # -----------------------------------------------------

        resposta = client.messages.create(
            model=modelo,
            max_tokens=500,
            system=prompt_sistema,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": imagem_b64
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

        conteudo = resposta.content[0].text

        # -----------------------------------------------------
        # 5. Limpar possíveis blocos Markdown
        # -----------------------------------------------------

        conteudo_limpo = (
            conteudo
            .strip()
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        # -----------------------------------------------------
        # 6. Converter para JSON
        # -----------------------------------------------------

        resultado = json.loads(conteudo_limpo)

        # -----------------------------------------------------
        # 7. Validar campos
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
                "A resposta do Claude não contém "
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
                f"Erro na chamada Claude: {str(e)}"
            ),
            "confianca": 0.0
        }