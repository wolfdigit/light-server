import time
from rndAge import RndAge

class Scheduler:
    def __init__(self, default=None):
        self.tasks = []
        self.timeout = []
        self.cronjobs = []
        if default is None:
            default = RndAge()
        self.default = default
        self.prepend_task(self.default)

    def append_task(self, obj):
        self.tasks.append(obj)

    def prepend_task(self, obj):
        self.tasks.insert(0, obj)
        self.runner = self.tasks[0]
        resume = getattr(self.runner, "resume", None)
        if callable(resume):
            resume()

    def next(self):
        if len(self.tasks)==1:
            self.append_task(self.default)
        self.tasks.pop(0)
        self.runner = self.tasks[0]
        resume = getattr(self.runner, "resume", None)
        if callable(resume):
            resume()

    def set_timeout(self, obj, ms):
        timeout = (time.time(), ms/1000.0, obj, False)
        self.timeout.append(timeout)
    def set_interval(self, obj, ms):
        timeout = (time.time(), ms/1000.0, obj, True)
        self.timeout.append(timeout)

    def check_timeout(self):
        now = time.time()
        for timeout in self.timeout:
            if now - timeout[0] > timeout[1]:
                self.prepend_task(timeout[2])
                self.timeout.remove(timeout)
                if timeout[3]:
                    self.timeout.append((now, timeout[1], timeout[2], True))

    def set_cronjob(self, obj, cron_str):
        """
        obj: object
        cron_str: sec, min, hr, dow, day
        """
        crons = tuple(cron_str.split(" "))  # sec, min, hr, dow, day
        self.cronjobs.append([crons, (0,0,0,0,0), obj])  # (crons, lastrun, obj)

    def check_cronjob(self):
        def in_cron(now, cron):
            # *  1,2  19-2,2  */2+1  21-0/2+1
            for s in cron.split(","):
                if s=="*":
                    return True
                if s.find("/")>=0:
                    remain = 0
                    numer, denom = s.split("/")
                    if denom.find("+")>=0:
                        denom, remain = denom.split("+")
                    if not in_cron(now, numer):
                        continue
                    if now%int(denom) != int(remain):
                        continue
                    return True
                if s.find("-")>=0:
                    lower, upper = s.split("-")
                    if lower<=upper:
                        if int(lower)<=now and now<=int(upper):
                            return True
                    else:
                        if int(lower)<=now or now<=int(upper):
                            return True
                if now==int(s):
                    return True
            return False
        now = time.localtime()
        now = (now.tm_sec, now.tm_min, now.tm_hour, now.tm_wday, now.tm_mday)
        for cronjob in self.cronjobs:
            lastrun = cronjob[1]
            if now == lastrun:
                continue
            cron = cronjob[0]
            if (
                in_cron(now[0], cron[0]) and
                in_cron(now[1], cron[1]) and
                in_cron(now[2], cron[2]) and
                in_cron(now[3], cron[3]) and
                in_cron(now[4], cron[4])
            ):
                self.prepend_task(cronjob[2])
                cronjob[1] = now

    def run(self):
        self.check_cronjob()
        self.check_timeout()
        cmds = self.runner.run()
        if isinstance(cmds, list):
            return cmds
        else:
            self.next()
            return self.run()