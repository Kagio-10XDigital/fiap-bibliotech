# 📚 FIAP BiblioTech

> Sistema de Empréstimo de Livros para a biblioteca da FIAP — desenvolvido como protótipo funcional para o Checkpoint 1 de Engenharia de Software.

---

## 🎯 Descrição do Problema

A biblioteca da FIAP ainda opera com processos manuais ou pouco integrados: alunos não sabem quais livros estão disponíveis sem ir até o balcão, funcionários controlam empréstimos em planilhas, e não há como verificar prazos de devolução remotamente. Isso gera filas, atrasos e perda de livros.

---

## 💡 Solução Proposta

O **FIAP BiblioTech** é um sistema via terminal que digitaliza o núcleo do processo de empréstimo de livros da biblioteca, permitindo:

- Buscar livros por título ou autor
- Realizar e registrar empréstimos com controle de prazo
- Registrar devoluções
- Consultar empréstimos ativos e identificar atrasos
- Cadastrar novos alunos com validação de RA e e-mail institucional

Todos os dados são persistidos em arquivos `.json`, simulando um banco de dados simples.

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia      | Uso                            |
| --------------- | ------------------------------ |
| Python 3.11+    | Linguagem principal            |
| JSON            | Persistência de dados          |
| Módulos nativos | `os`, `json`, `re`, `datetime` |

---

## ▶️ Como Executar

### Pré-requisitos

- Python 3.11 ou superior instalado

### Passos

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/fiap-bibliotech.git
cd fiap-bibliotech

# Execute o sistema
python3 main.py
```

> Não é necessário instalar dependências externas. O sistema cria os arquivos de dados automaticamente na primeira execução.

---

## 🗂️ Estrutura do Projeto

```
fiap-bibliotech/
│
├── main.py                    # Ponto de entrada — menu interativo
│
├── models/
│   ├── livro.py               # Entidade Livro
│   ├── usuario.py             # Entidade Usuário (Aluno)
│   └── emprestimo.py          # Entidade Empréstimo (com cálculo de prazo)
│
├── services/
│   ├── livro_service.py       # CRUD e busca de livros
│   ├── usuario_service.py     # Cadastro e validação de alunos
│   └── emprestimo_service.py  # Lógica de empréstimo e devolução
│
├── data/                      # Gerado automaticamente na 1ª execução
│   ├── livros.json
│   ├── usuarios.json
│   └── emprestimos.json
│
└── README.md
```

---

## ✅ Funcionalidades Implementadas

| #   | Caso de Uso                     | Requisito | Status |
| --- | ------------------------------- | --------- | ------ |
| 1   | Buscar livro por título/autor   | RF-01     | ✅     |
| 2   | Realizar empréstimo             | RF-02     | ✅     |
| 3   | Devolver livro                  | RF-03     | ✅     |
| 4   | Consultar empréstimos ativos    | RF-04     | ✅     |
| 5   | Listar livros disponíveis       | RF-05     | ✅     |
| 6   | Cadastrar usuário com validação | RF-06     | ✅     |
| 7   | Verificar livro por ISBN        | RF-07     | ✅     |
| 8   | Alertar empréstimos em atraso   | RF-08     | ✅     |

**Regras de negócio implementadas:**

- Limite de 3 empréstimos simultâneos por aluno
- Prazo de devolução de 14 dias corridos
- Validação de RA (formato `RM` + 6 dígitos)
- Validação de e-mail institucional (`@fiap.com.br`)
- Detecção automática de empréstimos em atraso
- Controle de disponibilidade de livros em tempo real

---

## 🎬 Demonstração

[![Assista ao vídeo](https://img.youtube.com/vi/ISCdRxfc0jM/0.jpg)](https://youtu.be/ISCdRxfc0jM)

### Exemplo de fluxo — Realizar Empréstimo:

```
========================================
       📚 FIAP BiblioTech
   Sistema de Empréstimo de Livros
========================================
Escolha uma opção: 2

Digite seu RA (ex: RM123456): RM123456
Digite o ISBN do livro: 978-85-7522-847-5

✅ Empréstimo realizado com sucesso!
  Livro: Engenharia de Software
  Data: 31/03/2026
  Prazo de devolução: 14/04/2026
```

---

## 👥 Integrantes do Grupo

| Nome            | RM       | GitHub              |
| --------------- | -------- | ------------------- |
| Kagio Miura     | RM559212 | [@Kagio-miura]      |
| Rodrigo Arantes | RM557594 | [@RodrigoPhilippi]  |
| Henrique Khouri | RM555572 | [@12345-oss]        |
| Juan Alberto    | RM559744 | [@juanitolen]       |
| Celso Singh     | RM565643 | [@celsoferrersingh] |

---

## 🔗 Links

| Recurso               | URL                                                                   |
| --------------------- | --------------------------------------------------------------------- |
| 📁 Repositório GitHub | [github.com/seu-usuario/fiap-bibliotech]                              |
| 🗂️ Board no Miro      | [https://miro.com/app/board/uXjVJpRiiXQ=/?share_link_id=113218780266] |

---

_Checkpoint 1 — Engenharia de Software · FIAP · Prof. Hercules Ramos · 2026_
