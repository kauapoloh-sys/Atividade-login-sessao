import os
import mysql.connector
from dotenv import load_dotenv
 
#Carrega as variáveis do arquivo .env
load_dotenv()
 
class Conexao:
 
    @staticmethod
    def conectar():
 
        # Traz as configurações do banco que está no env
        host = os.getenv("DB_HOST")
        porta = os.getenv("DB_PORT")
        usuario = os.getenv("DB_USER")
        senha = os.getenv("DB_PASSWORD")
        banco = os.getenv("DB_NAME")
 
        #Verifica se as configurações obrigatórias existem
        if not all([host, porta, usuario, banco]):
            raise ValueError( "Verifique as configurações do arquivo .env")
 
        conexao = mysql.connector.connect(
            host=host,
            port=int(porta),
            user=usuario,
            password=senha,
            database=banco
        )
 
        return conexao
 
try:
    conexao=Conexao.conectar()
 
    if conexao.is_connected():
        print("Conexão realizada com sucesso")
 
except ValueError as erro:
    print(f"Erro ao conectar com o MySQL {erro}")
 
finally:
    if "conexao" in locals() and conexao.is_connected():
        conexao.close()
        print("Conexao encerrada")
       