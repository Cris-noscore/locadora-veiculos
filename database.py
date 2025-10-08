import mysql.connector
from mysql.connector import Error

def create_connection():
    """Cria conexão com o Azure MySQL"""
    try:
        # Conectar diretamente ao database
        connection = mysql.connector.connect(
            host='server-bd-cn1.mysql.database.azure.com',
            database='locadora_veiculos',
            user='useradmin',
            password='admin@123',
            port=3306
        )
        return connection
    except Error as e:
        print(f"❌ Erro ao conectar: {e}")
        return None

def init_database():
    """Inicializa o banco e cria tabelas se não existirem"""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Tabela de veículos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS veiculos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    marca VARCHAR(100) NOT NULL,
                    modelo VARCHAR(100) NOT NULL,
                    ano INT NOT NULL,
                    placa VARCHAR(10) UNIQUE NOT NULL,
                    preco_diaria DECIMAL(10,2) NOT NULL,
                    disponivel BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabela de clientes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(200) NOT NULL,
                    email VARCHAR(200) UNIQUE NOT NULL,
                    telefone VARCHAR(20),
                    cpf VARCHAR(14) UNIQUE NOT NULL,
                    endereco TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabela de locações
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS locacoes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    veiculo_id INT,
                    cliente_id INT,
                    data_inicio DATE NOT NULL,
                    data_fim DATE NOT NULL,
                    valor_total DECIMAL(10,2) NOT NULL,
                    status ENUM('ativa', 'finalizada', 'cancelada') DEFAULT 'ativa',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (veiculo_id) REFERENCES veiculos(id),
                    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
                )
            ''')
            
            connection.commit()
            print("✅ Tabelas criadas/verificadas com sucesso!")
            
        except Error as e:
            print(f"Erro ao criar tabelas: {e}")
        finally:
            cursor.close()
            connection.close()