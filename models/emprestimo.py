from datetime import datetime, timedelta


class Emprestimo:
    PRAZO_DIAS = 14

    def __init__(self, ra: str, isbn: str, titulo: str,
                 data_emprestimo: str = None, prazo_devolucao: str = None):
        self.ra = ra
        self.isbn = isbn
        self.titulo = titulo
        hoje = datetime.now()
        self.data_emprestimo = data_emprestimo or hoje.strftime("%d/%m/%Y")
        self.prazo_devolucao = prazo_devolucao or (
            hoje + timedelta(days=self.PRAZO_DIAS)
        ).strftime("%d/%m/%Y")

    @property
    def atrasado(self) -> bool:
        prazo = datetime.strptime(self.prazo_devolucao, "%d/%m/%Y")
        return datetime.now() > prazo

    def dias_restantes(self) -> int:
        prazo = datetime.strptime(self.prazo_devolucao, "%d/%m/%Y")
        delta = prazo - datetime.now()
        return delta.days

    def to_dict(self) -> dict:
        return {
            "ra": self.ra,
            "isbn": self.isbn,
            "titulo": self.titulo,
            "data_emprestimo": self.data_emprestimo,
            "prazo_devolucao": self.prazo_devolucao,
            "atrasado": self.atrasado
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Emprestimo":
        return cls(
            ra=data["ra"],
            isbn=data["isbn"],
            titulo=data["titulo"],
            data_emprestimo=data["data_emprestimo"],
            prazo_devolucao=data["prazo_devolucao"]
        )

    def __str__(self) -> str:
        status = "ATRASADO" if self.atrasado else f"{self.dias_restantes()} dia(s) restantes"
        return (
            f"Livro: {self.titulo} | RA: {self.ra} | "
            f"Prazo: {self.prazo_devolucao} | {status}"
        )
