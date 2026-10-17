#===============Task Tracker CLI. Usaremos: Python Nativo sem frameworks importados=================
#Estrutura do código abaixo:
#encapsulamento;
#abstração;
#classes.

#Bibliotécas/Libraries:=============================================================================

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from json import JSONDecodeError
from pathlib import Path
from typing import Any
from altair import Description

#Constantes:========================================================================================

VALID_STATUSES = ("todo", "in-progress", "done")
DATA_FILE_NAME = "tasks.json"

#Classe: Task=======================================================================================

class TaskTrackerError(Exception):
    """Representa um erro conhecido e tratável da aplicação."""
    
@dataclass
class Task:
    id: int
    description: str
    status: str
    createdAt: str
    updatedAt: str
#Função: Validação/Validate
    def validate(self) -> None:
        """Valida os campos da tarefa."""

        if not isinstance(self.id, int) or isinstance(self.id, bool):
            raise TaskTrackerError(
                "O ID da tarefa deve ser um número inteiro."
            )

        if self.id <= 0:
            raise TaskTrackerError(
                "O ID da tarefa deve ser maior que zero."
            )

        if not isinstance(self.description, str):
            raise TaskTrackerError(
                "A descrição da tarefa deve ser um texto."
            )

        self.description = self.description.strip()

        if not self.description:
            raise TaskTrackerError(
                "A descrição da tarefa não pode estar vazia."
            )

        if self.status not in VALID_STATUSES:
            allowed_statuses = ", ".join(VALID_STATUSES)

            raise TaskTrackerError(
                "Status inválido. "
                f"Valores permitidos: {allowed_statuses}."
            )

        if not isinstance(self.createdAt, str) or not self.createdAt:
            raise TaskTrackerError(
                "A data de criação da tarefa é inválida."
            )

        if not isinstance(self.updatedAt, str) or not self.updatedAt:
            raise TaskTrackerError(
                "A data de atualização da tarefa é inválida."
            )

    def to_dict(self) -> dict[str, Any]:
        """Transforma a tarefa em um dicionário."""

        self.validate()
        return asdict(self)
    
#Função: Dicionário/Dictionary
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Task":
        """Cria uma tarefa a partir de um dicionário."""

        required_fields = {
            "id",
            "description",
            "status",
            "createdAt",
            "updatedAt",
        }

        missing_fields = required_fields - data.keys()

        if missing_fields:
            missing_fields_text = ", ".join(sorted(missing_fields))

            raise TaskTrackerError(
                "A tarefa possui campos ausentes: "
                f"{missing_fields_text}."
            )

        task = cls(
            id=data["id"],
            description=data["description"],
            status=data["status"],
            createdAt=data["createdAt"],
            updatedAt=data["updatedAt"],
        )

        task.validate()
        return task
    
#Função: Tempo/Timestemp
def current_timestamp() -> str:
    """Retorna o instante atual em UTC e no formato ISO 8601."""

    return datetime.now(timezone.utc).isoformat()

def get_data_file_path() -> Path:
    """Retorna o caminho do tasks.json no diretório atual."""

    return Path.cwd() / DATA_FILE_NAME

#Classe: Repositório JSON/Create JSON repository====================================================

class JsonTaskRepository:
    """Controla o armazenamento das tarefas em um arquivo JSON."""
#Função: Init
    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path

#Função: Caminho/File Path
    @property
    def file_path(self) -> Path:
        """Disponibiliza o caminho do arquivo somente para leitura."""

        return self._file_path
    
#Função: Criação do arquivo JSON/Create JSON file
    def ensure_file_exists(self) -> None:
        """Cria o arquivo JSON com uma lista vazia se ele não existir."""

        if self._file_path.exists():
            return

        try:
            self._file_path.write_text(
                "[]\n",
                encoding="utf-8",
            )
        except OSError as error:
            raise TaskTrackerError(
                "Não foi possível criar o arquivo de tarefas em "
                f"'{self._file_path}'."
            ) from error
            
#Função: Carregamento/Load data
    def load(self) -> list:
        """Lê, valida e devolve todas as tarefas."""
        
        self.ensure_file_exists()

        try:
            content = self._file_path.read_text(encoding="utf-8")
        except OSError as error:
            raise TaskTrackerError(
                "Não foi possível ler o arquivo de tarefas em "
                f"'{self._file_path}'."
            ) from error

        if not content.strip():
            raise TaskTrackerError(
                "O arquivo tasks.json está vazio. "
                "O conteúdo esperado é uma lista JSON."
            )

        try:
            raw_data = json.loads(content)
        except JSONDecodeError as error:
            raise TaskTrackerError(
                "O arquivo tasks.json contém um JSON inválido."
            ) from error

        if not isinstance(raw_data, list):
            raise TaskTrackerError(
                "A estrutura principal de tasks.json deve ser uma lista."
            )

        tasks: list[Task] = []

        for position, item in enumerate(raw_data, start=1):
            if not isinstance(item, dict):
                raise TaskTrackerError(
                    f"O item {position} de tasks.json "
                    "não é um objeto válido."
                )

            try:
                task = Task.from_dict(item)
            except TaskTrackerError as error:
                raise TaskTrackerError(
                    f"Erro no item {position} de tasks.json: {error}"
                ) from error

            tasks.append(task)

        self._validate_unique_ids(tasks)

        return tasks
    
#Função: Gravação/Save tasks
    def save(self, tasks: list[Task]) -> None:
        """Valida e grava a lista completa de tarefas."""

        self._validate_unique_ids(tasks)

        serialized_tasks = [
            task.to_dict()
            for task in tasks
        ]

        try:
            content = json.dumps(
                serialized_tasks,
                ensure_ascii=False,
                indent=2,
            )

            self._file_path.write_text(
                content + "\n",
                encoding="utf-8",
            )
        except OSError as error:
            raise TaskTrackerError(
                "Não foi possível salvar o arquivo de tarefas em "
                f"'{self._file_path}'."
            ) from error
            
#Função: Validação/Validate
    @staticmethod
    def _validate_unique_ids(tasks: list[Task]) -> None:
        """Verifica se existem IDs repetidos."""

        task_ids = [task.id for task in tasks]

        if len(task_ids) != len(set(task_ids)):
            raise TaskTrackerError(
                "O arquivo tasks.json contém IDs duplicados."
            )

#Classe: Versões do Serviço/Service Versions========================================================
class TaskService:
    """Contém as regras de negócio do Task Tracker."""
    #Função: Init
    def __init__(self, repository: JsonTaskRepository) -> None:
        self._repository = repository
#Função: Init storage
    def initialize_storage(self) -> list:
       """Inicializa o arquivo e devolve as tarefas existentes."""
       return self._repository.load()

#Função: Adiciona tarefas/Add tasks   
    def add_task(self, description: str) -> Task:
        """Cria, salva e devolve uma nova tarefa."""
        normalized_description = description.strip() 
        if not normalized_description:
            raise TaskTrackerError(
                "A descrição da tarefa não pode estar vazia."
            )
        tasks = self._repository.load()
        task_id = self._get_next_id(tasks)
        timestamp = current_timestamp()

        new_task = Task(
            id=task_id,
            description=normalized_description,
            status="todo",
            createdAt=timestamp,
            updatedAt=timestamp,
        )
        new_task.validate()
        tasks.append(new_task)
        self._repository.save(tasks)

        return new_task

#Função: Atualiza/Update task  
    def update_task(
        self,
        task_id: int,description: str,) -> Task:
        """Atualiza a descrição de uma tarefa."""
        self._validate_task_id(task_id)

        normalized_description = description.strip()

        if not normalized_description:
         raise TaskTrackerError(
            "A descrição da tarefa não pode estar vazia."
        )

        tasks = self._repository.load()
        task = self._find_task_by_id(tasks, task_id)

        if task.description == normalized_description:
         raise TaskTrackerError(
            f"A tarefa com ID {task_id} já possui "
            "essa descrição."
        )

        task.description = normalized_description
        task.updatedAt = current_timestamp()
        task.validate()

        self._repository.save(tasks)

        return task
    
#Função: Lista tarefas/List tasks
    def list_tasks(
        self,
        status: str | None = None,) -> list:
        """Lista todas as tarefas ou filtra pelo status."""
        tasks = self._repository.load()
        if status is None:
            return tasks

        if status not in VALID_STATUSES:
            allowed_statuses = ", ".join(VALID_STATUSES)
            raise TaskTrackerError(
                "Filtro de status inválido. "
                f"Valores permitidos: {allowed_statuses}."
            )
        return [
            task
            for task in tasks
            if task.status == status
        ]
#Função: Pega/Get ID
    @staticmethod
    def _get_next_id(tasks: list[Task]) -> int:
        """Calcula o próximo ID sem reutilizar IDs existentes."""

        if not tasks:
            return 1

        highest_id = max(task.id for task in tasks)

        return highest_id + 1
    
#Função: Encontra/Find ID  
    @staticmethod
    def _find_task_by_id(tasks: list[Task], task_id: int, ) -> Task:
      """Localiza uma tarefa pelo ID."""

      for task in tasks:
        if task.id == task_id:
           return task

        raise TaskTrackerError(
        f"Tarefa com ID {task_id} não encontrada."
    )

#Função: Valida/Validate ID
    @staticmethod
    def _validate_task_id(task_id: int) -> None:
       """Valida se o ID informado é um número inteiro positivo."""

       if isinstance(task_id, bool) or not isinstance(task_id, int):
        raise TaskTrackerError(
            "O ID da tarefa deve ser um número inteiro."
    )
       if task_id <= 0:
        raise TaskTrackerError(
            "O ID da tarefa deve ser maior que zero."
    )
        
#Função: Atualiza lista/Update the list
    def update_task_status(
     self,
     task_id: int, new_status: str,) -> Task:
     """Altera o status de uma tarefa e devolve a tarefa atualizada."""

     self._validate_task_id(task_id)

     if new_status not in VALID_STATUSES:
        allowed_statuses = ", ".join(VALID_STATUSES)

        raise TaskTrackerError(
            "Status inválido. "
            f"Valores permitidos: {allowed_statuses}."
    )

     tasks = self._repository.load()
     task = self._find_task_by_id(tasks, task_id)

     if task.status == new_status:
        raise TaskTrackerError(
            f"A tarefa com ID {task_id} já possui "
            f"o status '{new_status}'."
    )

     task.status = new_status
     task.updatedAt = current_timestamp()
     task.validate()

     self._repository.save(tasks)

     return task

#Função: Init repository
    def __init__(self, repository: JsonTaskRepository) -> None:
        self._repository = repository
#Função: Inicialização do arquivo e devolve a tarefa
    def initialize_storage(self) -> list:
        """Inicializa o arquivo e devolve as tarefas existentes."""

        return self._repository.load()
    
#Função: Lista tarefas
    def list_tasks(self, status: str | None = None) -> list:
        """Lista todas as tarefas ou filtra pelo status."""

        tasks = self._repository.load()

        if status is None:
            return tasks

        if status not in VALID_STATUSES:
            allowed_statuses = ", ".join(VALID_STATUSES)

            raise TaskTrackerError(
                "Filtro de status inválido. "
                f"Valores permitidos: {allowed_statuses}."
            )

        return [
            task
            for task in tasks
            if task.status == status
        ]
        
#Função: Parse CLI
def create_parser() -> argparse.ArgumentParser:
    """Cria e configura o interpretador de comandos da aplicação."""

    parser = argparse.ArgumentParser(
        prog="task-cli",
        description=(
            "Aplicação de linha de comando para gerenciamento de tarefas."
        ),
    )

    subparsers = parser.add_subparsers(
        dest="command",
        title="comandos",
    )

    add_parser = subparsers.add_parser(
        "add",
        help="Adiciona uma nova tarefa.",
    
    )

    add_parser.add_argument(
        "description",
        help="Descrição da nova tarefa.",
    
    )

    subparsers.add_parser(
        "delete",
        help="Exclui uma tarefa.",
    )
    
    update_parser = subparsers.add_parser(
    "update",
    help="Atualiza a descrição de uma tarefa.",
    )

    update_parser.add_argument(
    "task_id",
    type=int,
    help="ID da tarefa que será atualizada.",
    )

    update_parser.add_argument(
    "description",
    help="Nova descrição da tarefa.",
    )

    mark_in_progress_parser = subparsers.add_parser(
    "mark-in-progress",
    help="Marca uma tarefa como em andamento.",
    )

    mark_in_progress_parser.add_argument(
    "task_id",
    type=int,
    help="ID da tarefa que será marcada como em andamento.",
    )

    mark_done_parser = subparsers.add_parser(
    "mark-done",
    help="Marca uma tarefa como concluída.",
    )

    mark_done_parser.add_argument(
    "task_id",
    type=int,
    help="ID da tarefa que será marcada como concluída.",
    )

    list_parser = subparsers.add_parser(
        "list",
        help="Lista as tarefas.",
    )

    list_parser.add_argument(
        "status",
        nargs="?",
        choices=VALID_STATUSES,
        help="Filtra por todo, in-progress ou done.",
    )

    return parser

#Função: Exibir Tarefas
def print_tasks(tasks: list[Task]) -> None:
    """Exibe uma lista de tarefas no terminal."""

    if not tasks:
        print("Nenhuma tarefa encontrada.")
        return

    for task in tasks:
        print("-" * 50)
        print(f"ID: {task.id}")
        print(f"Descrição: {task.description}")
        print(f"Status: {task.status}")
        print(f"Criada em: {task.createdAt}")
        print(f"Atualizada em: {task.updatedAt}")

    print("-" * 50)

#Função: Controle de Comandos
def execute_command(
    args: argparse.Namespace,
    service: TaskService,
    parser: argparse.ArgumentParser,) -> None:
    """Direciona o comando recebido para a funcionalidade correta."""

    if args.command is None:
        parser.print_help()
        
        return

    if args.command == "add":
        task = service.add_task(args.description)

        print(f"Tarefa adicionada com sucesso (ID: {task.id})")
        
        return
    
    if args.command == "update":
       task = service.update_task(
        args.task_id,
        args.description,
    )

       print(f"Tarefa com ID {task.id} atualizada com sucesso.")
       
       return

    if args.command == "mark-in-progress":
       task = service.update_task_status(
       args.task_id,"in-progress",)

       print(f"Tarefa com ID {task.id} marcada como em andamento.")
    
       return

    if args.command == "mark-done":
        task = service.update_task_status(
        args.task_id,
        "done",
    )

        print(f"Tarefa com ID {task.id} marcada como concluída.")
    
        return

    if args.command == "list":
        tasks = service.list_tasks(args.status)
        print_tasks(tasks)
        
        return

    print(f"O comando '{args.command}' foi reconhecido, "
        "mas ainda não foi implementado.")

#Função Principal: Executa o programa(main)
def main() -> int:
    """Inicializa e executa a aplicação."""

    parser = create_parser()
    args = parser.parse_args()

    repository = JsonTaskRepository(
        get_data_file_path()
    )

    service = TaskService(repository)
    
    try:
        repository.ensure_file_exists()
        execute_command(args, service, parser)
        
        return 0

    except TaskTrackerError as error:
        print(
            f"Erro: {error}",
            file=sys.stderr,
        )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())