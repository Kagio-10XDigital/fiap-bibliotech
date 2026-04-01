import json
import os
from models.emprestimo import Emprestimo

CAMINHO_DADOS = os.path.join(os.path.dirname(__file__), "../data/emprestimos.json")
LIMITE_EMPRESTIMOS = 3  # máximo de empréstimos simultâneos por aluno (RNF)


class EmprestimoService:
    def __init__(self, livro_service, usuario_service):
        self.livro_service = livro_service
        self.usuario_service = usuario_service
        self._garantir_dados()

    def _garantir_dados(self):
        """Cria o arquivo JSON vazio se não existir."""
        os.makedirs(os.path.dirname(CAMINHO_DADOS), exist_ok=True)
        if not os.path.exists(CAMINHO_DADOS):
            with open(CAMINHO_DADOS, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _carregar(self) -> list[dict]:
        """Lê todos os empréstimos ativos do arquivo JSON."""
        with open(CAMINHO_DADOS, "r", encoding="utf-8") as f:
            return json.load(f)

    def _salvar(self, emprestimos: list[dict]):
        """Persiste a lista de empréstimos no arquivo JSON."""
        with open(CAMINHO_DADOS, "w", encoding="utf-8") as f:
            json.dump(emprestimos, f, ensure_ascii=False, indent=2)

    def realizar_emprestimo(self, ra: str, isbn: str) -> tuple[bool, str]:
        """
        RF-02: Registra o empréstimo de um livro para um aluno.
        Regras de negócio:
          - Aluno deve estar cadastrado e ativo
          - Livro deve existir e estar disponível
          - Aluno não pode ultrapassar o limite de empréstimos simultâneos
          - Aluno não pode ter o mesmo livro emprestado duas vezes
        Retorna tupla (sucesso: bool, mensagem: str).
        """
        # Verifica se o usuário está cadastrado e ativo
        usuario = self.usuario_service.buscar_por_ra(ra)
        if not usuario:
            return False, f"RA {ra} não encontrado. Realize o cadastro primeiro (opção 6)."
        if not usuario["ativo"]:
            return False, "Usuário inativo. Procure o balcão da biblioteca."

        # Verifica se o livro existe e está disponível
        livro = self.livro_service.buscar_por_isbn(isbn)
        if not livro:
            return False, f"Livro com ISBN {isbn} não encontrado no acervo."
        if not livro["disponivel"]:
            return False, f"'{livro['titulo']}' está indisponível no momento."

        # Verifica limite de empréstimos simultâneos
        emprestimos_ativos = self.listar_por_usuario(ra)
        if len(emprestimos_ativos) >= LIMITE_EMPRESTIMOS:
            return False, (
                f"Limite de {LIMITE_EMPRESTIMOS} empréstimos simultâneos atingido. "
                "Devolva um livro antes de realizar novo empréstimo."
            )

        # Verifica se o aluno já tem esse livro
        if any(e["isbn"] == isbn for e in emprestimos_ativos):
            return False, "Você já está com esse livro emprestado."

        # Registra o empréstimo e atualiza disponibilidade
        emprestimo = Emprestimo(ra=ra, isbn=isbn, titulo=livro["titulo"])
        emprestimos = self._carregar()
        emprestimos.append(emprestimo.to_dict())
        self._salvar(emprestimos)
        self.livro_service.atualizar_disponibilidade(isbn, False)

        return True, (
            f"Empréstimo realizado com sucesso!\n"
            f"  Livro: {livro['titulo']}\n"
            f"  Data: {emprestimo.data_emprestimo}\n"
            f"  Prazo de devolução: {emprestimo.prazo_devolucao}"
        )

    def devolver_livro(self, ra: str, isbn: str) -> tuple[bool, str]:
        """
        RF-03: Registra a devolução de um livro e libera o acervo.
        Retorna tupla (sucesso: bool, mensagem: str).
        """
        emprestimos = self._carregar()
        emprestimo_encontrado = None

        for emp in emprestimos:
            if emp["ra"] == ra and emp["isbn"] == isbn:
                emprestimo_encontrado = emp
                break

        if not emprestimo_encontrado:
            return False, "Empréstimo não encontrado. Verifique o RA e o ISBN informados."

        # Remove o empréstimo e libera o livro no acervo
        emprestimos.remove(emprestimo_encontrado)
        self._salvar(emprestimos)
        self.livro_service.atualizar_disponibilidade(isbn, True)

        titulo = emprestimo_encontrado["titulo"]
        return True, f"Devolução de '{titulo}' registrada com sucesso. Obrigado!"

    def listar_por_usuario(self, ra: str) -> list[dict]:
        """
        RF-04: Lista todos os empréstimos ativos de um aluno.
        RF-08: O campo 'atrasado' detecta automaticamente empréstimos vencidos.
        """
        return [
            Emprestimo.from_dict(e).to_dict()
            for e in self._carregar()
            if e["ra"] == ra
        ]
