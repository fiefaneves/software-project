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

## 2025-10-01 &ensp; \</~fmn>
### Implementação 

- Para melhorar o funcionamento, seria útil implementar:
    1. Um campo potencial mais sofisticado para lidar com múltiplos obstáculos.
    2. Uma estratégia de planejamento de caminho global (como A* ou RRT) para evitar situações de bloqueio.
    3. Suavização usando um filtro (por exemplo, Kalman) para o vetor de evitação.

### Dúvidas

- #1 Campo Potencial
    - A atração até o target já está implementada em Navigation.py?
    - Caso esteja, a repulsão dos obstáculos deveria ser implementada lá também?
    - E no agent.py apenas chamar a repulsão caso algum obstáculo esteja muito perto?

## 2025-13-01 &ensp; \</~fmn>
### Pesquisa
- [PythonRobotics](https://github.com/AtsushiSakai/PythonRobotics?tab=readme-ov-file#path-planning)
        - [The Dynamic Window Approach to Collision Avoidance](https://www.ri.cmu.edu/pub_files/pub1/fox_dieter_1997_1/fox_dieter_1997_1.pdf)
        - [Robotic Motion Planning:Potential Functions](https://www.cs.cmu.edu/~motionplanning/lecture/Chap4-Potential-Field_howie.pdf)

- Potencial Field:
    - [Path Planning Using Potential Field Algorithm](https://medium.com/@rymshasiddiqui/path-planning-using-potential-field-algorithm-a30ad12bdb08)
    - [Local Path Planning Using virtual Potential Field in Python](https://medium.com/nerd-for-tech/local-path-planning-using-virtual-potential-field-in-python-ec0998f490af)
    - [PulkitRustagi/Potential-Field-Path-Planning](https://github.com/PulkitRustagi/Potential-Field-Path-Planning/blob/main/potential_PathPlanning.py)

### Implementação
- Alterações na maneira de implementar o Potencial Field.
    #### Possíveis Melhorias:
    - Melhorar a modularização:
        - Melhoria deveria ter sido implementada no Navigation.py.
    - Estudar e reavaliar os parâmetros:
        - Testes feitos com K_ATTRACT = 5.0, K_REPULSE = 3.0 e REPULSE_RADIUS = 0.5 apresentaram melhor comportamento que K_ATTRACT = 3.0, K_REPULSE = 3.0 e REPULSE_RADIUS = 0.5. (Foram feitas capturas dos comportamentos)
    - Suavização de movimento.


