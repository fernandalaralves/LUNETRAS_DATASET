import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def classificar_com_gemini(
    caminho_imagem: str,
    modelo: str = "models/gemini-flash-lite-latest",
    prompt: str = "P1"
) -> dict:
    """
    Classifica uma produção escrita infantil usando o Gemini.

    Parâmetros:
        caminho_imagem (str):
            Caminho da imagem que será analisada.

        modelo (str):
            Modelo Gemini utilizado.
            Padrão: models/gemini-flash-lite-latest

        prompt (str):
            Prompt utilizado na classificação.
            Pode ser "P1" ou "P2".

    Retorno:
        dict contendo:
            - classificacao
            - justificativa
            - confianca

        Em caso de erro:
            - classificacao = "ERRO"
            - justificativa = mensagem do erro
            - confianca = 0.0
    """

    # ---------------------------------------------------------
    # 1. Selecionar o prompt
    # ---------------------------------------------------------

    if prompt.upper() == "P1":

        from .prompt_P1 import (
            PROMPT_P1_SISTEMA,
            PROMPT_P1_USUARIO
        )

        prompt_completo = (
            PROMPT_P1_SISTEMA
            + "\n\n"
            + PROMPT_P1_USUARIO
        )

    elif prompt.upper() == "P2":

        from .prompt_P2 import (
            PROMPT_P2_SISTEMA,
            PROMPT_P2_USUARIO
        )

        prompt_completo = (
            PROMPT_P2_SISTEMA
            + "\n\n"
            + PROMPT_P2_USUARIO
        )

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
        # 2. Ler a imagem
        # -----------------------------------------------------

        with open(caminho_imagem, "rb") as f:
            img_bytes = f.read()

        # -----------------------------------------------------
        # 3. Identificar o tipo da imagem
        # -----------------------------------------------------

        extensao = caminho_imagem.split(".")[-1].lower()

        if extensao in ["jpg", "jpeg", "png", "webp", "gif"]:

            if extensao in ["jpg", "jpeg"]:
                mime_type = "image/jpeg"
            else:
                mime_type = f"image/{extensao}"

        else:
            mime_type = "image/jpeg"

        # -----------------------------------------------------
        # 4. Montar o conteúdo enviado ao Gemini
        # -----------------------------------------------------

        contents = [
            genai.types.Part.from_bytes(
                data=img_bytes,
                mime_type=mime_type
            ),
            prompt_completo
        ]

        # -----------------------------------------------------
        # 5. Fazer a chamada para o Gemini
        # -----------------------------------------------------

        response = client.models.generate_content(
            model=modelo,
            contents=contents,
            config=genai.types.GenerateContentConfig(
                temperature=0.0,
                response_mime_type="application/json"
            )
        )

        # -----------------------------------------------------
        # 6. Obter a resposta
        # -----------------------------------------------------

        conteudo = response.text

        # -----------------------------------------------------
        # 7. Limpar possíveis blocos Markdown
        # -----------------------------------------------------

        conteudo_limpo = (
            conteudo
            .strip()
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        # -----------------------------------------------------
        # 8. Converter a resposta para JSON
        # -----------------------------------------------------

        resultado = json.loads(conteudo_limpo)

        # -----------------------------------------------------
        # 9. Validar os campos retornados
        # -----------------------------------------------------

        classificacao = resultado.get("classificacao")
        justificativa = resultado.get("justificativa")
        confianca = resultado.get("confianca")

        if classificacao is None:
            raise ValueError(
                "A resposta do Gemini não contém "
                "o campo 'classificacao'."
            )

        if justificativa is None:
            justificativa = ""

        if confianca is None:
            confianca = 0.0

        # -----------------------------------------------------
        # 10. Retornar resultado padronizado
        # -----------------------------------------------------

        return {
            "classificacao": classificacao,
            "justificativa": justificativa,
            "confianca": float(confianca)
        }

    except Exception as e:

        # -----------------------------------------------------
        # 11. Registrar erro da API
        # -----------------------------------------------------

        return {
            "classificacao": "ERRO",
            "justificativa": (
                f"Erro na chamada Gemini: {str(e)}"
            ),
            "confianca": 0.0
        }