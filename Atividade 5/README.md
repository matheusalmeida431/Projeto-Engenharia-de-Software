Para executar o sistema utilize:

> python3 main4.py

A interface gráfica irá aparecer e deve ser possível interagir com ela.

Para executar os testes é necessário instalar as bibliotecas *unittest* e *coverage* e usar os seguintes comandos:

- Para executar o unittest o qual irá verificar se todos os testes passam:

> python3 -m unittest tests.py

Após execução dos teste o terminal irá exibir o tempo de execução, os testes executados e o status OK ou caso falho casa haja algum teste que falhe.

- Para executar o coverage, que avalia a cobertura do teste:

> python3-coverage run --source=main4 -m unittest tests.py

Talvez o comando seja diferentes pois fiz a instalação do coverage pelo WSL. Ao executar o comando anterior, execute:

> python-coverage report

 Se conseguir executar, será exibida a quantidade de linhas de comandos no código main4.py ( Stmts ), quantidade de linhas não executadas ( Miss ) e a cobertura em porcentagem ( Cover ). No terminal deve aparecer algo do tipo:

Name      |   Stmts |  Miss | Cover

main4.py  |   194   |  106  |  45%

TOTAL     |   194   |  106  |  45%


Considerando que o coverage calcula a cobertura utilizando TODAS as linhas executáveis do código, há uma certa incoerência na porcentagem de cobertura pois como estamos usando a biblioteca easyGUI a qual cria uma interface gráfica, vários comando são para exibição de telas, interação do usuário com a tela e recebimento de dados pala GUI. Esses comandos não são executados nos teste de tests.py pois dependem da iteração do usuário. Então 19 linhas explicitamente usam comando da biblioteca easyGUI e 6 métodos não são chamados pois não são classe que implementam a lógica, mas implementam a interação com o usuário. 

Se tirarmos somente as linhas da biblioteca easyGUI do cálculo ficamos com 175 statements com 106 misses, a cobertura então é aproximadamente 60.57% [ (106*100) / 175 ] . Se não considerarmos as linhas dos métodos iterativos/gráficos a cobertura é quase completa. 


É possível também exectuar < python3-coverage html > o qual irá gerar uma pasta chamada *htmlcov* com informações visuais da cobertura. Só rodar a página gerada que será possível ver quais linhas foram executadas e quais não foram.