import os
import tempfile
import unittest

from task_manager import (
    add_task,
    complete_task,
    delete_task,
    get_completed_tasks,
    get_pending_tasks,
    load_tasks,
)


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_tasks.json")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_and_pending_tasks(self):
        task = add_task("Complete math homework", self.db_path)
        self.assertIsNotNone(task)
        self.assertEqual(task["title"], "Complete math homework")
        self.assertFalse(task["completed"])

        pending = get_pending_tasks(self.db_path)
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0]["id"], task["id"])

    def test_ignore_empty_task(self):
        self.assertIsNone(add_task("   ", self.db_path))
        self.assertEqual(load_tasks(self.db_path), [])

    def test_complete_task(self):
        task = add_task("Read chapter 4", self.db_path)
        result = complete_task(task["id"], self.db_path)
        self.assertTrue(result)
        self.assertEqual(len(get_pending_tasks(self.db_path)), 0)
        self.assertEqual(len(get_completed_tasks(self.db_path)), 1)

    def test_delete_task(self):
        task = add_task("Submit lab report", self.db_path)
        self.assertTrue(delete_task(task["id"], self.db_path))
        self.assertEqual(load_tasks(self.db_path), [])
        self.assertFalse(delete_task(999, self.db_path))


if __name__ == "__main__":
    unittest.main()
