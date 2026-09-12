import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
# DeepSeek usa API compatível com OpenAI
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

def classificar_com_deepseek(texto_extraido: str, modelo: str = "deepseek-chat") -> dict:
    """
    Classifica a produção escrita usando DeepSeek a partir do TEXTO extraído por OCR.
    NÃO recebe imagem diretamente.
    """
    from .prompt import PROMPT_SISTEMA

    prompt = f"""{PROMPT_SISTEMA}

Texto extraído da produção escrita infantil via OCR:
\"\"\"{texto_extraido}\"\"\"

Classifique o nível psicogenético com base nesse texto."""

    resposta = client.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.0,
    )

    conteudo = resposta.choices[0].message.content
    try:
        return json.loads(conteudo)
    except json.JSONDecodeError:
        return {"classificacao": "ERRO", "justificativa": conteudo, "confianca": 0.0}