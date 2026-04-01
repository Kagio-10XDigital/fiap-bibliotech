import json
import os
import re

CAMINHO_DADOS = os.path.join(os.path.dirname(__file__), "../data/usuarios.json")

# Usuários pré-cadastrados para testes
USUARIOS_INICIAIS = [
    {
        "ra": "RM123456",
        "nome": "João Silva",
        "email": "rm123456@fiap.com.br",
        "curso": "Engenharia de Computação",
        "ativo": True
    },
    {
        "ra": "RM654321",
        "nome": "Maria Souza",
        "email": "rm654321@fiap.com.br",
        "curso": "Análise e Desenvolvimento de Sistemas",
        "ativo": True
    },
]


class UsuarioService:
    def __init__(self):
        self._garantir_dados()

    def _garantir_dados(self):
        """Cria o arquivo JSON com dados iniciais se não existir."""
        os.makedirs(os.path.dirname(CAMINHO_DADOS), exist_ok=True)
        if not os.path.exists(CAMINHO_DADOS):
            with open(CAMINHO_DADOS, "w", encoding="utf-8") as f:
                json.dump(USUARIOS_INICIAIS, f, ensure_ascii=False, indent=2)

    def _carregar(self) -> list[dict]:
        """Lê todos os usuários do arquivo JSON."""
        with open(CAMINHO_DADOS, "r", encoding="utf-8") as f:
            return json.load(f)

    def _salvar(self, usuarios: list[dict]):
        """Persiste a lista de usuários no arquivo JSON."""
        with open(CAMINHO_DADOS, "w", encoding="utf-8") as f:
            json.dump(usuarios, f, ensure_ascii=False, indent=2)

    def buscar_por_ra(self, ra: str) -> dict | None:
        """Retorna os dados de um usuário pelo RA. Retorna None se não encontrado."""
        for u in self._carregar():
            if u["ra"] == ra:
                return u
        return None

    def cadastrar(self, ra: str, nome: str, email: str, curso: str) -> tuple[bool, str]:
        """
        RF-06: Cadastra um novo aluno com validações de entrada.
        Validações:
          - RA no formato RM seguido de 6 dígitos (ex: RM123456)
          - Nome com pelo menos 3 caracteres
          - E-mail institucional @fiap.com.br
          - Curso não pode ser vazio
          - RA não pode ser duplicado
        Retorna tupla (sucesso: bool, mensagem: str).
        """
        # Valida formato do RA
        if not re.match(r"^RM\d{6}$", ra):
            return False, "RA inválido. Use o formato RM seguido de 6 dígitos (ex: RM123456)."

        # Valida nome
        if not nome or len(nome.strip()) < 3:
            return False, "Nome inválido. Informe o nome completo."

        # Valida e-mail institucional
        if not email.endswith("@fiap.com.br"):
            return False, "E-mail deve ser institucional (@fiap.com.br)."

        # Valida curso
        if not curso or len(curso.strip()) == 0:
            return False, "Curso não pode ser vazio."

        # Verifica duplicidade de RA
        usuarios = self._carregar()
        if any(u["ra"] == ra for u in usuarios):
            return False, f"RA {ra} já está cadastrado no sistema."

        # Cadastra o novo usuário
        novo_usuario = {
            "ra": ra,
            "nome": nome.strip(),
            "email": email.strip().lower(),
            "curso": curso.strip(),
            "ativo": True
        }
        usuarios.append(novo_usuario)
        self._salvar(usuarios)

        return True, f"Usuário {nome} ({ra}) cadastrado com sucesso!"