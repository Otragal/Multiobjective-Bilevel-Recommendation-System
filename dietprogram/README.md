# dietprogram

Aqui é a pasta principal do projeto. É onde tudo acontece.

## Descrição de Cada Arquivo

| Arquivo | Descrição |
| --- | --- |
| app.py | Principal Arquivo para Iniciar o Programa |
| database.py | Comunicação com Banco de Dados |
| filtros.py |  Dataclass de Filtros para Usuário |
| fitnessGurobi.py | Classe que atualiza os Objetivos do Indivíduo |
| formatConverter.py | Classe que converte os dados do cromossomo do Indivíduo para modelo Gurobi |
| ga.py | Classe que inicializa o NSAG-II |
| genetic.py | Classe que contém todas funcionalidades e operações do NSGA-II |
| gurobyModel.py | Classe da estrutura do modelo Gurobi - Programação Linear Mono Objetivo |
| individuo.py | Classe da estrutura do Indivíduo do NSGA-II (INCOMPLETO) |
| interface.py | GUI do Programa - Segundo Arquivo Principal para Iniciar o Programa |
| macro.py | Classe que armazena as informações do usuário e do banco de dados. PACOTE |
| povo.py | Classe da estrutura do Povo do NSGA-II |
| TESTE.py | Arquivo para testar o programa todo |
| TESTE2.py | Arquivo para gerar gráficos na hora de testar as equações dos objetivos |

## Fluxo de Informação

Inicializa o App (app.py) pelo comando

> python3 app.py

1. App inicia
    - App recebe os dados do usuário
    - Se houver filtros, ele chama o Filtros (filtros.py)
    - App chama o Macro (macro.py) [2]
    - App chama o GA (ga.py) [4]
2. Macro quarda os dados do usuário
    - Chama o Database (database,py) [3]
    - Armazena os dados do banco de dados
3. Database recebe os pedidos do Macro
    - Comunica com o Banco de Dados
    - Entrega os dados ao macro
4. GA recebe o macro
    - Pega o Macro com os dados armazenados
    - Cria o Primeiro Povo do algoritmo NSGA-II, chamando Povo (povo.py) [6]
    - Inicializa o NSGA-II, chamando o Genetic (genetic.py) [5]
    - Recebe os resultados do Genetic
    - Printa os resultados
5. Genetic realiza o algoritmo NSGA-II
    - Utiliza seus métodos para operar sua busca
    - Cria os filhos da População Atual, chamando seus métodos e outras classes [8] [7] [6] [4] 
    - Chama FitnessGurobi (fitnessGurobi.py) [8] para calcular os objetivos dos indivíduos 
    - Realia o algoritmo NSGA-II até chegar o método de parada e retornar os resultados para o GA
6. Povo é chamado tanto no GA quanto no Genetic
    - Ele cria os individuos, chamando o Indivíduo (individuo.py) [7]
    - Dependendo da chamada, ele altera a lista individuos e os indivíduos
7. Indivíduo é chamado tanto no Genetic quanto no Povo
    - Responsável em criar o cromossommo do Indivíduo e alterar seu valor fitness (Objetivos)
8. FitnessGurobi é chamado tanto no Genetic quanto no GA
    - Ele realiza a operação de inserir os objetivos dos indivíduos do NSGA-II
    - Chama o FormatConverter (formatConverter.py) [9] para converter os dados do cromossomo
    - Chama o GurobyModel (gurobyModel.py) [10] para realizar o calculo do Programação Linear Mono-Objetivo
    - Recebe o objetivo do NSGA-II "Custo", trazido pelo GurobyModel
    - Calcula o segundo objetivo do NSGA-II "Desempenho"
9. FormatConverter é chamado pelo FitnessGurobi
    - Reponsável em converter os dados do cromossomo para o modelo Gurobi poder ler estes dados
10. GurobyModel é chamado pelo FitnessGurobi
    - Recebe todos os parametros necesśarios para criar o modelo matemético
    - Calcula e retorna os resultados