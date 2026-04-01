import json
import os
from models.livro import Livro

CAMINHO_DADOS = os.path.join(os.path.dirname(__file__), "../data/livros.json")

# Acervo inicial carregado automaticamente na primeira execução
LIVROS_INICIAIS = [
    {
        "isbn": "978-85-7522-847-5",
        "titulo": "Engenharia de Software",
        "autor": "Roger Pressman",
        "categoria": "Engenharia",
        "disponivel": True
    },
    {
        "isbn": "978-85-352-3523-7",
        "titulo": "Clean Code",
        "autor": "Robert C. Martin",
        "categoria": "Programação",
        "disponivel": True
    },
    {
        "isbn": "978-85-7522-123-0",
        "titulo": "Introdução aos Algoritmos",
        "autor": "Cormen et al.",
        "categoria": "Algoritmos",
        "disponivel": True
    },
    {
        "isbn": "978-85-430-0855-9",
        "titulo": "Padrões de Projeto",
        "autor": "Gang of Four",
        "categoria": "Arquitetura",
        "disponivel": True
    },
    {
        "isbn": "978-85-7639-484-5",
        "titulo": "Python Fluente",
        "autor": "Luciano Ramalho",
        "categoria": "Programação",
        "disponivel": True
    },
    {
        "isbn": "978-85-352-8023-7",
        "titulo": "Banco de Dados",
        "autor": "Abraham Silberschatz",
        "categoria": "Banco de Dados",
        "disponivel": True
    },
    {
        "isbn": "978-85-7783-123-4",
        "titulo": "Redes de Computadores",
        "autor": "Andrew Tanenbaum",
        "categoria": "Redes",
        "disponivel": True
    },
    {
        "isbn": "978-85-7532-456-7",
        "titulo": "Estruturas de Dados",
        "autor": "Tenenbaum et al.",
        "categoria": "Algoritmos",
        "disponivel": True
    },
]


class LivroService:
    def __init__(self):
        self._garantir_dados()

    def _garantir_dados(self):
        """Cria o arquivo JSON com dados iniciais se não existir."""
        os.makedirs(os.path.dirname(CAMINHO_DADOS), exist_ok=True)
        if not os.path.exists(CAMINHO_DADOS):
            with open(CAMINHO_DADOS, "w", encoding="utf-8") as f:
                json.dump(LIVROS_INICIAIS, f, ensure_ascii=False, indent=2)

    def _carregar(self) -> list[dict]:
        """Lê todos os livros do arquivo JSON."""
        with open(CAMINHO_DADOS, "r", encoding="utf-8") as f:
            return json.load(f)

    def _salvar(self, livros: list[dict]):
        """Persiste a lista de livros no arquivo JSON."""
        with open(CAMINHO_DADOS, "w", encoding="utf-8") as f:
            json.dump(livros, f, ensure_ascii=False, indent=2)

    def buscar(self, termo: str) -> list[dict]:
        """
        RF-01: Busca livros por título ou autor (case-insensitive).
        Retorna lista de livros que contêm o termo buscado.
        """
        termo = termo.lower()
        livros = self._carregar()
        return [
            l for l in livros
            if termo in l["titulo"].lower() or termo in l["autor"].lower()
        ]

    def buscar_por_isbn(self, isbn: str) -> dict | None:
        """RF-07: Retorna os dados de um livro a partir do ISBN. Retorna None se não encontrado."""
        for livro in self._carregar():
            if livro["isbn"] == isbn:
                return livro
        return None

    def listar_disponiveis(self) -> list[dict]:
        """RF-05: Lista todos os livros com status disponível no acervo."""
        return [l for l in self._carregar() if l["disponivel"]]

    def atualizar_disponibilidade(self, isbn: str, disponivel: bool) -> bool:
        """
        Atualiza o status de disponibilidade de um livro.
        Chamado internamente pelo EmprestimoService ao emprestar ou devolver.
        Retorna True se o livro foi encontrado e atualizado.
        """
        livros = self._carregar()
        for livro in livros:
            if livro["isbn"] == isbn:
                livro["disponivel"] = disponivel
                self._salvar(livros)
                return True
        return False
