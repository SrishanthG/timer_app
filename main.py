from backend.timer import TimerManager

import time


if __name__ == "__main__":
    manager = TimerManager()

    user_input = input("Enter amount of time for timer (HH:MM:SS): ")
    user_input = list(map(int, user_input.split(":")))

    manager.new_timer(user_input[0], user_input[1], user_input[2])

    while True:
        delay = manager.next_wakeup()

        if delay is None:
            time.sleep(0.1)
            continue
        
        time.sleep(delay.total_seconds())

        finished = manager.check_all_timers()

        for timer in finished:
            print('\nTimer finished\n')

        if not manager.timers:
            break