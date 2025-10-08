from flask import Flask, render_template, request, redirect, url_for, jsonify
import database
from datetime import datetime, timedelta

app = Flask(__name__)

# ===== ROTAS PRINCIPAIS =====
@app.route('/')
def index():
    return render_template('index.html')

# ===== ROTAS VEÍCULOS =====
@app.route('/veiculos')
def veiculos():
    connection = database.create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM veiculos ORDER BY id DESC")
            veiculos_data = cursor.fetchall()
            return render_template('veiculos.html', veiculos=veiculos_data)
        except Exception as e:
            return f"Erro ao buscar veículos: {e}"
        finally:
            cursor.close()
            connection.close()
    return "Erro de conexão com o banco"

@app.route('/veiculo/novo', methods=['GET', 'POST'])
def novo_veiculo():
    if request.method == 'POST':
        marca = request.form['marca']
        modelo = request.form['modelo']
        ano = request.form['ano']
        placa = request.form['placa']
        preco_diaria = request.form['preco_diaria']
        
        connection = database.create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute('''
                    INSERT INTO veiculos (marca, modelo, ano, placa, preco_diaria)
                    VALUES (%s, %s, %s, %s, %s)
                ''', (marca, modelo, ano, placa, preco_diaria))
                connection.commit()
                return redirect(url_for('veiculos'))
            except Exception as e:
                return f"Erro ao cadastrar veículo: {e}"
            finally:
                cursor.close()
                connection.close()
    
    return render_template('novo_veiculo.html')

@app.route('/veiculo/editar/<int:id>', methods=['GET', 'POST'])
def editar_veiculo(id):
    connection = database.create_connection()
    if connection:
        if request.method == 'POST':
            marca = request.form['marca']
            modelo = request.form['modelo']
            ano = request.form['ano']
            placa = request.form['placa']
            preco_diaria = request.form['preco_diaria']
            disponivel = request.form.get('disponivel') == 'on'
            
            try:
                cursor = connection.cursor()
                cursor.execute('''
                    UPDATE veiculos 
                    SET marca=%s, modelo=%s, ano=%s, placa=%s, preco_diaria=%s, disponivel=%s
                    WHERE id=%s
                ''', (marca, modelo, ano, placa, preco_diaria, disponivel, id))
                connection.commit()
                return redirect(url_for('veiculos'))
            except Exception as e:
                return f"Erro ao editar veículo: {e}"
            finally:
                cursor.close()
                connection.close()
        else:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM veiculos WHERE id = %s", (id,))
                veiculo = cursor.fetchone()
                return render_template('editar_veiculo.html', veiculo=veiculo)
            except Exception as e:
                return f"Erro ao carregar veículo: {e}"
            finally:
                cursor.close()
                connection.close()
    return "Erro de conexão com o banco"

@app.route('/veiculo/excluir/<int:id>')
def excluir_veiculo(id):
    connection = database.create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM veiculos WHERE id = %s", (id,))
            connection.commit()
            return redirect(url_for('veiculos'))
        except Exception as e:
            return f"Erro ao excluir veículo: {e}"
        finally:
            cursor.close()
            connection.close()
    return redirect(url_for('veiculos'))

# ===== ROTAS CLIENTES =====
@app.route('/clientes')
def clientes():
    connection = database.create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM clientes ORDER BY id DESC")
            clientes_data = cursor.fetchall()
            return render_template('clientes.html', clientes=clientes_data)
        except Exception as e:
            return f"Erro ao buscar clientes: {e}"
        finally:
            cursor.close()
            connection.close()
    return "Erro de conexão com o banco"

@app.route('/cliente/novo', methods=['GET', 'POST'])
def novo_cliente():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        cpf = request.form['cpf']
        endereco = request.form['endereco']
        
        connection = database.create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute('''
                    INSERT INTO clientes (nome, email, telefone, cpf, endereco)
                    VALUES (%s, %s, %s, %s, %s)
                ''', (nome, email, telefone, cpf, endereco))
                connection.commit()
                return redirect(url_for('clientes'))
            except Exception as e:
                return f"Erro ao cadastrar cliente: {e}"
            finally:
                cursor.close()
                connection.close()
    
    return render_template('novo_cliente.html')

@app.route('/cliente/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    connection = database.create_connection()
    if connection:
        if request.method == 'POST':
            nome = request.form['nome']
            email = request.form['email']
            telefone = request.form['telefone']
            cpf = request.form['cpf']
            endereco = request.form['endereco']
            
            try:
                cursor = connection.cursor()
                cursor.execute('''
                    UPDATE clientes 
                    SET nome=%s, email=%s, telefone=%s, cpf=%s, endereco=%s
                    WHERE id=%s
                ''', (nome, email, telefone, cpf, endereco, id))
                connection.commit()
                return redirect(url_for('clientes'))
            except Exception as e:
                return f"Erro ao editar cliente: {e}"
            finally:
                cursor.close()
                connection.close()
        else:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM clientes WHERE id = %s", (id,))
                cliente = cursor.fetchone()
                return render_template('editar_cliente.html', cliente=cliente)
            except Exception as e:
                return f"Erro ao carregar cliente: {e}"
            finally:
                cursor.close()
                connection.close()
    return "Erro de conexão com o banco"

@app.route('/cliente/excluir/<int:id>')
def excluir_cliente(id):
    connection = database.create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM clientes WHERE id = %s", (id,))
            connection.commit()
            return redirect(url_for('clientes'))
        except Exception as e:
            return f"Erro ao excluir cliente: {e}"
        finally:
            cursor.close()
            connection.close()
    return redirect(url_for('clientes'))

# ===== ROTAS LOCAÇÕES =====
@app.route('/locacoes')
def locacoes():
    connection = database.create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute('''
                SELECT l.*, v.marca, v.modelo, v.placa, c.nome as cliente_nome 
                FROM locacoes l
                JOIN veiculos v ON l.veiculo_id = v.id
                JOIN clientes c ON l.cliente_id = c.id
                ORDER BY l.id DESC
            ''')
            locacoes_data = cursor.fetchall()
            return render_template('locacoes.html', locacoes=locacoes_data)
        except Exception as e:
            return f"Erro ao buscar locações: {e}"
        finally:
            cursor.close()
            connection.close()
    return "Erro de conexão com o banco"

@app.route('/locacao/nova', methods=['GET', 'POST'])
def nova_locacao():
    if request.method == 'POST':
        try:
            veiculo_id = request.form['veiculo_id']
            cliente_id = request.form['cliente_id']
            data_inicio = request.form['data_inicio']
            data_fim = request.form['data_fim']
            valor_total = request.form['valor_total']
            
            connection = database.create_connection()
            if connection:
                cursor = connection.cursor()
                cursor.execute('''
                    INSERT INTO locacoes (veiculo_id, cliente_id, data_inicio, data_fim, valor_total)
                    VALUES (%s, %s, %s, %s, %s)
                ''', (veiculo_id, cliente_id, data_inicio, data_fim, valor_total))
                
                # Marcar veículo como indisponível
                cursor.execute("UPDATE veiculos SET disponivel = FALSE WHERE id = %s", (veiculo_id,))
                
                connection.commit()
                cursor.close()
                connection.close()
                return redirect(url_for('locacoes'))
            else:
                return "Erro de conexão com o banco"
                
        except Exception as e:
            return f"Erro ao criar locação: {e}"
    
    # GET - Carregar veículos e clientes para o formulário
    connection = database.create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            
            # Buscar veículos disponíveis
            cursor.execute("SELECT * FROM veiculos WHERE disponivel = TRUE")
            veiculos = cursor.fetchall()
            
            # Buscar todos os clientes
            cursor.execute("SELECT * FROM clientes")
            clientes = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            return render_template('nova_locacao.html', veiculos=veiculos, clientes=clientes)
            
        except Exception as e:
            return f"Erro ao carregar dados: {e}"
    else:
        return "Erro de conexão com o banco"

# ===== API PARA BUSCAR DADOS =====
@app.route('/api/veiculos/disponiveis')
def api_veiculos_disponiveis():
    connection = database.create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM veiculos WHERE disponivel = TRUE")
            veiculos = cursor.fetchall()
            return jsonify(veiculos)
        except Exception as e:
            return jsonify({'error': str(e)})
        finally:
            cursor.close()
            connection.close()
    return jsonify({'error': 'Erro de conexão'})

# ===== ROTAS PARA FINALIZAR E CANCELAR LOCAÇÕES =====
@app.route('/locacao/finalizar/<int:id>')
def finalizar_locacao(id):
    connection = database.create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Buscar veículo_id da locação
            cursor.execute("SELECT veiculo_id FROM locacoes WHERE id = %s", (id,))
            resultado = cursor.fetchone()
            
            if resultado:
                veiculo_id = resultado[0]
                # Finalizar locação
                cursor.execute("UPDATE locacoes SET status = 'finalizada' WHERE id = %s", (id,))
                # Liberar veículo
                cursor.execute("UPDATE veiculos SET disponivel = TRUE WHERE id = %s", (veiculo_id,))
                connection.commit()
                print(f"✅ Locação {id} finalizada e veículo liberado")
            
            cursor.close()
            connection.close()
            return redirect(url_for('locacoes'))
            
        except Exception as e:
            return f"Erro ao finalizar locação: {e}"
    return redirect(url_for('locacoes'))

@app.route('/locacao/cancelar/<int:id>')
def cancelar_locacao(id):
    connection = database.create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Buscar veículo_id da locação
            cursor.execute("SELECT veiculo_id FROM locacoes WHERE id = %s", (id,))
            resultado = cursor.fetchone()
            
            if resultado:
                veiculo_id = resultado[0]
                # Cancelar locação
                cursor.execute("UPDATE locacoes SET status = 'cancelada' WHERE id = %s", (id,))
                # Liberar veículo
                cursor.execute("UPDATE veiculos SET disponivel = TRUE WHERE id = %s", (veiculo_id,))
                connection.commit()
                print(f"✅ Locação {id} cancelada e veículo liberado")
            
            cursor.close()
            connection.close()
            return redirect(url_for('locacoes'))
            
        except Exception as e:
            return f"Erro ao cancelar locação: {e}"
    return redirect(url_for('locacoes'))

# ===== ROTA PARA BUSCAR INFORMAÇÕES DE VEÍCULOS =====
@app.route('/api/veiculo/<int:id>')
def api_veiculo_info(id):
    connection = database.create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM veiculos WHERE id = %s", (id,))
            veiculo = cursor.fetchone()
            cursor.close()
            connection.close()
            return jsonify(veiculo)
        except Exception as e:
            return jsonify({'error': str(e)})
    return jsonify({'error': 'Erro de conexão'})

if __name__ == '__main__':
    # Inicializar banco de dados
    database.init_database()
    
    # Executar aplicação
    app.run(debug=True)