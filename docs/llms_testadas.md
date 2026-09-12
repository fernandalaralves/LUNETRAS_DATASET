# LLMs Testados

## 1. Objetivo

Comparar o desempenho de Modelos de Linguagem de Grande Escala (LLMs) 
multimodais na classificação do nível psicogenético da escrita infantil, 
utilizando o mesmo prompt e o mesmo conjunto de imagens anotadas.

A comparação é feita entre três LLMs comerciais e serve como *baseline* 
para o modelo supervisionado treinado pela equipe (ResNet/ViT), que é a 
contribuição principal do trabalho.

## 2. Modelos utilizados

| LLM | Modelo | Modalidade | Aceita imagem? | Custo |
|-----|--------|------------|----------------|-------|
| OpenAI | gpt-4o-mini | Multimodal | Sim | Pago (com cota gratuita) |
| Anthropic | claude-3-5-sonnet | Multimodal | Sim | Pago (com cota gratuita) |
| DeepSeek | deepseek-chat | Texto | Não (usa OCR) | Pago (com cota gratuita) |

>  **Nota sobre o DeepSeek:** A API oficial do DeepSeek (`api.deepseek.com`) 
> **não processa imagens nativamente**, aceitando apenas texto. Para incluí-lo 
> na comparação, foi necessário aplicar OCR (Tesseract) previamente para 
> extrair o texto da produção escrita e, em seguida, enviar esse texto ao 
> modelo. Essa adaptação é uma limitação da comparação e deve ser considerada 
> na interpretação dos resultados.

## 3. Prompt utilizado

Foi utilizado o mesmo prompt para os três modelos, com o objetivo de garantir 
comparação justa. O prompt define o papel do modelo como especialista em 
psicogênese da língua escrita (Ferreiro & Teberosky) e solicita a 
classificação em uma das quatro categorias:

- `PRE_SILABICO`
- `SILABICO`
- `SILABICO_ALFABETICO`
- `ALFABETICO`

A saída é solicitada em formato JSON estruturado, contendo:
- `classificacao`
- `justificativa`
- `confianca` (0.0 a 1.0)

Para OpenAI e Claude, a imagem foi enviada diretamente (base64). Para o 
DeepSeek, o texto extraído via OCR foi enviado no lugar da imagem.

## 4. Conjunto de teste

Foi utilizada uma amostra de **17 imagens** do dataset, anotadas manualmente 
por um avaliador (A001), com a seguinte distribuição:

| Classe | Quantidade |
|--------|-----------|
| PRE_SILABICO | 3 |
| SILABICO | 11 |
| SILABICO_ALFABETICO | 3 |
| ALFABETICO | 0 |
| **Total** | **17** |

>  **Limitação:** O dataset apresenta desbalanceamento significativo 
> (64,7% das imagens na classe SILABICO) e **ausência de exemplos da classe 
> ALFABETICO**. Isso impacta diretamente a avaliação dos modelos, 
> tornando a acurácia uma métrica enganosa (um classificador que sempre 
> prevê SILABICO já acerta 64,7%). Por isso, utiliza-se também o **F1-macro**.

## 5. Métricas de avaliação

- **Acurácia:** proporção de acertos (limitada pelo desbalanceamento).
- **F1-macro:** média do F1-Score de cada classe, dando peso igual a todas 
  as classes — mais adequado para datasets desbalanceados.
- **Matriz de confusão:** para analisar quais classes os modelos confundem.


## 6. Resultados

| LLM | Acurácia | F1-macro |
|-----|----------|----------|
| OpenAI gpt-4o-mini | 0,118 | 0,083 |
| Claude Sonnet 4.5 | 0,059 | 0,071 |
| Baseline aleatório | 0,250 | 0,250 |

### Matriz de Confusão — OpenAI gpt-4o-mini

PRE SIL SIL-ALF ALF
PRE_SILABICO [0, 0, 3, 0]
SILABICO [0, 1, 5, 0]
SIL-ALFABETICO [0, 0, 1, 0]
ALFABETICO [0, 0, 0, 0]

### Matriz de Confusão — Claude Sonnet 4.5
PRE SIL SIL-ALF ALF
PRE_SILABICO [0, 1, 0, 2]
SILABICO [0, 0, 3, 8]
SIL-ALFABETICO [1, 0, 1, 1]
ALFABETICO [0, 0, 0, 0]



> Inserir as matrizes geradas pelo notebook para cada LLM.

## 7. Análise qualitativa

Além das métricas quantitativas, as **justificativas** geradas por cada LLM 
foram analisadas qualitativamente, buscando identificar:

- Se o modelo reconhece os indicadores descritos no protocolo de anotação 
  (ex: "uma letra por sílaba" para SILABICO).
- Se há viés pedagógico (ex: confundir níveis próximos).
- Se a confiança declarada (`confianca`) é coerente com o acerto/erro.

## 8. Limitações

- **Amostra pequena:** 17 imagens é insuficiente para conclusões estatísticas robustas.
- **Desbalanceamento:** 64,7% em SILABICO e nenhuma imagem ALFABETICO.
- **Prompt zero-shot:** não foram testadas variações (few-shot, chain-of-thought).
- **DeepSeek sem visão:** depende do OCR, que tem limitações para escrita infantil.
- **Ausência de múltiplos anotadores:** apenas A001 anotou, sem dupla checagem.
- **Sem avaliação de reprodutibilidade:** uma única execução por modelo.

## 9. Considerações éticas

- As imagens são produções escritas infantis anonimizadas.
- Nenhum dado pessoal (nome, CPF, endereço) foi enviado às APIs.
- As políticas de retenção de dados da OpenAI, Anthropic e DeepSeek devem 
  ser verificadas e citadas no artigo.
- O uso de APIs comerciais para análise de produções infantis levanta 
  questões sobre privacidade que devem ser discutidas.

## 10. Arquivos gerados

Os resultados brutos são armazenados em:
data/llm_results/
├── openai/resultados.csv
├── claude/resultados.csv
├── deepseek/resultados.csv
└── comparativo_llms.csv

Cada arquivo contém:

- `image_id`
- `label_real` (anotação humana)
- `label_predito` (classificação do LLM)
- `justificativa`
- `confianca`
- `llm`

## 11. Arquivos relacionados

- `docs/anotacao.md` — protocolo de classificação
- `docs/dicionario_dados.md` — estrutura dos dados
- `docs/protocolo_coleta.md` — coleta das imagens
- `notebooks/05_testes_llms.ipynb` — notebook de execução
- `src/llms/` — código dos clientes das APIs