import unittest
from unittest.mock import patch
from io import StringIO
import curses
import psutil

# Import functions/classes from your ltop.py script
from ltop import get_system_info, get_top_processes_by_memory, draw_progress_bar, safe_addstr, display_system_info

class TestLtop(unittest.TestCase):

    def test_get_system_info(self):
        # Test get_system_info function
        mem, swap, cpu = get_system_info()
        self.assertIsNotNone(mem)
        self.assertIsNotNone(swap)
        self.assertIsNotNone(cpu)

    def test_get_top_processes_by_memory(self):
        # Test get_top_processes_by_memory function
        processes = get_top_processes_by_memory()
        self.assertGreaterEqual(len(processes), 0)

    def test_draw_progress_bar(self):
        # Test draw_progress_bar function
        screen = curses.initscr()
        try:
            draw_progress_bar(screen, 0, 0, 20, 50, curses.color_pair(1))
            screen.refresh()
        finally:
            curses.endwin()

    def test_safe_addstr(self):
        # Test safe_addstr function
        screen = curses.initscr()
        try:
            safe_addstr(screen, 0, 0, "Test String", curses.A_NORMAL)
            screen.refresh()
        finally:
            curses.endwin()

    def test_display_system_info(self):
        # Test display_system_info function
        screen = curses.initscr()
        try:
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            cpu = psutil.cpu_percent(interval=1, percpu=True)
            processes = get_top_processes_by_memory()
            display_system_info(screen, mem, swap, cpu, processes)
            screen.refresh()
            # You can add assertions here to verify if the system information is displayed correctly
        finally:
            curses.endwin()

if __name__ == '__main__':
    unittest.main()

