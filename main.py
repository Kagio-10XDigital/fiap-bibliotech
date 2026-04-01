from services.emprestimo_service import EmprestimoService
from services.livro_service import LivroService
from services.usuario_service import UsuarioService


def menu_principal():
    print("\n" + "="*50)
    print("       📚 FIAP BiblioTech")
    print("   Sistema de Empréstimo de Livros")
    print("="*50)
    print("1. 📖  Buscar livro")
    print("2. 📤  Realizar empréstimo")
    print("3. 📥  Devolver livro")
    print("4. 📋  Meus empréstimos")
    print("5. 📊  Livros disponíveis")
    print("6. 👤  Cadastrar usuário")
    print("7. 🔍  Verificar livro por ISBN")
    print("0. ❌  Sair")
    print("-"*50)
    return input("Escolha uma opção: ").strip()


def main():
    livro_service = LivroService()
    usuario_service = UsuarioService()
    emprestimo_service = EmprestimoService(livro_service, usuario_service)

    print("\nBem-vindo ao FIAP BiblioTech!")

    while True:
        opcao = menu_principal()

        if opcao == "1":
            # RF-01: Buscar livro por título ou autor
            termo = input("\nDigite o título ou autor: ").strip()
            if not termo:
                print("❌ Termo de busca não pode ser vazio.")
                continue
            resultados = livro_service.buscar(termo)
            if resultados:
                print(f"\n📚 {len(resultados)} livro(s) encontrado(s):\n")
                for livro in resultados:
                    status = "✅ Disponível" if livro["disponivel"] else "❌ Emprestado"
                    print(f"  ISBN: {livro['isbn']}")
                    print(f"  Título: {livro['titulo']}")
                    print(f"  Autor: {livro['autor']}")
                    print(f"  Status: {status}")
                    print(f"  Categoria: {livro['categoria']}")
                    print()
            else:
                print("❌ Nenhum livro encontrado.")

        elif opcao == "2":
            # RF-02: Realizar empréstimo
            ra = input("\nDigite seu RA (ex: RM123456): ").strip().upper()
            isbn = input("Digite o ISBN do livro: ").strip()
            sucesso, mensagem = emprestimo_service.realizar_emprestimo(ra, isbn)
            print(f"\n{'✅' if sucesso else '❌'} {mensagem}")

        elif opcao == "3":
            # RF-03: Devolver livro
            ra = input("\nDigite seu RA: ").strip().upper()
            isbn = input("Digite o ISBN do livro a devolver: ").strip()
            sucesso, mensagem = emprestimo_service.devolver_livro(ra, isbn)
            print(f"\n{'✅' if sucesso else '❌'} {mensagem}")

        elif opcao == "4":
            # RF-04: Consultar empréstimos do usuário
            ra = input("\nDigite seu RA: ").strip().upper()
            emprestimos = emprestimo_service.listar_por_usuario(ra)
            if emprestimos:
                print(f"\n📋 Empréstimos ativos de {ra}:\n")
                for emp in emprestimos:
                    print(f"  Livro: {emp['titulo']}")
                    print(f"  ISBN: {emp['isbn']}")
                    print(f"  Data de empréstimo: {emp['data_emprestimo']}")
                    print(f"  Prazo de devolução: {emp['prazo_devolucao']}")
                    atrasado = emp.get("atrasado", False)
                    print(f"  Status: {'⚠️  ATRASADO' if atrasado else '🟢 No prazo'}")
                    print()
            else:
                print("ℹ️  Nenhum empréstimo ativo encontrado.")

        elif opcao == "5":
            # RF-05: Listar livros disponíveis
            livros = livro_service.listar_disponiveis()
            print(f"\n📚 {len(livros)} livro(s) disponível(is):\n")
            for livro in livros:
                print(f"  [{livro['isbn']}] {livro['titulo']} — {livro['autor']} ({livro['categoria']})")

        elif opcao == "6":
            # RF-06: Cadastrar usuário
            ra = input("\nDigite o RA do aluno (ex: RM123456): ").strip().upper()
            nome = input("Nome completo: ").strip()
            email = input("E-mail FIAP (@fiap.com.br): ").strip().lower()
            curso = input("Curso: ").strip()
            sucesso, mensagem = usuario_service.cadastrar(ra, nome, email, curso)
            print(f"\n{'✅' if sucesso else '❌'} {mensagem}")

        elif opcao == "7":
            # RF-07: Verificar detalhes de um livro por ISBN
            isbn = input("\nDigite o ISBN: ").strip()
            livro = livro_service.buscar_por_isbn(isbn)
            if livro:
                print(f"\n📖 Detalhes do livro:")
                for chave, valor in livro.items():
                    print(f"  {chave.capitalize()}: {valor}")
            else:
                print("❌ Livro não encontrado.")

        elif opcao == "0":
            print("\n👋 Até logo! Bons estudos!\n")
            break

        else:
            print("❌ Opção inválida. Tente novamente.")

        input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
    main()