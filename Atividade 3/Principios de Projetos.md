# Relatório sobre Princípios de Projeto de Software

Este relatório detalha a aplicação de princípios de projeto de software, com foco no acrônimo *SOLID*, ao sistema de loja virtual. A análise é baseada nas estórias de usuário e nos diagramas UML (Casos de Uso e Classes) desenvolvidos para o projeto.

## O que são Princípios de Projeto?

Princípios de projeto são diretrizes e boas práticas que visam orientar a criação de software de alta qualidade. Eles ajudam a construir sistemas que são mais fáceis de entender, manter, testar e estender ao longo do tempo. Adotar esses princípios reduz a complexidade, o acoplamento (dependência entre partes) e aumenta a coesão (responsabilidades bem definidas).

## Aplicação dos Princípios SOLID

SOLID é um acrônimo para cinco princípios de design de classes em programação orientada a objetos.

---

### 1. (S) Single Responsibility Principle - Princípio da Responsabilidade Única

> "Uma classe deve ter um, e apenas um, motivo para mudar."

*Explicação:* Cada classe ou módulo em um sistema deve ser responsável por uma única funcionalidade. Isso torna as classes menores, mais focadas e mais fáceis de entender.

*Aplicação no Projeto:*
Nossos diagramas já refletem esse princípio:
* *Classe Usuario:* Sua única responsabilidade é gerenciar os dados de autenticação e perfil do usuário (nome, email, senha, endereço).
* *Classe Vendedor:* Sua responsabilidade é gerenciar os dados específicos de um vendedor (como o nome da loja), atuando como um "papel" que um usuário pode assumir.
* *Classe Produto:* Sua única responsabilidade é conter as informações sobre um produto (nome, descrição, preço, etc.).

Se precisássemos, por exemplo, adicionar um sistema de Pedidos, criaríamos uma nova classe Pedido, em vez de adicionar essa responsabilidade à classe Usuario ou Produto.

---

### 2. (O) Open/Closed Principle - Princípio do Aberto/Fechado

> "As entidades de software (classes, módulos, funções) devem estar abertas para extensão, mas fechadas para modificação."

*Explicação:* Devemos ser capazes de adicionar novas funcionalidades a uma classe sem alterar seu código-fonte existente. Isso geralmente é alcançado através de herança, interfaces ou padrões de composição.

*Aplicação no Projeto:*
O design atual permite extensões facilmente:
* *Novos Papéis de Usuário:* Se no futuro precisarmos de um usuário Administrador com permissões especiais, podemos criar uma nova classe Administrador associada ao Usuario, sem precisar modificar a classe Usuario.
* *Novos Tipos de Produto:* Se quiséssemos vender Produtos Digitais (que não têm estoque físico, mas têm um link para download), poderíamos criar uma nova classe ProdutoDigital que herda de Produto e adiciona o campo link_download, sem alterar a classe Produto original.

---

### 3. (L) Liskov Substitution Principle - Princípio da Substituição de Liskov

> "Se S é um subtipo de T, então os objetos do tipo T podem ser substituídos por objetos do tipo S sem alterar nenhuma das propriedades desejáveis do programa."

*Explicação:* Uma classe derivada (filha) deve ser perfeitamente substituível por sua classe base (mãe).

*Aplicação no Projeto:*
Na nossa primeira versão dos diagramas, tínhamos Vendedor herdando de Usuario. Se tivéssemos mantido esse modelo, o Princípio de Liskov exigiria que qualquer parte do código que funcionasse com um Usuario também deveria funcionar perfeitamente se recebesse um Vendedor.

Ao mudarmos para o modelo de *composição* (um Usuario tem um Vendedor), nós evitamos possíveis violações deste princípio e criamos um design mais flexível, que se alinha melhor à nossa regra de negócio ("qualquer usuário pode ser um vendedor").

---

### 4. (I) Interface Segregation Principle - Princípio da Segregação de Interfaces

> "Nenhum cliente deve ser forçado a depender de métodos que não usa."

*Explicação:* É melhor ter muitas interfaces pequenas e específicas do que uma única interface grande e genérica.

*Aplicação no Projeto:*
Atualmente, não temos interfaces explícitas, mas podemos projetar como elas seriam. Em vez de uma interface "genérica" IUsuario, poderíamos ter:
* IComprador: com métodos como fazerPedido(), verHistoricoDeCompras().
* IVendedor: com métodos como cadastrarProduto(), verRelatorioDeVendas().

Um Usuario comum implementaria apenas IComprador. Quando ele se tornasse um vendedor, sua conta passaria a implementar também IVendedor. Isso garante que um usuário que é apenas comprador não tenha acesso a métodos de vendedor.

---

### 5. (D) Dependency Inversion Principle - Princípio da Inversão de Dependência

> "Módulos de alto nível não devem depender de módulos de baixo nível. Ambos devem depender de abstrações."

*Explicação:* As classes devem depender de abstrações (como interfaces), e não de implementações concretas (classes específicas). Isso desacopla o código e o torna mais flexível e testável.

*Aplicação no Projeto:*
Imagine como salvaríamos um produto no banco de dados. Uma má prática seria a classe Produto ter o código para se conectar e salvar em um banco de dados específico (ex: MySQL).

A forma correta, aplicando o DIP, seria:
1.  Criar uma interface chamada IProdutoRepository com um método salvar(produto).
2.  A lógica de negócio que cadastra um produto dependeria dessa *interface*, não de uma classe concreta.
3.  Criaríamos uma classe concreta, como ProdutoRepositoryMySQL, que implementa a interface IProdutoRepository e contém o código específico para o MySQL.

Dessa forma, se no futuro quisermos trocar o banco de dados para PostgreSQL, basta criar uma nova classe ProdutoRepositoryPostgreSQL e "injetar" no sistema, sem alterar nenhuma regra de negócio.
