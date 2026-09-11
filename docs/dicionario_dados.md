## Dicionário de dados

# 1 Objetivo:
Este documento descreve os campos utilizados para armazenar os metadados das produções escritas que irão compor o dataset do projeto.

# 2 Arquivo dataset.csv

O arquivo dataset.csv contém uma linha para cada produção escrita registrada no dataset.

## Estrutura inicial
# Campo	     Tipo	        Obrigatório	    Descrição	                                                Exemplo
image_id	 texto	        Sim	            Identificador único da imagem	                            IMG0001
filename	 texto	        Sim	            Nome do arquivo da imagem	                                IMG0001.jpg
child_id	 texto	        Sim        	    Identificador anonimizado da criança	                    C001
task_id	     texto	        Sim	            Identificador da atividade realizada	                    T001
label	     categórico	    Sim	            Nível psicogenético atribuído à produção	                SILABICO
annotator	 texto	        Sim	            Identificador do avaliador responsável pela anotação	    A001
split	     categórico	    Não	            Conjunto utilizado para treinamento, validação ou teste     train
age	         numérico	    A definir	    Idade da criança no momento da coleta	                    6
school_year	 texto	        A definir	    Ano/série escolar da criança	                            1º ano
observation	 texto	        Não	            Observações relevantes sobre a produção	                    Produção parcialmente ilegível


## 3 Descrição dos campos:
# 3.1 image_id

Identificador único atribuído a cada imagem do dataset.

O identificador não deve conter informações pessoais da criança.

Formato sugerido:

IMG0001
IMG0002
IMG0003

Exemplo:

IMG0025

# 3.2 filename

Nome do arquivo correspondente à imagem armazenada no dataset.

Exemplo:

IMG0025.jpg

O nome do arquivo deve corresponder ao image_id para facilitar a associação entre os metadados e a imagem.

# 3.3 child_id

Identificador anonimizado da criança responsável pela produção.

Não devem ser utilizados nomes ou outras informações que permitam identificar diretamente a criança.

Formato sugerido:

C001
C002
C003

Exemplo:

C017

O mesmo child_id deve ser utilizado para todas as produções da mesma criança.

# 3.4 task_id

Identificador da atividade de escrita realizada pela criança.

Cada tipo de atividade deve receber um identificador próprio.

Exemplo:

T001
T002
T003

A descrição detalhada de cada atividade deverá ser mantida na documentação do protocolo de coleta.

Exemplo:

T001 = atividade de escrita de palavras
T002 = atividade de escrita de frase
T003 = produção escrita espontânea

Os tipos de atividade ainda deverão ser definidos pela equipe do projeto.

# 3.5 label

Classificação correspondente ao nível psicogenético identificado na produção escrita.

Inicialmente, estão previstas quatro categorias:

PRE_SILABICO
SILABICO
SILABICO_ALFABETICO
ALFABETICO

Exemplo:

SILABICO_ALFABETICO

Os critérios utilizados para atribuição de cada classe devem estar documentados em docs/anotacao.md.

# 3.6 annotator

Identificador do avaliador responsável pela classificação da produção.

Os avaliadores devem ser identificados por códigos, evitando o armazenamento desnecessário de nomes pessoais no dataset.

Formato sugerido:

A001
A002
A003

Exemplo:

A002

Quando houver mais de um avaliador, os códigos deverão permitir identificar qual avaliador realizou cada anotação.

# 3.7 split

Indica em qual subconjunto a produção será utilizada durante os experimentos de aprendizado de máquina.

Valores possíveis:

train
validation
test
train

Dados utilizados durante o treinamento do modelo.

validation

Dados utilizados para acompanhar o desempenho durante o desenvolvimento e ajuste do modelo.

test

Dados utilizados para a avaliação final do modelo.

Regra importante

A divisão deverá considerar o child_id, evitando que produções da mesma criança sejam distribuídas simultaneamente entre treinamento e teste.

Exemplo recomendado:

C001 → train
C002 → train
C003 → validation
C004 → test

Evitar:

C001 → train
C001 → test

Essa separação é necessária para reduzir o risco de vazamento de dados (data leakage) entre os conjuntos.

# 3.8 age

Idade da criança no momento da realização da atividade.

Tipo:

numérico

Exemplo:

6

A utilização desse campo deverá ser definida de acordo com os objetivos da pesquisa e as questões relacionadas à privacidade dos participantes.

Caso a idade exata não seja necessária, pode ser utilizada uma faixa etária.

Exemplo:

6-7
# 3.9 school_year

Ano ou série escolar da criança no momento da coleta.

Exemplos:

1º ano
2º ano

Esse campo deverá ser utilizado somente se for relevante para a pesquisa e estiver de acordo com o protocolo definido pela equipe.

# 3.10 observation

Campo destinado a registrar observações relevantes sobre a imagem ou sobre o processo de anotação.

Exemplos:

Produção parcialmente ilegível.
Imagem apresenta sombra na parte inferior da folha.
Classificação revisada após discordância entre avaliadores.

Esse campo não deve ser utilizado para armazenar informações pessoais desnecessárias.

## 4. Arquivo labels.csv

O arquivo labels.csv deverá armazenar a definição das classes utilizadas na classificação.

Estrutura inicial:
# Campo	Tipo	    Descrição	                                Exemplo
label_id	        inteiro	Identificador numérico da classe	0
label_name	texto	Nome da classe	                            PRE_SILABICO
description	texto	Descrição da classe	                        Descrição definida no protocolo de anotação

# Exemplo:
label_id,label_name,description
0,PRE_SILABICO,"Descrição a definir"
1,SILABICO,"Descrição a definir"
2,SILABICO_ALFABETICO,"Descrição a definir"
3,ALFABETICO,"Descrição a definir"

As descrições definitivas deverão ser estabelecidas com base na fundamentação teórica adotada no projeto e no protocolo de anotação.

# 5. Arquivo tasks.csv

Caso o projeto utilize diferentes atividades de escrita, recomenda-se criar um arquivo tasks.csv para documentá-las.

Estrutura:
# Campo	Tipo	    Descrição	                Exemplo
task_id	texto	    Identificador da atividade	T001
task_name	texto	Nome da atividade	        Escrita de palavras
description	texto	Descrição da atividade	    Produção escrita a partir de palavras apresentadas

# Exemplo:
task_id,task_name,description
T001,"Escrita de palavras","Descrição a definir"
T002,"Escrita de frase","Descrição a definir"
T003,"Escrita espontânea","Descrição a definir"

As atividades definitivas ainda deverão ser definidas pela equipe.


## 6. Regras gerais dos dados
# 6.1 Identificação

Os identificadores devem ser únicos dentro de sua categoria.

Exemplo:

C001
C002
C003

# 6.2 Anonimização

Os dados utilizados no dataset não devem conter informações pessoais desnecessárias que permitam identificar diretamente os participantes.

Os identificadores utilizados no projeto devem ser códigos anônimos.

# 6.3 Valores ausentes

Quando uma informação não estiver disponível, deverá ser utilizado um padrão único definido pela equipe.

Sugestão:

NA

Exemplo:

IMG001,img001.jpg,C001,T001,SILABICO,A001,train,NA,1º ano,

Não utilizar diferentes representações para a mesma situação, como:

N/A
na
-
vazio
não informado

A equipe deverá escolher um único padrão.

# 6.4 Padronização das classes

Os nomes das classes devem ser escritos exatamente conforme definidos em labels.csv.

Utilizar:

PRE_SILABICO
SILABICO
SILABICO_ALFABETICO
ALFABETICO

Evitar variações como:

Pré-silábico
pre silabico
pre_silabico
Silábico
silabico-alfabetico

A padronização reduz problemas durante o processamento automático dos dados.

## 7. Exemplo completo

Um exemplo hipotético de dataset.csv:

image_id,filename,child_id,task_id,label,annotator,split,age,school_year,observation
IMG0001,IMG0001.jpg,C001,T001,PRE_SILABICO,A001,train,6,"1º ano",
IMG0002,IMG0002.jpg,C001,T002,SILABICO,A001,train,6,"1º ano",
IMG0003,IMG0003.jpg,C002,T001,SILABICO_ALFABETICO,A002,train,7,"1º ano",
IMG0004,IMG0004.jpg,C003,T001,ALFABETICO,A001,validation,7,"2º ano",
IMG0005,IMG0005.jpg,C004,T002,SILABICO,A002,test,6,"1º ano","Classificação revisada"

Os dados acima são apenas exemplos fictícios e não representam dados reais da pesquisa.


# 8. Campos que ainda precisam ser definidos


-Quantidade de participantes

-Tipos de atividades de escrita

-Quantidade de produções por criança

-Formato das imagens

-Resolução mínima das imagens

-Metadados que serão coletados

-Critérios definitivos das classes

-Quantidade de avaliadores

-Procedimento para casos de discordância

-Estratégia de divisão entre train, validation e test

-Política de armazenamento e acesso às imagens

-Procedimentos relacionados à autorização e privacidade dos participantes

## 9. Arquivos relacionados

Este documento deve ser utilizado em conjunto com:

docs/
├── protocolo_coleta.md
├── anotacao.md
└── dicionario_dados.md
protocolo_coleta.md → define como os dados são coletados.
anotacao.md → define como as produções são classificadas.
dicionario_dados.md → define como as informações são armazenadas e padronizadas.