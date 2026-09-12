import os
import time
import pandas as pd
from tqdm import tqdm
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

from .openai_client import classificar_com_openai
from .claude_client import classificar_com_claude
from .deepseek_client import classificar_com_deepseek

CLASSES = ["PRE_SILABICO", "SILABICO", "SILABICO_ALFABETICO", "ALFABETICO"]

def avaliar_llm(df: pd.DataFrame, pasta_imagens: str, funcao_llm, nome_llm: str,
                precisa_ocr: bool = False, ocr_func=None) -> pd.DataFrame:
    """
    Roda um LLM em todas as imagens do dataframe e retorna resultados.
    """
    resultados = []
    for _, linha in tqdm(df.iterrows(), total=len(df), desc=nome_llm):
        caminho = os.path.join(pasta_imagens, linha["filename"])
        try:
            if precisa_ocr:
                texto = ocr_func(caminho)
                saida = funcao_llm(texto)
            else:
                saida = funcao_llm(caminho)

            resultados.append({
                "image_id": linha["image_id"],
                "label_real": linha["label"],
                "label_predito": saida.get("classificacao", "ERRO"),
                "justificativa": saida.get("justificativa", ""),
                "confianca": saida.get("confianca", 0.0),
                "llm": nome_llm,
            })
        except Exception as e:
            resultados.append({
                "image_id": linha["image_id"],
                "label_real": linha["label"],
                "label_predito": "ERRO",
                "justificativa": str(e),
                "confianca": 0.0,
                "llm": nome_llm,
            })
        time.sleep(0.5)  # evitar rate limit
    return pd.DataFrame(resultados)

def calcular_metricas(df_resultados: pd.DataFrame) -> dict:
    """Calcula acurácia, F1 macro e matriz de confusão."""
    y_true = df_resultados["label_real"]
    y_pred = df_resultados["label_predito"]
    return {
        "acuracia": accuracy_score(y_true, y_pred),
        "f1_macro": f1_score(y_true, y_pred, average="macro", labels=CLASSES, zero_division=0),
        "matriz_confusao": confusion_matrix(y_true, y_pred, labels=CLASSES).tolist(),
    }