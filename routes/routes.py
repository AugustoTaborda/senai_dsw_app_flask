from flask import render_template, request, redirect, url_for, session, flash, get_flashed_messages
from forms.forms import ContatoForm  # Importa o formulário
import os
import sqlite3


# CLUD Simples - Inicio
tarefas = [] 
tarefas.append("Comprar pão")
tarefas.append("Estudar Python")

# CLUD Simples - Fim


# CRUD SQL - Inicio

#Função para conectar ao banco de dados
def obter_conexao_bd():
    conexao_bd = sqlite3.connect('database.db')
    conexao_bd.row_factory = sqlite3.Row
    return conexao_bd

# Função para criar o banco e as tabelas

def iniciar_bd():
    if not os.path.exists('database.db'):
        conexao_bd = obter_conexao_bd()
        conexao_bd.execute('''
                           CREATE TABLE IF NOT EXISTS Categoria (
                               Id INTEGER PRIMARY KEY AUTOINCREMENT,
                               Nome TEXT NOT NULL
                           )
                           ''')
        conexao_bd.execute('''
                           CREATE TABLE IF NOT EXISTES Produto (
                               Id INTEGER PRIMARY KEY AUTOINCREMENT,
                               Nome TEXT NOT NULL,
                               IdCategorias INTEGER,
                               FOREIGN KEY (IdCategorias) REFERENCES Categoria(Id)
                           ) 
                           ''')
        
        conexao_bd.execute('''
                           CREATE TABLE IF NOT EXISTS Usuario (
                                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                                Nome TEXT NOT NULL,
                                Email TEXT UNIQUE NOT NULL,
                                Senha TEXT NOT NULL
                           )
                           ''')
        conexao_bd.commit()
        conexao_bd.close()
        
# inicializar o banco de dados
iniciar_bd()


# CRUD SQL - Fim



def configurar_rotas(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/Web-Forms', methods=['GET', 'POST'])
    def web_form():
        if request.method == 'POST':
            nome = request.form['nome']
            email = request.form['email']
            idade = request.form['idade']
            mensagem = request.form['mensagem']
            
            # Aqui você pode processar os dados do formulário, 
            #como salvar em um banco de dados ou enviar um e-mail.
            print(f"Nome: {nome}, Email: {email}, Idade: {idade}, Mensagem: {mensagem}")
            
            return redirect(url_for('obrigado_1'))
        
        return render_template('web_forms.html')

    @app.route('/Web-Forms-WTF', methods=['GET', 'POST'])
    def web_forms_wtf():
        formulario = ContatoForm()
        if formulario.validate_on_submit():
            contato = {
                'nome': formulario.nome.data,
                'email': formulario.email.data,
                'idade': formulario.idade.data,
                'mensagem': formulario.mensagem.data
            }
            
            session['contato'] = contato # Armazena os dados na sessão
        
            return redirect(url_for('obrigado_2'))        
        
        return render_template('web_forms_wtf.html', formulario=formulario)

    @app.route('/upload-arquivo', methods=['GET', 'POST'])
    def upload_arquivo():
        if request.method == 'POST':
            if 'arquivo' not in request.files:
                
                flash( ' Nenhum  arquivo foi selecionado. ' )
                return redirect(url_for('upload_arquivo'))
            
            arquivo = request.files['arquivo']
            
            if arquivo.filename == '':
                
                flash('Nenhum  arquivo foi selecionado.')
                return redirect(url_for('upload_arquivo'))
            
            if arquivo:
                nome_arquivo = arquivo.filename
                caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)
                try:
                    
                    arquivo.save(caminho_arquivo)
                    flash(f'Arquivo {nome_arquivo} enviado com sucesso')
                    
                except Exception as e:
                    flash(f'Erro ao salvar o arquivo: {e}')
                return redirect(url_for('upload_arquivo'))
        # Se o metodo for GET, renderiza a pagina de upload
        
        
         
        return render_template('upload_arquivo.html')
    # CLUD Simples - inicio
    
    @app.route('/CRUD-Simples')
    def crud_simples():
        return render_template('crud_simples.html', tarefas=tarefas)
    
    @app.route('/adicionar', methods=['POST'])
    def adicionar():
        tarefa = request.form.get('tarefa')
        if tarefa:
            tarefas.append(tarefa)
        return redirect(url_for('crud_simples'))
    
    @app.route('/editar/<init:tarefa_id>', methods=['GET', 'POST'])
    def editar(tarefa_id):
        if request.method == 'POST':
            tarefa = request.form.get('tarefa')
            if tarefa:
                tarefas[tarefa_id] = tarefa
            return render_template(url_for('crud_simples'))
        
        tarefa = tarefas[tarefa_id]
        return render_template('crud_simples_edicao.html', tarefa=tarefa, tarefa_id=tarefa_id )
    
    @app.route('/excluir/<init:tarefa_id>')
    def excluir(tarefa_id):
        if 0 <= tarefa_id < len(tarefas):
            tarefas.pop(tarefa_id)
            
        return redirect(url_for('crud_simples'))
    
    # CLUD Simples - Fim


    # CRUD SQL - Inicio
    @app.route('/CRUD-SQL')
    def crud_sql():
        conexao_bd = obter_conexao_bd()
        categorias = conexao_bd.execute('SELECT * FROM Categoria').fetchall()
        produtos = conexao_bd.execute('SELECT p.Id, p.Nome, c.Nome as Categorias FROM Produto p JOIN Categoria c ON p.IdCategoria = c.Id').fetchall()
        conexao_bd.close()
        
        return render_template('crud_sql.html', categorias=categorias, produtos=produtos)
    
    @app.route('/categoria', methods={'GET', 'POST'})
    def categoria():
        # acesse as mensagens fish e as descarta
        get_flashed_messages()
        
        if request.method == 'POST':
            nome = request.form('nome')
            if not nome:
                flash('O nome da categoria é obrigatorio')
            else:
                conexao_bd = obter_conexao_bd()
                conexao_bd.execute('INSERT INTO Categoria (Nome) VALUES (?)', {nome,})
                conexao_bd.commit()
                conexao_bd.close()
                return redirect(url_for('crud_sql'))
        return render_template('categoria.html')
    
    
    
    # CRUD SQL - Fim

    @app.route('/CRUD-SQLAlchemy')
    def crud_sqlalchemy():
        return render_template('crud_sqlalchemy.html')
    
    @app.route('/sobre')
    def sobre():
        return render_template('sobre.html')

    @app.route('/contato')
    def contato():
        return render_template('contato.html')
    
    @app.route('/obrigado-1')
    def obrigado_1():
        return render_template('obrigado_1.html')
    
    @app.route('/obrigado-2')
    def obrigado_2():
        contato = session.get('contato', None)  # Recupera os dados da sessão
        if contato is None:
            # Redireciona para a página do formulário se não houver dados
            return redirect(url_for('web_forms_wtf'))
        # Limpa a sessão após o uso
        session.clear()
        return render_template('obrigado_2.html', contato=contato)
