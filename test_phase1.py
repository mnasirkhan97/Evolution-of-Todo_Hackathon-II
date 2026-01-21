import unittest
from src.models import Task, TaskStatus
from src.storage import InMemoryStorage
from src.cli import TodoCLI
from unittest.mock import MagicMock 

class TestInMemoryStorage(unittest.TestCase):
    def setUp(self):
        self.storage = InMemoryStorage()

    def test_add_task(self):
        task = self.storage.add_task("Test Task", "Description")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Description")
        self.assertEqual(task.status, TaskStatus.PENDING)

    def test_get_all_tasks(self):
        self.storage.add_task("T1")
        self.storage.add_task("T2")
        tasks = self.storage.get_all_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].title, "T1")

    def test_update_task(self):
        task = self.storage.add_task("Old Title")
        self.storage.update_task(task.id, title="New Title")
        updated = self.storage.get_task(task.id)
        self.assertEqual(updated.title, "New Title")

    def test_mark_complete(self):
        task = self.storage.add_task("Task")
        self.storage.mark_complete(task.id)
        self.assertEqual(task.status, TaskStatus.COMPLETED)

    def test_delete_task(self):
        task = self.storage.add_task("Task")
        result = self.storage.delete_task(task.id)
        self.assertTrue(result)
        self.assertIsNone(self.storage.get_task(task.id))

class TestCLI(unittest.TestCase):
    def setUp(self):
        self.cli = TodoCLI()
        self.cli.console = MagicMock() # Mock console to avoid printing

    def test_handle_add(self):
        self.cli.handle_command("add 'Buy Milk' 'Dairy'")
        tasks = self.cli.storage.get_all_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Buy Milk")

    def test_handle_delete(self):
        task = self.cli.storage.add_task("To Delete")
        self.cli.handle_command(f"delete {task.id}")
        self.assertEqual(len(self.cli.storage.get_all_tasks()), 0)

if __name__ == "__main__":
    unittest.main()
