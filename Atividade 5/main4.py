import re
import easygui as eg
import os           
import requests     
import tempfile     
from urllib.parse import urlparse

# --- SIMULAÇÃO DO BANCO DE DADOS EM MEMÓRIA ---
usuarios = []
vendedores = []
produtos = []

proximo_id_usuario = 1
proximo_id_vendedor = 1
proximo_id_produto = 1

# --- CLASSES DE MODELO ---
class Usuario:
    def __init__(self, nome, email, senha, endereco):
        global proximo_id_usuario
        self.id_usuario = proximo_id_usuario
        self.nome = nome
        self.email = email
        self.senha = senha
        self.endereco = endereco
        proximo_id_usuario += 1

class Vendedor:
    def __init__(self, id_usuario, nome_loja):
        global proximo_id_vendedor
        self.id_vendedor = proximo_id_vendedor
        self.id_usuario = id_usuario
        self.nome_loja = nome_loja
        proximo_id_vendedor += 1

class Produto:
    def __init__(self, nome, descricao, preco, id_vendedor, imagem_url):
        global proximo_id_produto
        self.id_produto = proximo_id_produto
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.id_vendedor = id_vendedor
        self.imagem_url = imagem_url


# --- FUNÇÕES (Lógica de Negócio) ---

def cadastrar_usuario_logica(nome, email, senha, confirma_senha, rua, numero, bairro, cidade, cep):
    """Contém APENAS a lógica de negócio para cadastrar um usuário."""
    
    if not nome.strip() or not nome.replace(" ", "").isalpha():
        return "Erro: O nome deve conter apenas letras e espaços."
    
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        return "Erro: E-mail inválido. Use o formato 'nome@dominio.com'."
    
    # verificar e-mail duplicado
    if any(u.email == email for u in usuarios):
        return "Erro: Este e-mail já está em uso."
        
    if senha != confirma_senha:
        return "Erro: As senhas não conferem."
        
    if not rua.strip() or not numero.strip() or not bairro.strip() or not cidade.strip():
        return "Erro: Todos os campos do endereço são obrigatórios."
        
    if not cep.isdigit() or len(cep) != 8:
        return "Erro: CEP inválido. Digite 8 números (sem traço)."
        
    endereco_completo = f"{rua.strip()}, {numero.strip()} - {bairro.strip()}, {cidade.strip()}. CEP: {cep}"
    novo_usuario = Usuario(nome.strip(), email, senha, endereco_completo)
    usuarios.append(novo_usuario)

    return f"✅ Usuário '{nome.strip()}' cadastrado com sucesso!"

def cadastrar_usuario():
    """Contém APENAS a interface (EasyGUI) para coletar os dados do usuário."""
    titulo = "Cadastro de Novo Usuário"
    msg = "Por favor, preencha todos os campos:"
    
    nomes_campos = ["Nome Completo", "E-mail (ex: nome@dominio.com)", "Senha", "Confirmar Senha",
                    "Rua/Avenida", "Número (ou 's/n')", "Bairro", "Cidade", "CEP (só 8 números)"]
    
    valores = eg.multenterbox(msg, titulo, nomes_campos)

    if valores is None:
        return 

    nome, email, senha, confirma_senha, rua, numero, bairro, cidade, cep = valores
    
    # Chama a função de lógica com os valores
    resultado = cadastrar_usuario_logica(nome, email, senha, confirma_senha, rua, numero, bairro, cidade, cep)
    
    # Exibe o resultado (sucesso ou erro)
    eg.msgbox(resultado, "Resultado do Cadastro")

def tornar_vendedor_logica(email_usuario, nome_loja):
    """Contém APENAS a lógica de negócio para tornar um usuário vendedor."""
    
    usuario_encontrado = next((u for u in usuarios if u.email == email_usuario), None)

    if not usuario_encontrado:
        return "❌ Usuário não encontrado. Cadastre-se primeiro."

    ja_e_vendedor = any(v.id_usuario == usuario_encontrado.id_usuario for v in vendedores)
    if ja_e_vendedor:
        return "❌ Você já é um vendedor!"

    if not nome_loja.strip():
        return "❌ O nome da loja não pode ser vazio."

    novo_vendedor = Vendedor(id_usuario=usuario_encontrado.id_usuario, nome_loja=nome_loja.strip())
    vendedores.append(novo_vendedor)

    return f"✅ Parabéns, {usuario_encontrado.nome}! Sua loja '{nome_loja.strip()}' foi criada."


def tornar_vendedor():
    """Contém APENAS a interface (EasyGUI) para coletar dados do vendedor."""
    titulo = "Tornar-se um Vendedor"
    
    email_usuario = eg.enterbox("Confirme seu e-mail de usuário:", titulo)
    if email_usuario is None: return

    # Verificações rápidas antes de pedir o nome da loja
    usuario_encontrado = next((u for u in usuarios if u.email == email_usuario), None)
    if not usuario_encontrado:
        eg.msgbox("❌ Usuário não encontrado. Cadastre-se primeiro.", titulo)
        return

    ja_e_vendedor = any(v.id_usuario == usuario_encontrado.id_usuario for v in vendedores)
    if ja_e_vendedor:
        eg.msgbox("❌ Você já é um vendedor!", titulo)
        return
    
    # Só pede o nome da loja se o usuário for válido
    nome_loja = eg.enterbox(f"Olá, {usuario_encontrado.nome}. Qual será o nome da sua loja?", titulo)
    if nome_loja is None: return

    # Chama a função de lógica
    resultado = tornar_vendedor_logica(email_usuario, nome_loja)

    eg.msgbox(resultado, "Resultado")

# --- FUNÇÕES (Lógica de Negócio) ---

###################################################

def adicionar_produto_logica(email_usuario, nome_produto, descricao, preco_str, imagem_url):
    """
    Recebe os parâmetros passados na função adicionar_produto() os quais são digitados pelo usuário
    na interface do easyGUI.

    Essa função é necessário pois o teste simula a chamada dela passando parâmetros que serão testados,
    e o resultado será comparado com o esperado. A função antiga não recebia parâmetros.
    """
    
    # Procura o usuário
    usuario_encontrado = next((u for u in usuarios if u.email == email_usuario), None)
    if not usuario_encontrado:
        return "❌ Usuário não encontrado."

    # Verifica se é vendedor
    vendedor_encontrado = next((v for v in vendedores if v.id_usuario == usuario_encontrado.id_usuario), None)
    if not vendedor_encontrado:
        return "❌ Você precisa se tornar um vendedor para adicionar produtos."

    # Valida o preço recebido
    try:
        preco = float(preco_str.replace(',', '.'))
        if preco <= 0:
             raise ValueError("Preço deve ser positivo")
    except ValueError:
        return "❌ Valor de preço inválido! Use números positivos e ponto (ex: 29.99)."
        
    # 4. Validaa os campos obrigatórios
    if not nome_produto.strip() or not imagem_url.strip():
        return "❌ Nome do produto e URL da Imagem são obrigatórios."

    novo_produto = Produto(
        nome=nome_produto.strip(), 
        descricao=descricao, 
        preco=preco, 
        id_vendedor=vendedor_encontrado.id_vendedor, 
        imagem_url=imagem_url.strip()
    )
    produtos.append(novo_produto)
    
    return f"✅ Produto '{nome_produto.strip()}' adicionado com sucesso!"


def adicionar_produto():
    """
    Essa função recebe os valores da interface de usuário e chama a função adicionar_produto_logica() passando
    os valores recebidos como parâmetros.
    """
    titulo = "Adicionar Novo Produto"
    
    # Coleta 1: E-mail
    email_usuario = eg.enterbox("Confirme seu e-mail de vendedor:", titulo)
    if email_usuario is None: return

    # Validação rápida de e-mail (opcional, mas bom)
    usuario_encontrado = next((u for u in usuarios if u.email == email_usuario), None)
    vendedor_encontrado = None
    if usuario_encontrado:
        vendedor_encontrado = next((v for v in vendedores if v.id_usuario == usuario_encontrado.id_usuario), None)

    if not usuario_encontrado:
         eg.msgbox("❌ Usuário não encontrado.", titulo)
         return
    if not vendedor_encontrado:
         eg.msgbox("❌ Você precisa se tornar um vendedor para adicionar produtos.", titulo)
         return

    # Coleta 2: Dados do Produto
    msg = f"Olá, {usuario_encontrado.nome} da loja '{vendedor_encontrado.nome_loja}'!"
    nomes_campos = ["Nome do Produto", "Descrição", "Preço (use PONTO, ex: 29.99)", 
                    "URL da Imagem (http://.../.png, .gif ou .jpg)"]
    
    valores = eg.multenterbox(msg, titulo, nomes_campos)
    if valores is None: return
    
    nome_produto, descricao, preco_str, imagem_url = valores
    
    # 6. Chamar a LÓGICA
    resultado = adicionar_produto_logica(
        email_usuario, 
        nome_produto, 
        descricao, 
        preco_str, 
        imagem_url
    )
    
    # 7. Exibir o resultado da lógica
    eg.msgbox(resultado, titulo)

######################################################


def listar_produtos():
    titulo = "Catálogo de Produtos"
    if not produtos:
        eg.msgbox("Nenhum produto cadastrado no momento.", titulo)
        return

    produto_escolhido = None
    
    if len(produtos) == 1:
        produto_escolhido = produtos[0]
    else:
        nomes_produtos = [p.nome for p in produtos]
        msg = "Escolha um produto para ver os detalhes:"
        escolha = eg.choicebox(msg, titulo, nomes_produtos)

        if escolha is None:
            return
        
        produto_escolhido = next((p for p in produtos if p.nome == escolha), None)

    if produto_escolhido is None:
        return

    vendedor_do_produto = next((v for v in vendedores if v.id_vendedor == produto_escolhido.id_vendedor), None)
    nome_loja = vendedor_do_produto.nome_loja if vendedor_do_produto else "Loja Desconhecida"

    texto_detalhes = f"Produto: {produto_escolhido.nome}\n"
    texto_detalhes += f"Descrição: {produto_escolhido.descricao}\n"
    texto_detalhes += f"Preço: R$ {produto_escolhido.preco:.2f}\n"
    texto_detalhes += f"Vendido por: {nome_loja}\n"

    imagem_url = produto_escolhido.imagem_url
    temp_path = None
    
    # Formatos suportados agora que temos o Pillow
    formatos_suportados = ('.png', '.gif', '.jpg', '.jpeg')

    try:
        # Verifica se é um caminho LOCAL
        if os.path.exists(imagem_url) and imagem_url.lower().endswith(formatos_suportados):
            eg.msgbox(texto_detalhes, titulo, image=imagem_url)
        
        # Verifica se é uma URL
        elif imagem_url.lower().startswith('http'):
            # Extrai a extensão da URL
            path = urlparse(imagem_url).path
            ext = os.path.splitext(path)[1].lower()

            if ext in formatos_suportados:
                response = requests.get(imagem_url)
                response.raise_for_status()
                
                # Usa a extensão correta (ex: .jpg) para o arquivo temporário
                temp_file = tempfile.NamedTemporaryFile(suffix=ext, delete=False)
                temp_file.write(response.content)
                temp_path = temp_file.name
                temp_file.close()

                eg.msgbox(texto_detalhes, titulo, image=temp_path)
            else:
                raise ValueError(f"Formato de URL não suportado: {ext} (use .png, .gif, .jpg)")
        else:
            raise ValueError("Caminho/URL inválido")

    except Exception as e:
        texto_detalhes += f"\n\n--- [Imagem não pôde ser exibida] ---\nURL: {imagem_url}\nErro: {e}"
        eg.msgbox(texto_detalhes, titulo)
        
    finally:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)


# --- INTERFACE DE MENU PRINCIPAL ---
def main():
    while True:
        titulo = "Menu Principal - Loja Virtual"
        msg = "Bem-vindo! O que você gostaria de fazer?"
        
        escolhas = ["Ver produtos disponíveis", 
                    "Cadastrar novo usuário", 
                    "Tornar-se um vendedor", 
                    "Adicionar novo produto", 
                    "Sair"]
        
        escolha = eg.buttonbox(msg, titulo, choices=escolhas)

        if escolha is None or escolha == "Sair":
            eg.msgbox("Obrigado por usar o sistema. Até logo!", "Saindo")
            break
        elif escolha == "Ver produtos disponíveis":
            listar_produtos()
        elif escolha == "Cadastrar novo usuário":
            cadastrar_usuario()
        elif escolha == "Tornar-se um vendedor":
            tornar_vendedor()
        elif escolha == "Adicionar novo produto":
            adicionar_produto()

# Roda o programa
if __name__ == "__main__":
    main()