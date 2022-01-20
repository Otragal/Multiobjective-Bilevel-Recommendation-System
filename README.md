# Sistema de Remendação de Dieta Alimentar Multi-Objetivo

Autor: Vítor de Oliveira Pochmann (Otragal)
Orientador: Fernando Von Zuben


## Sobre

Este trabalho pertence ao projeto de Mestrado deste autor na Faculdade de Engenharia Elétrica e de Computação - Unicamp (2020 - 2022).

Este trabalho é um sistema de recomendação de dieta alimentar multi-objetivo (sistema bi-nível) em que utiliza dois algoritmos *solvers* para encontrar um conjunto de cardápios das refeições diárias (pratos para café da manhã, almoço, jantar e lanche).

A busca sobre encontrar as melhores soluções de cardápios é realizada atráves do método Pareto-Ótimo, pelo algoritmo [NSGA-II](https://ieeexplore.ieee.org/document/996017) com uso de objetivos de cada solução candidata, calculados pelo *solver* [Gurobi](https://www.gurobi.com/).

![Estrutura do Sistema](/home/ancalangon/Pictures/Figura_6.png)

Ambiente de desenvolvimento usado:

- Ubuntu 20.04 GNU Linux 64-bits


## Requisitos

- Python Versão 3.7 ou maior (com ambiente virtual)
- SQLite3 (Banco de Dados)
- [Gurobi Versão 9.1.0](https://www.gurobi.com/)

## Mapa do Repositório

- \root
    - \database (Banco de Dados)
    - \dietprogram (\src do projeto)
        - \app.py (main do projeto)

## Instalação

### Download

Realiza a clonagem `git clone` ou download zip do repositório `master`.

### Prapação do Ambiente

1. Cria um ambiente virtual para este projeto (ou apenas deixe em sua máquina).
2. Baixe as bibliotecas dependendes do projeto com `pip3 install <nome_da_biblioteca>`
    - sqlite3
    - numpy
    - unicodedata
    - matplotlib
    - tkinter
3. Ter o Gurobi e sua licença em sua máquina para usar as bibliotecas:
    - gurobipy

**NOTA**: A versão utilizada da ferramenta Gurobi foi `Gurobi 9.1.0`. É possível baixar esta versão no Site Oficial, mas pode utilizar a ferramenta com a versão mais recente.

### Obtendo Gurobi

Gurobi Solver é uma ferramenta privada da empresa Gurobi Optimization. É possível usar esta ferramenta gratuitamente através da *Licença Acadêmica*. Caso for usar para outros fins, segue os procedimentos no [Site Oficial](https://www.gurobi.com/).

#### Download Gurobi

1. Deve acessar e criar uma conta em visão "Acadêmica" no [Site Oficial do Gurobi Optimization](https://www.gurobi.com/).
2. Baixar a ferramenta Gurobi em [Gurobi Optimizer](https://www.gurobi.com/downloads/gurobi-optimizer-eula/). É possível usar o Gurobi com Anaconda.
    - LINUX (Ubuntu): Existe um guia de instalação feita pela [Unicamp](https://www.ic.unicamp.br/~cid/cursos/MC658/201901/tutorial-pacotes.pdf) ou tem a [Documentação no Site Oficial](https://www.gurobi.com/documentation/9.5/remoteservices/linux_installation.html).
    - WINDOWS 64-bits: Existe um guia de instalação feita pela [Universidade de Missipi](https://it.engr.msstate.edu/wp-content/uploads/2017/12/Gurobi-Installation_2017.pdf) ou tem a [Documentação no Site Oficial] (https://www.gurobi.com/documentation/9.5/remoteservices/windows_installation.html).
    - MAC OS: Tem a [Ducmentação no Site Oficial](https://www.gurobi.com/documentation/9.5/remoteservices/macos_installation.html)

#### Licença do Gurobi

Após a instalação da biblioteca gurobi em sua máquina é necessário ter uma licença.

1. Tendo conta acessada no Site Oficial, inicia a etapa de adquirir a [Academic Licence](https://www.gurobi.com/downloads/end-user-license-agreement-academic/).
2. Aceita as condições e pega a licença.
3. Coloque a licença no diretório padrão do sistema. Clique aqui para ver a [Recomendação de colocar a licença na sua máquina](https://support.gurobi.com/hc/en-us/articles/360013417211-Where-do-I-place-the-Gurobi-license-file-gurobi-lic-).

Em Linux, recomenda-se colocar a licença no diretório em `/opt/gurobi` ou `opt/gurobiXXX` (XXX = numero da versão).

Ainda em Linux, deve criar um `PATH` para que o python entenda que existe a biblioteca Gurobi. Em seu `.bashrc` ou `.profile_bash`, insere estas linhas de código e realiza as alterações necessárias:

```bash
export GUROBI_HOME="/opt/gurobiXXX/linux64"
export PATH="${PATH}:${GUROBI_HOME}/bin"
export LD_LIBRARY_PATH="${GUROBI_HOME}/lib"
export GRB_LICENSE_FILE="/opt/gurobiXXX/linux64/gurobi.lic"
```

