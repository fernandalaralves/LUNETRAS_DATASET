# Protocolo de Coleta de Dados

## 1. Objetivo

Descrever os procedimentos utilizados para coleta das produções
escritas infantis que irão compor o dataset destinado ao
desenvolvimento do sistema de classificação do nível psicogenético
da escrita.

## 2. Participantes

Descrever:
- público-alvo;
- faixa etária;
- escolaridade/ano;
- quantidade esperada de participantes;
- contexto da coleta.

Os participantes deverão ser identificados por códigos anônimos
(C001, C002, C003...), não por seus nomes.

## 3. Atividade de escrita

Descrever exatamente o que será solicitado à criança.

Exemplo:
- escrita de palavras;
- escrita de frases;
- escrita espontânea;
- ditado;
- outras atividades.

Registrar também quais palavras/frases serão utilizadas.

## 4. Procedimento de coleta

Descrever passo a passo:

1. Entregar a atividade à criança.
2. Explicar a atividade de acordo com o protocolo.
3. Solicitar a produção escrita.
4. Registrar a produção.
5. Fotografar a folha.
6. Associar a imagem ao identificador anônimo da criança.
7. Registrar os metadados.

## 5. Registro das imagens

Formato:
- PNG ou JPG
- resolução mínima: [definir]
- orientação: [definir]
- iluminação: [definir]
- evitar sombras e reflexos
- folha inteira visível
- câmera paralela à folha, quando possível

## 6. Identificação dos arquivos

Padrão:

C001_T001_IMG001.jpg

Onde:
- C001 = participante (child_id)
- T001 = atividade (task_id)
- IMG001 = identificação da imagem (image_id)

 O campo `filename` no dataset.csv deve ser idêntico a este nome de arquivo.
 O campo `image_id` é o identificador lógico (ex: IMG001) e pode ser 
   usado em relatórios sem o prefixo Cxxx_Txxx.

## 7. Metadados

Para cada produção, registrar:

- ID da imagem
- ID anonimizado da criança
- atividade
- idade/faixa etária, se necessário
- ano escolar
- data da coleta, se necessário
- observações relevantes

## 8. Armazenamento

As imagens originais devem ser armazenadas em:

data/raw/

Os dados processados devem ser armazenados em:

data/processed/

## 9. Privacidade e segurança

Não armazenar no dataset:
- nome da criança;
- CPF;
- endereço;
- outras informações pessoais desnecessárias.

As imagens devem ser utilizadas de acordo com as autorizações
e procedimentos éticos definidos para a pesquisa.

## 10. Controle de qualidade

Antes de uma imagem entrar no dataset, verificar:

- [ ] imagem legível
- [ ] escrita completamente visível
- [ ] iluminação adequada
- [ ] sem desfoque excessivo
- [ ] identificação correta
- [ ] atividade corretamente registrada