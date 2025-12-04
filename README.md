## Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Como clonar ou baixar](#como-clonar-ou-baixar)  
- [Estrutura do Projeto](#estrutura-do-projeto)  
- [Licença](#licença)  

## Sobre o Projeto

### Título
Engenharia de Software

### Descrição
Repositório destinado a disciplina DCA3603 - Engenharia de Software. As atividades realizadas durante o semestre estão guardadas em suas respectivas pastas, algumas acompanham descrição em markdown próprio.

### Componentes
- Luan Pedro Abreu Vieira 
- Matheus Almeida Fontes
- Pedro Henrique da Silva Santos

### Estrutura do Projeto

> *Esta seção pode variar conforme a organização do repositório de cada grupo.*

```
Eng-de-Software-UFRN/
├── LICENSE
├── README.md
├── <Atividade 1>/
├── <Atividade 2>/
├── <Atividade 3>/                # Relatório de Princípios SOLID
├── <Atividade 4>/                # Código inicial do MVP (.ipynb)
└── <Atividade 5>/                # Versão Final com Testes (main4.py, tests.py)
```

Instalação e Execução
Siga os passos abaixo para rodar a versão final do projeto (localizada na Atividade 5).

Clone o repositório:

Bash

git clone [https://github.com/matheusalmeida431/Projeto-Engenharia-de-Software.git](https://github.com/matheusalmeida431/Projeto-Engenharia-de-Software.git)
cd Projeto-Engenharia-de-Software
Instale as dependências: O projeto necessita das seguintes bibliotecas para interface gráfica e manipulação de imagens:

Bash

pip install easygui requests Pillow coverage

Execute o Sistema (Loja Virtual): Navegue até a pasta da versão final e execute:

Bash

cd "Atividade 5"
python main4.py
A interface gráfica da loja será aberta.

Testes e Qualidade
Para garantir a qualidade do software, foram aplicados testes na versão final (Atividade 5).

- Executar Testes Unitários

# Dentro da pasta 'Atividade 5'
python -m unittest tests.py

- Verificar Cobertura (Coverage)

Para gerar o relatório de cobertura de código:

Bash

coverage run --source=main4 -m unittest tests.py
coverage report

Nota: A cobertura de código gira em torno de 60% pois o código de interface gráfica (easygui) foi isolado da lógica de negócio testável. Para mais informações veja o README da atividade 5.

Licença
Este projeto está licenciado sob a Licença MIT. Consulte o arquivo LICENSE para mais informações.
