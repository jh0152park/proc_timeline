import xlsxwriter


class Report:
    def __init__(self, model):
        self.workbook = xlsxwriter.Workbook(model + "_proc_timeline.xlsx")
        self.sheet = self.workbook.add_worksheet("Summary")

        self.scenario = []
        self.test_apps = []
        self.launch_time = []
        self.processes = {}
        self.process_sequence = []

    def close_sheet(self):
        self.workbook.close()

    def bring_scenario(self, scenario):
        self.scenario = scenario

    def bring_processes_info(self, processes):
        self.processes = processes

    def bring_launch_time(self, time):
        self.launch_time = time

    def bring_test_apps(self, apps):
        self.test_apps = apps

    def write_string(self, x, y, string, form):
        self.sheet.write_string(y - 1, x - 1, string, form)

    def write_number(self, x, y, number, form):
        self.sheet.write_number(y - 1, x - 1, number, form)

    def write_scenario(self):
        for i in range(len(self.launch_time)):
            self.sheet.set_column(2 + i, 1, 11)
            self.write_string(2 + i, 1, self.launch_time[i], None)
        for i in range(len(self.scenario)):
            self.write_string(2 + i, 2, self.scenario[i], None)

    def write_processes(self):
        processes = list(self.processes.keys())
        for app in self.test_apps:
            processes.remove(app)
        self.process_sequence = self.test_apps + processes

        self.sheet.set_column(0, 0, 40)
        for i in range(len(self.process_sequence)):
            self.sheet.set_row(2 + i, 60, None)
            self.write_string(1, 3 + i, self.process_sequence[i], None)

    def write_processes_detail(self):
        y = 0
        for proc in self.process_sequence:
            y += 1
            for info in self.processes[proc]:
                if info["pid"] == 0:
                    self.write_string(1 + info["launched"], 2 + y, "", None)
                else:
                    self.write_string(1 + info["launched"], 2 + y,
                                        info["adj"] + "\n" + info["pid"] + "\n" + info["pss"], None)
