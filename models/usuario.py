class Usuario:
    def __init__(self, ra: str, nome: str, email: str, curso: str, ativo: bool = True):
        self.ra = ra
        self.nome = nome
        self.email = email
        self.curso = curso
        self.ativo = ativo

    def to_dict(self) -> dict:
        return {
            "ra": self.ra,
            "nome": self.nome,
            "email": self.email,
            "curso": self.curso,
            "ativo": self.ativo
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Usuario":
        return cls(
            ra=data["ra"],
            nome=data["nome"],
            email=data["email"],
            curso=data["curso"],
            ativo=data.get("ativo", True)
        )

    def __str__(self) -> str:
        status = "Ativo" if self.ativo else "Inativo"
        return f"{self.ra} — {self.nome} ({self.curso}) | {status}"