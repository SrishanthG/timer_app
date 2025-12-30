import time
from datetime import timedelta


class _Timer:
    def __init__(self, hours, minutes, seconds):
        self.start_time = time.monotonic()
        self.target_elapsed_time = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        self.elapsed_time = timedelta(seconds=time.monotonic() - self.start_time)
        self.finished = False
        self.running = True

    def updated_elapsed_time(self):
        self.elapsed_time = timedelta(seconds=time.monotonic() - self.start_time)
        return self.elapsed_time

    def check_finished(self):
        if self.running:
            self.updated_elapsed_time()
            if self.elapsed_time >= self.target_elapsed_time:
                self.running = False
                self.finished = True
                return True
            
        return False


class TimerManager:
    def __init__(self):
        self.timers = []

    def new_timer(self, hours, minutes, seconds):
        self.timers.append(_Timer(hours, minutes, seconds))

    def next_wakeup(self):
        if not(self.timers):
            return None
        next_timer = min(self.timers, key=lambda t: t.target_elapsed_time - t.updated_elapsed_time())
        return next_timer.target_elapsed_time - next_timer.updated_elapsed_time()

    def check_all_timers(self):
        completed = []
        for timer in self.timers:
            if timer.check_finished():
                completed.append(timer)
                self.timers.remove(timer)
        return completed