import sys
import shlex
from rich.console import Console
from rich.table import Table
from src.storage import InMemoryStorage
from src.models import TaskStatus

class TodoCLI:
    def __init__(self):
        self.storage = InMemoryStorage()
        self.console = Console()

    def start(self):
        """Starts the interactive CLI loop."""
        self.console.print("[bold green]Welcome to The Evolution of Todo (Phase I)[/bold green]")
        self.console.print("Type 'help' for commands or 'exit' to quit.")

        while True:
            try:
                user_input = self.console.input("[bold blue]todo>[/bold blue] ")
                if not user_input.strip():
                    continue
                
                self.handle_command(user_input)
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Exiting...[/yellow]")
                break
            except Exception as e:
                self.console.print(f"[bold red]Error:[/bold red] {e}")

    def handle_command(self, user_input: str):
        parts = shlex.split(user_input)
        command = parts[0].lower()
        args = parts[1:]

        if command in ("exit", "quit"):
            self.console.print("[yellow]Goodbye![/yellow]")
            sys.exit(0)
        
        elif command == "add":
            if not args:
                self.console.print("[red]Usage: add <title> [description][/red]")
                return
            title = args[0]
            description = args[1] if len(args) > 1 else None
            task = self.storage.add_task(title, description)
            self.console.print(f"[green]Added task #{task.id}: {task.title}[/green]")

        elif command == "list":
            tasks = self.storage.get_all_tasks()
            if not tasks:
                self.console.print("[italic]No tasks found.[/italic]")
                return
            
            table = Table(title="Todo List")
            table.add_column("ID", style="cyan", no_wrap=True)
            table.add_column("Title", style="magenta")
            table.add_column("Status", style="green")
            table.add_column("Description")

            for task in tasks:
                status_color = "green" if task.status == TaskStatus.COMPLETED else "yellow"
                table.add_row(
                    str(task.id), 
                    task.title, 
                    f"[{status_color}]{task.status.value}[/{status_color}]", 
                    task.description or ""
                )
            self.console.print(table)

        elif command == "update":
            if len(args) < 1:
                self.console.print("[red]Usage: update <id> [title] [description][/red]")
                return
            try:
                task_id = int(args[0])
                # Interactive update or args? Spec says "Input: New Title, New Description". 
                # Let's support both but prioritize interactive if args missing? 
                # To keep it simple and consistent with shlex parsing: expects arguments.
                
                # However, providing optional args in a single line can be tricky (which one is title?).
                # Let's follow a simpler approach: prompt if not provided, or strict args.
                # Spec: "Input: New Title, New Description. (Blank to keep existing)."
                
                new_title = None
                new_desc = None
                
                # Check for additional args or prompt
                if len(args) > 1:
                    new_title = args[1]
                else:
                    new_title = self.console.input("New Title (leave blank to keep): ").strip() or None
                
                if len(args) > 2:
                    new_desc = args[2]
                else:
                    new_desc = self.console.input("New Description (leave blank to keep): ").strip() or None

                updated_task = self.storage.update_task(task_id, new_title, new_desc)
                if updated_task:
                    self.console.print(f"[green]Updated task #{task_id}[/green]")
                else:
                    self.console.print(f"[red]Task #{task_id} not found.[/red]")
            except ValueError:
                self.console.print("[red]Invalid ID format.[/red]")

        elif command == "complete":
            if not args:
                self.console.print("[red]Usage: complete <id>[/red]")
                return
            try:
                task_id = int(args[0])
                task = self.storage.mark_complete(task_id)
                if task:
                    self.console.print(f"[green]Task #{task_id} marked as completed![/green]")
                else:
                    self.console.print(f"[red]Task #{task_id} not found.[/red]")
            except ValueError:
                self.console.print("[red]Invalid ID format.[/red]")

        elif command == "delete":
            if not args:
                self.console.print("[red]Usage: delete <id>[/red]")
                return
            try:
                task_id = int(args[0])
                if self.storage.delete_task(task_id):
                    self.console.print(f"[green]Task #{task_id} deleted.[/green]")
                else:
                    self.console.print(f"[red]Task #{task_id} not found.[/red]")
            except ValueError:
                self.console.print("[red]Invalid ID format.[/red]")
        
        elif command == "help":
            self.console.print("Commands: add, list, update, complete, delete, exit")
        
        else:
            self.console.print(f"[red]Unknown command: {command}[/red]")
