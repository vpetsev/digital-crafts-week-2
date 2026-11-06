import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).parent


class PoolRegressionTests(unittest.TestCase):
    def run_example(self, directory, code=None, answers=None):
        with tempfile.TemporaryDirectory() as tmp:
            shutil.copytree(ROOT / directory, tmp, dirs_exist_ok=True)
            command = [sys.executable, '-c', code] if code else [sys.executable, 'main.py']
            result = subprocess.run(command, cwd=tmp, input=answers,
                                    text=True, capture_output=True, timeout=5)
            self.assertEqual(result.returncode, 0, result.stderr)
            return result.stdout

    def test_legacy_table_menu_lists_all_tables(self):
        output = self.run_example('pool-table-management', answers='2\nq\n')
        self.assertEqual(output.count('Table number:'), 12)
        self.assertIn('Table number: 12', output)

    def test_procedural_close_selects_requested_table(self):
        self.run_example('pool-table-management2', code="""
import logic
logic.table_list[:] = [dict(table_number=n, occupied='Occupied', start_time='2024-01-01T23:30:00') for n in (1, 12)]
logic.time_adder = lambda: '2024-01-02T00:30:00'
assert logic.mark_as_unoccupied(1) is True
assert logic.table_list[0]['occupied'] == 'Not Occupied'
assert logic.table_list[0]['num_minutes_played'] == 60
assert logic.table_list[1]['occupied'] == 'Occupied'
assert logic.mark_as_unoccupied(1) is False
assert logic.mark_as_unoccupied(99) is False
assert logic.total_time_played == 60
""")

    def test_procedural_close_reads_legacy_clock_time(self):
        self.run_example('pool-table-management2', code="""
import logic
logic.table_list[:] = [dict(table_number=1, occupied='Occupied', start_time='23:30:00')]
logic.time_adder = lambda: '2024-01-02T00:30:00'
logic.mark_as_unoccupied(1)
assert logic.table_list[0]['num_minutes_played'] == 60
""")

    def test_class_table_cannot_be_reopened_while_occupied(self):
        self.run_example('pool-table-management-classes', code="""
import view, logic
view.pool_hall_tables[:] = [logic.Table(1).toDict()]
assert logic.Table(1).open_table() is True
original = view.pool_hall_tables[0]['start_time']
assert 'T' in original
assert logic.Table(1).open_table() is False
assert view.pool_hall_tables[0]['start_time'] == original
""")

    def test_class_elapsed_time_across_dates_and_legacy_midnight(self):
        self.run_example('pool-table-management-classes', code="""
import view, logic
for start, end, expected in [
    ('2024-01-01T23:30:00', '2024-01-02T00:30:00', 60),
    ('2024-01-01T23:30:00', '2024-01-03T00:30:00', 1500),
    ('23:30:00', '00:30:00', 60),
]:
    row = logic.Table(1).toDict()
    row.update(start_time=start, end_time=end, total_minutes_played_today=10)
    view.pool_hall_tables[:] = [row]
    logic.Table(1).min_played()
    assert row['total_minutes_played_today'] == expected + 10
    assert row['start_time'] is None
""")


if __name__ == '__main__':
    unittest.main()
