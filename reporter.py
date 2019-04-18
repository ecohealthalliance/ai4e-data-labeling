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

        output = "\033[F\033[K" + "Processed {0} articles ({1:.1f}%) in "\
            "{2:.0f}m{3:.0f}s; about {4:.0f}m{5:.0f}s left."\
            .format(
                idx,
                idx/self.total * 100,
                elapsed // 60,
                elapsed % 60,
                est_time_left // 60,
                est_time_left % 60)
        clear_output(wait=True)
        print(output)


class MongoQueryReporter:
    def __init__(self, interval, collection, query):
        self.interval = interval
        self.collection = collection
        self.query = query
        self.times = []
        self.times.append({
            "time": time.time(),
            "remaining": self.collection.count_documents(self.query),
            "completed": 0
        })

    def update(self, idx=None):
        t1 = time.time()
        if idx is not None:
            completed = idx + 1
            self.times.append({
                "time": time.time(),
                "remaining": self.times[0]["remaining"] - completed,
                "completed": completed
            })
        else:
            remaining = self.collection.count_documents(self.query)
            self.times.append({
                "time": time.time(),
                "remaining": remaining,
                "completed": self.times[0]["remaining"] - remaining
            })

    def report(self, idx=None):
        if time.time() - self.times[-1]["time"] < self.interval:
            return self.times[-1]["remaining"]
        self.update(idx)
        first = self.times[0]
        comparison = self.times[-5:][1]
        latest = self.times[-1]
        if latest["remaining"] == 0:
            return latest["remaining"]
        time_delta = latest["time"] - comparison["time"]
        task_delta = comparison["remaining"] - latest["remaining"]
        if task_delta > 0:
            time_per_task = time_delta / task_delta
        else:
            return latest["remaining"]
        total_time_delta = latest["time"] - first["time"]
        total_task_delta = first["remaining"] - latest["remaining"]
        tasks_left = latest["remaining"]
        est_time_left = tasks_left * time_per_task

        output = "\033[F\033[K" + "Processed {0} articles ({1:.1f}%) in "\
            "{2:.0f}m{3:.0f}s; about {4:.0f}m{5:.0f}s left."\
            .format(
                total_task_delta,
                total_task_delta / first["remaining"] * 100,
                total_time_delta // 60,
                total_time_delta % 60,
                est_time_left // 60,
                est_time_left % 60)
        clear_output(wait=True)
        print(output)
        return latest["remaining"]
