# Changelog

All notable changes to this project and the learning process will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 2025-07-01 &ensp; \</~fmn>
### Configuração

- instalação do WSL, configuração de ambiente e clone do repositório.

## 2025-08-01 &ensp; \</~fmn>
### Pesquisa

- entender como o código se estrutura; 
- estudo de alguns conceitos como:
    - navegação autônoma, algoritmos de busca e otimização, métodos de navegação;
        - [Planning Algorithms - Steven M. LaValle](https://msl.cs.uiuc.edu/planning/bookbig.pdf)
        - [Path Planning in Dynamic Environments](https://thesai.org/Downloads/Volume5No8/Paper_13-Path_Planning_in_a_Dynamic_Environment.pdf)
    - controle, otimização para sistemas de múltiplos agentes, estratégias de evasão e comportamento colaborativo;
        - [Optimal Control Theory - Donald E. Kirk.](http://e.guigon.free.fr/rsc/book/Kirk04.pdf)
        - [Control Theory for Dummies](https://medium.com/lifeandtech/control-theory-for-dummies-e86155b14aff)
        - [Multi-Agent Systems: Algorithmic, Game-Theoretic, and Logical Foundations - Shoham & Leyton-Brown.](https://www.masfoundations.org/mas.pdf)
    - aprendizado por reforço;
        - [Reinforcement Learning: An Introduction - Sutton & Barto.](https://web.stanford.edu/class/psych209/Readings/SuttonBartoIPRLBook2ndEd.pdf)
    - documentação do gymnasium e rsoccer_gym.
    
### Plano de ação

1. estudo teórico com foco em navegação autônoma e controle de agentes;
2. entender como os robôs interagem no ambiente;
3. pesquisa de soluções para análise de estratégias;
4. implementação incremental;
5. testes;
6. documentação e comparação de resultados.

## 2025-09-01 &ensp; \</~fmn>
### Implementação

- Entendimento da integração sslenv.py / base_agent.py / agent.py;
- Lidando com o 1º desafio:
    - Implementação de "Avoidance behavior"
        - Agente ainda colide com obstáculos mas já da pra notar que tenta desviar;
        - Talvez a velocidade esteja interferindo no movimento de desvio do agente em relação aos obstáculos.