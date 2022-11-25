class Miner:
    def __init__(self, log):
        self.log = log
        self.time = []
        self.scenario = []
        self.processes = {}
        self.process_count = {}

        self.launched = 100

    def compute_scenario(self):
        for i in range(len(self.log)):
            line = self.log[i][:-1]
            if "run this app" in line:
                app = line.split(":")[-1].strip()
                self.time.append(self.log[i-1][:-1])
                if len(self.scenario) > 1 and self.scenario[-1] == "Fit The Fat 3":
                    self.scenario.append("Call of Duty")
                elif len(self.scenario) > 1 and self.scenario[-1] == "ESPN":
                    self.scenario.append("Coupang")
                else:
                    self.scenario.append(app)

    def read_all_process(self):
        read = False
        for line in self.log:
            line = line[:-1]
            if "Total PSS by process:" in line:
                read = True
            if "Total PSS by OOM adjustment:" in line:
                read = False

            if read is True:
                if "(pid" in line:
                    process = line.split()[1]
                    if process not in self.process_count.keys():
                        self.process_count[process] = 0
                    self.process_count[process] += 1

        # for proc in self.overlap_process.keys():
        #     print(f"{proc} / {self.overlap_process[proc]}")

    def select_process(self):
        for proc in self.process_count.keys():
            if self.process_count[proc] > self.launched:
                pass
                """
                 * skip this case
                 * because, we can not detect which process is same or different
                 * when some process was overlap, its can divide with only pid
                 * but processes were could be dead every time while test
                 * so, this case we can not divide which process is correct with past
                """
            else:
                if proc not in self.processes.keys():
                    self.processes[proc] = []

    @staticmethod
    def compute_adj(log):
        adj = log.split(":")[1].split("(")[0].strip()
        return adj

    @staticmethod
    def compute_pss(log) -> int:
        return int(log.split()[0][:-2].replace(",", ""))

    @staticmethod
    def compute_swap(log) -> int:
        return 0 if "swap)" not in log else int(log.split()[-3][:-1].replace(",", ""))

    @staticmethod
    def compute_pid(log) -> str:
        return log.split()[3].replace(")", "")

    @staticmethod
    def compute_process(log) -> str:
        return log.split()[1]

    @staticmethod
    def compute_activity(log) -> bool:
        return True if "activities)" in log else False

    def fill_up_process_info(self):
        for proc in self.processes.keys():
            self.processes[proc].append({
                "launched": 0,
                "activity": False,
                "adj": 0,
                "pss": 0,
                "pid": 0
            })
            self.processes[proc][-1]["launched"] = len(self.processes[proc])

    def compute_processes(self):
        adj = ""
        read = False

        for line in self.log:
            line = line[:-1]

            if "run this app" in line:
                self.fill_up_process_info()
            if "Total PSS by OOM adjustment:" in line:
                read = True
            if "Total PSS by category:" in line:
                read = False

            if read is True:
                if "K: " in line:
                    if "pid" not in line:
                        adj = self.compute_adj(line)
                    else:
                        proc = self.compute_process(line)
                        print(f"{proc} / {adj}")
                        if self.process_count[proc] <= self.launched:
                            self.processes[proc][-1]["adj"] = adj
                            self.processes[proc][-1]["pss"] = self.compute_pss(line)
                            self.processes[proc][-1]["pid"] = self.compute_pid(line)
                            self.processes[proc][-1]["activity"] = self.compute_activity(line)

    def start_parsing(self):
        self.compute_scenario()
        self.read_all_process()
        self.select_process()
        self.compute_processes()
