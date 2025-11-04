# Documentação da Atividade 4: MVP e Padrões de Projeto

## 1. MVP Implementado

O Produto Mínimo Viável (MVP) consiste no **Núcleo de Gerenciamento de Entidades** para o sistema de Loja Virtual, conforme implementado no arquivo `marketplace_mvp.py`.

As funcionalidades principais são:
1.  **Modelagem de Dados:** Classes `Usuario`, `Vendedor` e `Produto`.
2.  **Gerenciamento de Identidade:** Cadastro de Usuários e promoção a Vendedores.
3.  **Catálogo:** Adição e listagem de Produtos associados aos Vendedores.

A persistência de dados é simulada através de listas em memória (variáveis globais).

---

## 2. Padrões de Projeto Utilizados

O MVP se baseia em um padrão de criação e um padrão estrutural para garantir a coesão e a escalabilidade futura.

### A. Padrão Criacional: Preparação para Factory Method

Embora o MVP atual implemente a criação de objetos (`new Usuario(...)`) diretamente nas funções, a estrutura foi desenhada para facilitar a adoção do **Factory Method** em uma evolução futura.

* **Onde se aplica:** Na função de cadastro (`cadastrar_usuario`) ou na adição de produtos (`adicionar_produto`).
* **Por que é relevante:** No futuro, se houver diferentes tipos de usuários (ex: `UsuarioPremium`, `UsuarioBásico`) ou produtos (ex: `ProdutoDigital`, `ProdutoFísico`), o Factory Method permitirá centralizar e abstrair a lógica de criação, decidindo qual classe instanciar sem alterar o código cliente que faz a chamada (`main`).

### B. Padrão Estrutural: Singleton (Implícito)

Este padrão é utilizado para gerenciar o estado centralizado da aplicação.

* **Onde é aplicado:** Nas listas e contadores de ID definidos globalmente (`usuarios`, `vendedores`, `proximo_id_usuario`, etc.).
* **Por que foi utilizado:** No contexto de um MVP em memória que simula um Banco de Dados, o Singleton (implícito) garante que **apenas uma instância** dos dados (a lista global) seja acessada por todas as funções. Isso assegura a consistência e a unicidade da informação em todo o sistema, simulando uma única fonte de verdade.

---