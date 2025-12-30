from backend.timer import TimerManager

import time


if __name__ == "__main__":
    manager = TimerManager()
    manager.new_timer(int(input('Number of hours: ')), int(input('Number of minutes: ')), int(input('Number of seconds: ')))

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