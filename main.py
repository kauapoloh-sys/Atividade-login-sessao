import bcrypt
from banco import conectar
from usuario import Usuario
from sessao import Sessao

while True:

    if not Sessao.autenticado():

        print("\n=== MENU INICIAL ===")
        print("1 - Cadastrar")
        print("2 - Login")
        print("3 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":

            nome = input("Nome: ").strip()
            email = input("Email: ").strip()
            senha = input("Senha: ").strip()

            if not nome or not email or not senha:
                print("Todos os campos são obrigatórios!")
                continue

            senha_hash = bcrypt.hashpw(
                senha.encode(),
                bcrypt.gensalt()
            )

            try:

                conexao = conectar()
                cursor = conexao.cursor()

                sql_verifica = """
                SELECT id
                FROM usuarios
                WHERE email = %s
                """

                cursor.execute(sql_verifica, (email,))

                if cursor.fetchone():

                    print("E-mail já cadastrado!")

                else:

                    sql = """
                    INSERT INTO usuarios(nome,email,senha)
                    VALUES(%s,%s,%s)
                    """

                    cursor.execute(
                        sql,
                        (
                            nome,
                            email,
                            senha_hash.decode()
                        )
                    )

                    conexao.commit()

                    usuario = Usuario(
                        cursor.lastrowid,
                        nome,
                        email
                    )

                    Sessao.iniciar(usuario)

                    print("Usuário cadastrado com sucesso!")
                    print("Sessão iniciada automaticamente!")

            except Exception as erro:

                print("Erro:", erro)

            finally:

                cursor.close()
                conexao.close()

        elif opcao == "2":

            tentativas = 0

            while tentativas < 5:

                email_login = input("Digite o email: ")
                senha_login = input("Digite a senha: ")

                try:

                    conexao = conectar()
                    cursor = conexao.cursor()

                    sql = """
                    SELECT id,nome,email,senha
                    FROM usuarios
                    WHERE email = %s
                    """

                    cursor.execute(
                        sql,
                        (email_login,)
                    )

                    usuario = cursor.fetchone()

                    if usuario:

                        senha_hash = usuario[3]

                        if bcrypt.checkpw(
                            senha_login.encode(),
                            senha_hash.encode()
                        ):

                            usuario_logado = Usuario(
                                usuario[0],
                                usuario[1],
                                usuario[2]
                            )

                            Sessao.iniciar(
                                usuario_logado
                            )

                            print(
                                "Login realizado com sucesso!"
                            )

                            break

                    tentativas += 1

                    print(
                        f"Credenciais inválidas! "
                        f"Tentativa {tentativas}/5"
                    )

                except Exception as erro:

                    print("Erro:", erro)

                finally:

                    cursor.close()
                    conexao.close()

            if tentativas == 5:
                print("Limite de tentativas atingido!")

        elif opcao == "3":

            print("Programa encerrado!")
            break

        else:

            print("Opção inválida!")

    else:

        usuario = Sessao.obter_usuario()

        print("\n=== USUÁRIO AUTENTICADO ===")
        print("Nome:", usuario.nome)
        print("Email:", usuario.email)

        print("\n1 - Ver dados")
        print("2 - Encerrar sessão")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":

            print("\n=== DADOS DO USUÁRIO ===")
            print("ID:", usuario.id)
            print("Nome:", usuario.nome)
            print("Email:", usuario.email)

        elif opcao == "2":

            Sessao.encerrar()

            print("Sessão encerrada com sucesso!")

        else:

            print("Opção inválida!")