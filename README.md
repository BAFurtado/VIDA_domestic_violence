#### Análise crimininalidade e violência com modelos baseados em agentes -- ABMs

"Traditionally, researchers have employed statistical methods to model crime. However, these approaches
are limited by being unable to model individual actions and behaviour. ... [a model should] attempt to model
the occurrence of crimes and motivations behind it. ... **explore the potential of the model to realistically
simulate the main processes and drivers within this system**." (Malleson, Heppenstall, See, 2009).  

We developed the model on top of [https://github.com/projectmesa/mesa] mesa wolf_sheep example
We thank David Massa e all the contributors of the mesa project. 

**Alan Rafael Dill**

**Lígia Mori Madeira**

**Bernardo Alves Furtado**

We are considering two models: 

### 1. Home violence model

An exploratory **stay-at-home-COVID-increased-violence** model. *Under construction*

See folder `home_violence`

1. A partir de um indicador de **stress** dos agentes, baseados em fatores tais como: gênero, histórico de agressões
salário, horas em casa e número de membros na família; maior probabilidade de agressão.
2. Entidades: pessoas (adultos, crianças, famílias)
3. Alterações nos estados: trabalha/não trabalho, salário (0, 1), número de horas em casa
4. Perguntas: 

4.1 Em que medida o aumento do número de dias em casa aumenta a violência doméstica e os feminicídios?

4.2 Em que medida o não acesso à rede de proteção amplia a violência doméstica e os feminicídios?

### 2. Gun-reaction model

See folder `guns_model`

1. A partir do modelo simples, descrito em Proposta.docx, construímos três classes de agentes.
2. Vítimas, Agressores e Policiais
3. Todos movem-se aleatoriamente pelo grid
4. 1. Quando Agressor se encontra com vítima(s), escolhe uma para confrontar
   2. Se há policial na vizinhança imediata (uma célula, Moore), há confronto, determinado pela letalidade policial (parâmetro do modelo)
        1. Ou agressor ou policial morrem.
   3. Quando não há policial, agressor confronta vítima
        1. Se vítima possui arma
            1. Se há reação da vítima, 
                1. Morre vítima ou agressor  

## To run the models:
#### Para rodar os modelos, desde a instalação inicial

1. Preferencialmente, download e instale Python, via [https://www.anaconda.com/distribution] conda. No mínimo, tenha Pyton3 instalado
2. Preferencialmente, download e instale uma IDE. Sugiro [https://www.jetbrains.com/pycharm/download/] PyCharm Community. Universitários tem acesso à versão profissional, basta cadastro com e-mail institucional. 
3. Donwload e instale [https://git-scm.com/downloads] [GIT].
4. Com todos funcionando, vá até o Terminal do PyCharm (ou command line com acesso a Python) e usando o Git, clone esse repositório:
    1. `git clone https://github.com/BAFurtado/armas.git`  
    2. `pip install mesa`
    
#### To actually run
5. Utilize o comando `cd` para que o Terminal esteja no diretorio correto: 
    1. `cd ~/mesa_guns/guns_model` directory OU `cd ~/mesa_guns/home_violence`
    2. Type `mesa runserver` e pronto. Se tudo foi instalado, o browser se abriu automaticamente. 
    3. Altere os parâmetros como quiser.
    4. Clique em `Reset` no último botão à direita, na barra preta ao alto.
    5. Clique em `Start`, à esquerda do `Reset'
    
Enjoy modeling!
