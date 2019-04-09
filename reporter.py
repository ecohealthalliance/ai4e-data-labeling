import time
from statistics import mean
from IPython.display import clear_output

class Reporter:
    def __init__(self, interval, total):
        self.start = time.time()
        self.this_time = self.start
        self.interval = interval
        self.total = total
        self.times_per_batch = []

    def report(self, idx):
        idx += 1
        if idx % self.interval is not 0:
            return
        self.last_time = self.this_time
        self.this_time = time.time()
        time_per = (self.this_time - self.last_time) / self.interval
        self.times_per_batch.append(time_per)
        est_time_left = (self.total - idx) * mean(self.times_per_batch[-10:])
        elapsed = time.time() - self.start

        output = "\033[F\033[K" + "Processed {0} articles ({1:.1f}%) in {2:.0f}m{3:.0f}s; about {4:.0f}m{5:.0f}s left.".format(
            idx,
            idx/self.total * 100,
            elapsed // 60,
            elapsed % 60,
            est_time_left // 60,
            est_time_left % 60)
        clear_output(wait=True)
        print(output)