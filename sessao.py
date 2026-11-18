class Sessao:

    usuario_logado = None

    @staticmethod
    def iniciar(usuario):
        Sessao.usuario_logado = usuario

    @staticmethod
    def autenticado():
        return Sessao.usuario_logado is not None

    @staticmethod
    def obter_usuario():
        return Sessao.usuario_logado

    @staticmethod
    def encerrar():
        Sessao.usuario_logado = None