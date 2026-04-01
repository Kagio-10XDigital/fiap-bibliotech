class Livro:
    def __init__(self, isbn: str, titulo: str, autor: str, categoria: str, disponivel: bool = True):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.disponivel = disponivel

    def to_dict(self) -> dict:
        return {
            "isbn": self.isbn,
            "titulo": self.titulo,
            "autor": self.autor,
            "categoria": self.categoria,
            "disponivel": self.disponivel
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Livro":
        return cls(
            isbn=data["isbn"],
            titulo=data["titulo"],
            autor=data["autor"],
            categoria=data["categoria"],
            disponivel=data.get("disponivel", True)
        )

    def __str__(self) -> str:
        status = "Disponível" if self.disponivel else "Emprestado"
        return f"[{self.isbn}] {self.titulo} — {self.autor} ({self.categoria}) | {status}"
