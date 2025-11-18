#
#  Para rodar o teste no terminal é necessário usar o comando:
#       python3 -m unittest tests.py
#

import unittest
# Importa TUDO do código principal (classes e listas globais)
from main4 import *

class TestAdicionarProduto(unittest.TestCase):

    def setUp(self):
        usuarios.clear()
        vendedores.clear()
        produtos.clear()
        
        global proximo_id_usuario, proximo_id_vendedor, proximo_id_produto
        proximo_id_usuario = 1
        proximo_id_vendedor = 1
        proximo_id_produto = 1

        usuario_teste = Usuario(
            nome="Vendedor Teste", 
            email="vendedor@teste.com", 
            senha="123", 
            endereco="Rua Teste, 1"
        )
        usuarios.append(usuario_teste)
        
        vendedor_teste = Vendedor(
            id_usuario=usuario_teste.id_usuario, 
            nome_loja="Loja Teste"
        )
        vendedores.append(vendedor_teste)

    def test_adicionar_produto_sucesso(self):
        """Caso de Teste 1: Caminho feliz (Happy Path)"""
        print("Executando: test_adicionar_produto_sucesso")
        
        resultado = adicionar_produto_logica(
            email_usuario="vendedor@teste.com",
            nome_produto="Camiseta Azul",
            descricao="Algodão 100%",
            preco_str="59.90",
            imagem_url="http://teste.com/img.png"
        )
        
        self.assertEqual(len(produtos), 1, "Deveria haver 1 produto na lista")
        self.assertEqual(produtos[0].nome, "Camiseta Azul")
        self.assertEqual(produtos[0].preco, 59.90)
        self.assertTrue(resultado.startswith("✅"), "Mensagem de sucesso esperada")

    def test_adicionar_produto_usuario_nao_encontrado(self):
        """Caso de Teste 2: E-mail do usuário não existe"""
        print("Executando: test_adicionar_produto_usuario_nao_encontrado")
        
        resultado = adicionar_produto_logica(
            email_usuario="fantasma@teste.com",
            nome_produto="Produto Fantasma",
            descricao="",
            preco_str="10.0",
            imagem_url="url"

            # Para testar um caso em que o teste falha, usar a linha abaixo como email_usuario:
            #email_usuario="vendedor@teste.com"
        )
        
        self.assertEqual(len(produtos), 0, "Nenhum produto deve ser adicionado")
        self.assertEqual(resultado, "❌ Usuário não encontrado.")

    def test_adicionar_produto_usuario_nao_e_vendedor(self):
        """Caso de Teste 3: Usuário existe, mas não é vendedor"""
        print("Executando: test_adicionar_produto_usuario_nao_e_vendedor")
        
        usuario_cliente = Usuario("Cliente Teste", "cliente@teste.com", "123", "Rua C, 2")
        usuarios.append(usuario_cliente)
        
        resultado = adicionar_produto_logica(
            email_usuario="cliente@teste.com",
            nome_produto="Produto de Cliente",
            descricao="",
            preco_str="10.0",
            imagem_url="url"
        )
        
        self.assertEqual(len(produtos), 0, "Nenhum produto deve ser adicionado")
        self.assertEqual(resultado, "❌ Você precisa se tornar um vendedor para adicionar produtos.")

    def test_adicionar_produto_preco_invalido(self):
        """Caso de Teste 4: Preço com formato inválido (letras)"""
        print("Executando: test_adicionar_produto_preco_invalido")
        
        resultado = adicionar_produto_logica(
            email_usuario="vendedor@teste.com",
            nome_produto="Produto Caro",
            descricao="Desc",
            preco_str="cinquenta reais",
            imagem_url="url"
        )
        
        self.assertEqual(len(produtos), 0, "Nenhum produto deve ser adicionado")
        self.assertTrue(resultado.startswith("❌ Valor de preço inválido!"))

        resultado = adicionar_produto_logica(
            email_usuario="vendedor@teste.com",
            nome_produto="Produto Caro",
            descricao="Desc",
            preco_str="-2",
            imagem_url="url"
        )
        
        self.assertEqual(len(produtos), 0, "Nenhum produto deve ser adicionado")
        self.assertTrue(resultado.startswith("❌ Valor de preço inválido!"))


    def test_adicionar_produto_campos_obrigatorios_vazios(self):
        """Caso de Teste 5: Nome do produto está vazio"""
        print("Executando: test_adicionar_produto_campos_obrigatorios_vazios")
        
        resultado = adicionar_produto_logica(
            email_usuario="vendedor@teste.com",
            nome_produto="  ",
            descricao="Desc",
            preco_str="10.0",
            imagem_url="url"
        )
        
        self.assertEqual(len(produtos), 0, "Nenhum produto deve ser adicionado")
        self.assertEqual(resultado, "❌ Nome do produto e URL da Imagem são obrigatórios.")

class TestCadastrarUsuario(unittest.TestCase):
    
    def setUp(self):
        """Prepara o ambiente para testes de USUÁRIO:
        - Listas totalmente limpas
        """
        usuarios.clear()
        vendedores.clear()
        produtos.clear()
        global proximo_id_usuario
        proximo_id_usuario = 1

    def test_cadastrar_usuario_sucesso(self):
        print("Executando: test_cadastrar_usuario_sucesso")
        resultado = cadastrar_usuario_logica(
            "Cliente Novo", "cliente@email.com", "senha123", "senha123",
            "Rua A", "10", "Bairro B", "Cidade C", "12345678"
        )
        self.assertTrue(resultado.startswith("✅"))
        self.assertEqual(len(usuarios), 1)
        self.assertEqual(usuarios[0].nome, "Cliente Novo")
        self.assertEqual(usuarios[0].email, "cliente@email.com")

    def test_cadastrar_usuario_senhas_nao_conferem(self):
        print("Executando: test_cadastrar_usuario_senhas_nao_conferem")
        resultado = cadastrar_usuario_logica(
            "Cliente", "c@email.com", "senha123", "senha456",
            "Rua A", "10", "Bairro B", "Cidade C", "12345678"
        )
        self.assertEqual(resultado, "Erro: As senhas não conferem.")
        self.assertEqual(len(usuarios), 0) # Não deve criar o usuário

    def test_cadastrar_usuario_email_invalido(self):
        print("Executando: test_cadastrar_usuario_email_invalido")
        resultado = cadastrar_usuario_logica(
            "Cliente", "email_invalido.com", "123", "123",
            "Rua A", "10", "Bairro B", "Cidade C", "12345678"
        )
        self.assertEqual(resultado, "Erro: E-mail inválido. Use o formato 'nome@dominio.com'.")

    def test_cadastrar_usuario_nome_invalido(self):
        print("Executando: test_cadastrar_usuario_nome_invalido")
        resultado = cadastrar_usuario_logica(
            "Nome123", "a@b.com", "123", "123", "Rua", "1", "B", "C", "12345678"
        )
        self.assertEqual(resultado, "Erro: O nome deve conter apenas letras e espaços.")
        
    def test_cadastrar_usuario_cep_invalido(self):
        print("Executando: test_cadastrar_usuario_cep_invalido")
        resultado = cadastrar_usuario_logica(
            "Nome Valido", "a@b.com", "123", "123", "Rua", "1", "B", "C", "12345" # CEP curto
        )
        self.assertEqual(resultado, "Erro: CEP inválido. Digite 8 números (sem traço).")
        
    def test_cadastrar_usuario_endereco_invalido(self):
        print("Executando: test_cadastrar_usuario_endereco_invalido")
        resultado = cadastrar_usuario_logica(
            "Nome Valido", "a@b.com", "123", "123", "", "1", "B", "C", "12345678" # CEP curto
        )
        self.assertEqual(resultado, "Erro: Todos os campos do endereço são obrigatórios.")

    def test_cadastrar_usuario_email_duplicado(self):
        print("Executando: test_cadastrar_usuario_email_duplicado")
        # Cria o primeiro usuário
        cadastrar_usuario_logica(
            "Cliente Um", "user@email.com", "123", "123", "R", "1", "B", "C", "12345678"
        )
        self.assertEqual(len(usuarios), 1)
        # Tenta criar o segundo com o mesmo e-mail
        resultado = cadastrar_usuario_logica(
            "Cliente Dois", "user@email.com", "456", "456", "R", "2", "B", "C", "87654321"
        )
        self.assertEqual(resultado, "Erro: Este e-mail já está em uso.")
        self.assertEqual(len(usuarios), 1) # Garante que o segundo não foi criado

class TestTornarVendedor(unittest.TestCase):
    
    def setUp(self):
        """Prepara o ambiente para testes de VENDEDOR:
        - 1 Usuário que NÃO É Vendedor
        """
        usuarios.clear()
        vendedores.clear()
        produtos.clear()
        global proximo_id_usuario, proximo_id_vendedor
        proximo_id_usuario = 1
        proximo_id_vendedor = 1
        
        # Cria um usuário base que é apenas cliente
        usuario_cliente = Usuario("Cliente Padrao", "cliente@padrao.com", "123", "End")
        usuarios.append(usuario_cliente)

    def test_tornar_vendedor_sucesso(self):
        print("Executando: test_tornar_vendedor_sucesso")
        resultado = tornar_vendedor_logica("cliente@padrao.com", "Loja do Cliente")
        self.assertTrue(resultado.startswith("✅"))
        self.assertEqual(len(vendedores), 1)
        self.assertEqual(vendedores[0].nome_loja, "Loja do Cliente")
        self.assertEqual(vendedores[0].id_usuario, usuarios[0].id_usuario)

    def test_tornar_vendedor_usuario_nao_encontrado(self):
        print("Executando: test_tornar_vendedor_usuario_nao_encontrado")
        resultado = tornar_vendedor_logica("fantasma@email.com", "Loja Fantasma")
        self.assertEqual(resultado, "❌ Usuário não encontrado. Cadastre-se primeiro.")
        self.assertEqual(len(vendedores), 0)

    def test_tornar_vendedor_ja_e_vendedor(self):
        print("Executando: test_tornar_vendedor_ja_e_vendedor")
        # Torna o usuário um vendedor (primeira vez)
        tornar_vendedor_logica("cliente@padrao.com", "Minha Primeira Loja")
        self.assertEqual(len(vendedores), 1)
        
        # Tenta tornar vendedor de novo
        resultado = tornar_vendedor_logica("cliente@padrao.com", "Minha Segunda Loja")
        self.assertEqual(resultado, "❌ Você já é um vendedor!")
        self.assertEqual(len(vendedores), 1) # Garante que não criou um segundo registro
        
    def test_tornar_vendedor_nome_loja_vazio(self):
        print("Executando: test_tornar_vendedor_nome_loja_vazio")
        resultado = tornar_vendedor_logica("cliente@padrao.com", "   ") # Nome da loja vazio
        self.assertEqual(resultado, "❌ O nome da loja não pode ser vazio.")
        self.assertEqual(len(vendedores), 0)

if __name__ == '__main__':
    unittest.main()