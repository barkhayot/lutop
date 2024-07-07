import psutil
import curses

def get_system_info():
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    cpu = psutil.cpu_percent(interval=1, percpu=True)
    return mem, swap, cpu

def get_top_processes_by_memory(num_processes=10):
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent', 'cmdline']):
        try:
            proc_info = proc.info
            if proc_info['memory_percent'] is not None:  # Ensure memory_percent is not None
                proc_info['cmdline'] = ' '.join(proc_info['cmdline']) if proc_info['cmdline'] else '[No Command Line]'
                processes.append(proc_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    processes = sorted(processes, key=lambda p: p['memory_percent'], reverse=True)
    return processes[:num_processes]

def draw_progress_bar(screen, y, x, width, percent, color_pair):
    filled_width = int(width * percent // 100)
    bar = '█' * filled_width + ' ' * (width - filled_width)
    try:
        screen.addstr(y, x, f"[{bar}] {percent:.2f}%", color_pair)
    except curses.error:
        pass

def safe_addstr(screen, y, x, text, attr):
    height, width = screen.getmaxyx()
    if y < height:
        screen.addstr(y, x, text[:width - x], attr)

def display_system_info(screen, mem, swap, cpu, processes):
    screen.clear()
    height, width = screen.getmaxyx()

    pid_width = 5
    name_width = max(20, (width - 80) // 2)  # Minimum 20 characters, or half the available space
    cpu_width = 6
    mem_width = 6
    cmdline_width = max(60, width - pid_width - name_width - cpu_width - mem_width - 4)  # Minimum 60 characters or remainder space

    # CPU Usage
    cpu_info_start_y = 0
    screen.addstr(cpu_info_start_y, 0, "CPU Usage".center(width), curses.A_BOLD)
    col_width = (width - 2) // 2  # Width for each column
    for i, cpu_percent in enumerate(cpu):
        col = i % 2  # Determine the column (0 or 1)
        row = i // 2  # Determine the row
        color_pair = curses.color_pair(1 if cpu_percent < 50 else 2 if cpu_percent < 75 else 3)
        core_label = f" Core {i}:".ljust(8)
        core_x = col * col_width
        draw_progress_bar(screen, cpu_info_start_y + 1 + row, core_x + len(core_label), col_width - len(core_label) - 1 - 8, cpu_percent, color_pair)
        safe_addstr(screen, cpu_info_start_y + 1 + row, core_x, core_label, curses.A_BOLD)

    # Memory Information
    mem_info_start_y = cpu_info_start_y + (len(cpu) // 2) + 2
    screen.addstr(mem_info_start_y, 0, "Memory Usage".center(width), curses.A_BOLD)
    color_pair = curses.color_pair(1 if mem.percent < 50 else 2 if mem.percent < 75 else 3)
    draw_progress_bar(screen, mem_info_start_y + 1, 0, width - 2, mem.percent, color_pair)
    safe_addstr(screen, mem_info_start_y + 1, width - 8, f"{mem.percent:.2f}%", curses.A_BOLD)

    screen.addstr(mem_info_start_y + 2, 0, f"Total Memory: {mem.total / (1024 ** 3):.2f} GB")
    screen.addstr(mem_info_start_y + 3, 0, f"Used Memory: {mem.used / (1024 ** 3):.2f} GB")
    screen.addstr(mem_info_start_y + 4, 0, f"Free Memory: {mem.free / (1024 ** 3):.2f} GB")

    # Swap Information
    swap_info_start_y = mem_info_start_y + 5
    screen.addstr(swap_info_start_y, 0, "Swap Usage".center(width), curses.A_BOLD)
    color_pair = curses.color_pair(1 if swap.percent < 50 else 2 if swap.percent < 75 else 3)
    draw_progress_bar(screen, swap_info_start_y + 1, 0, width - 2, swap.percent, color_pair)
    safe_addstr(screen, swap_info_start_y + 1, width - 8, f"{swap.percent:.2f}%", curses.A_BOLD)

    screen.addstr(swap_info_start_y + 2, 0, f"Total Swap: {swap.total / (1024 ** 3):.2f} GB")
    screen.addstr(swap_info_start_y + 3, 0, f"Used Swap: {swap.used / (1024 ** 3):.2f} GB")
    screen.addstr(swap_info_start_y + 4, 0, f"Free Swap: {swap.free / (1024 ** 3):.2f} GB")

    # Top Processes by Memory Usage
    top_procs_start_y = swap_info_start_y + 5
    if top_procs_start_y >= height:
        screen.addstr(top_procs_start_y, 0, "Terminal too small to display processes".center(width), curses.A_BOLD)
    else:
        screen.addstr(top_procs_start_y, 0, "Top Processes by Memory Usage".center(width), curses.A_BOLD)
        max_procs = min(height - top_procs_start_y - 2, len(processes))  # Maximum processes to display
        for i, proc in enumerate(processes[:max_procs]):
            cmdline = proc['cmdline'].replace('\n', ' ').replace('\r', ' ')  # Replace newlines and carriage returns
            safe_addstr(screen, top_procs_start_y + 1 + i, 0, f"{proc['pid']:>{pid_width}} {proc['name'][:name_width]:<{name_width}} {proc['cpu_percent']:>{cpu_width}.2f} {proc['memory_percent']:>{mem_width}.2f} {cmdline[:cmdline_width]:<{cmdline_width}}", curses.A_NORMAL)

    screen.refresh()

def main(screen):
    curses.curs_set(0)  # Hide the cursor
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    # Initial screen setup
    mem, swap, cpu = get_system_info()
    top_processes = get_top_processes_by_memory()
    display_system_info(screen, mem, swap, cpu, top_processes)

    while True:
        try:
            # Check for terminal resize
            new_height, new_width = screen.getmaxyx()
            if new_height != curses.LINES or new_width != curses.COLS:
                curses.resizeterm(new_height, new_width)
                screen.clear()
                mem, swap, cpu = get_system_info()
                top_processes = get_top_processes_by_memory()
                display_system_info(screen, mem, swap, cpu, top_processes)
            else:
                # Refresh data every second
                mem, swap, cpu = get_system_info()
                top_processes = get_top_processes_by_memory()
                display_system_info(screen, mem, swap, cpu, top_processes)

                # Check for Ctrl + D (EOFError) to quit the application
                ch = screen.getch()
                if ch == 4:  # Ctrl + D (EOFError)
                    break  # Exit the loop and terminate the application

        except curses.error:
            pass

curses.wrapper(main)


