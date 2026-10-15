# Testes manuais do Task Tracker CLI

Este arquivo será utilizado para registrar os testes manuais realizados durante o desenvolvimento.

Checkpoint 1:

Comandos planejados
add
update
delete
mark-in-progress
mark-done
list
list todo
list in-progress
list done
Regras iniciais
Toda nova tarefa começa com o status todo.
O ID deve ser um número inteiro positivo e único.
IDs excluídos não serão reutilizados.
A descrição não pode ser vazia.

O arquivo tasks.json deve ser criado automaticamente.

Checkpoint 2: estrutura da CLI e armazenamento JSON

Inicialização
Executar a aplicação sem argumentos.
Mostrar a ajuda geral.
Criar tasks.json automaticamente.
Criar tasks.json com uma lista vazia.
Comandos
Reconhecer add.
Reconhecer update.
Reconhecer delete.
Reconhecer mark-in-progress.
Reconhecer mark-done.
Reconhecer list.
Listagem
Listar todas as tarefas.
Filtrar pelo status todo.
Filtrar pelo status in-progress.
Filtrar pelo status done.
Rejeitar um filtro inválido.
Arquivo JSON
Ler uma lista vazia.
Rejeitar um arquivo vazio.
Rejeitar um JSON inválido.
Rejeitar uma estrutura principal que não seja lista.
Rejeitar uma tarefa sem campos obrigatórios.
Rejeitar tarefas com IDs duplicados.
Criar tasks.json automaticamente.
