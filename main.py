from backend.timer import TimerManager
import time
import threading
import queue
import winsound


manager = TimerManager()
condition = threading.Condition()
commands = queue.Queue()
quit_flag = False


def cli():
    global quit_flag

    cmds = []
    while True:
        user_input = input("\nEnter a command> ").strip()
        user_input = tuple(user_input.split())
        cmds.append(user_input)

        with condition:
            for _ in cmds:
                commands.put(cmds.pop())

            condition.notify()

        if user_input[0].lower() == "quit":
            quit_flag = True
            break
        

def scheduler():
    while True:
        if quit_flag:
            break

        with condition:
            if commands:
                while not commands.empty():
                    temp = commands.get_nowait()
                    if len(temp) == 2:
                        command, info = temp
                    else:
                        command = temp[0]

                    if command.lower() == "add":
                        duration = list(map(int, info.split(":")))
                        manager.new_timer(duration[0], duration[1], duration[2])

            delay = manager.next_wakeup()

            if delay is None:
                condition.wait(0.1)
                continue
            
            condition.wait(timeout=delay.total_seconds())

        finished = manager.check_all_timers()

        for timer in finished:
            winsound.PlaySound("Video Project.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

        if not manager.timers:
            pass


if __name__ == "__main__":
    print("Please enter a command. The available commands are add <HH:MM:SS> and quit. More commands will be available in the future.")

    cli_thread = threading.Thread(target=cli)
    scheduler_thread = threading.Thread(target=scheduler)

    cli_thread.start()
    scheduler_thread.start()

    cli_thread.join()
    scheduler_thread.join()