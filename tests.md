# Testes manuais do Task Tracker CLI

Este arquivo será utilizado para registrar os testes manuais realizados durante o desenvolvimento.

XXXXXXX Checkpoint 1: XXXXXXXX

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

XXXXXXXX Checkpoint 2: estrutura da CLI e armazenamento JSON XXXXXXXXX

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

Argumentos do comando add
Reconhecer o comando add.
Receber uma descrição entre aspas.
Aceitar descrição com várias palavras.
Aceitar descrição com acentos.
Rejeitar descrição ausente.
Mostrar ajuda com add --help.

XXXXXX Checkpoint 3: adição de tarefas XXXXXXXX

Estrutura e execução
Validar a sintaxe de task_cli.py.
Instanciar TaskService com JsonTaskRepository.
Executar o comando add com uma descrição.
Executar o comando list.

Criação

Adicionar a primeira tarefa com ID 1.
Adicionar a segunda tarefa com ID 2.
Salvar o status inicial como todo.
Salvar createdAt.
Salvar updatedAt.
Manter createdAt e updatedAt iguais na criação.

Descrição

Remover espaços do início e do fim.
Rejeitar uma descrição vazia.
Rejeitar uma descrição formada somente por espaços.
Preservar caracteres acentuados.

Listagem

Listar todas as tarefas.
Listar tarefas com status todo.
Retornar lista vazia para done.
Retornar lista vazia para in-progress.

XXXXXXX Checkpoint 4: alteração de status XXXXXXXXX

Mark in progress
Receber um ID inteiro.
Marcar uma tarefa todo como in-progress.
Preservar o ID.
Preservar a descrição.
Preservar createdAt.
Atualizar updatedAt.
Exibir a tarefa em list in-progress.
Remover a tarefa do resultado de list todo.
Mark done
Receber um ID inteiro.
Marcar uma tarefa como done.
Preservar o ID.
Preservar a descrição.
Preservar createdAt.
Atualizar updatedAt.
Exibir a tarefa em list done.
Remover a tarefa do status anterior.
Validações
Rejeitar ID igual a zero.
Rejeitar ID negativo.
Rejeitar ID não numérico.
Rejeitar ID ausente.
Tratar tarefa inexistente.
Impedir a aplicação repetida do mesmo status.
Não modificar o JSON quando ocorrer erro.

Checkpoint 5: atualização de tarefas

Atualização válida
Atualizar a descrição pelo ID.
Preservar o ID.
Preservar o status.
Preservar createdAt.
Atualizar updatedAt.
Persistir a alteração em tasks.json.
Descrição
Remover espaços do início e do final.
Rejeitar descrição vazia.
Rejeitar descrição composta somente por espaços.
Preservar acentos e caracteres especiais.
Rejeitar atualização com a descrição atual.
Não alterar updatedAt quando a descrição não mudar.
Identificação
Rejeitar ID igual a zero.
Rejeitar ID negativo.
Rejeitar ID não numérico.
Rejeitar ID ausente.
Tratar ID inexistente.
Integridade
Não alterar outras tarefas.
Não modificar o JSON quando ocorrer erro.
