import xlsxwriter


class Report:
    def __init__(self, model):
        self.workbook = xlsxwriter.Workbook(model + "_proc_timeline.xlsx")
        self.sheet = self.workbook.add_worksheet("Summary")

        self.scenario = []
        self.test_apps = []
        self.launch_time = []
        self.processes = {}

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
        self.sheet.write_string(y-1, x-1, string, form)

    def write_number(self, x, y, string, form):
        self.sheet.write_number(y-1, x-1, string, form)

    def write_scenario(self):
        for i in range(len(self.launch_time)):
            self.sheet.set_column(2+i, 1, 11)
            self.write_string(2+i, 1, self.launch_time[i], None)
        for i in range(len(self.scenario)):
            self.write_string(2+i, 2, self.scenario[i], None)

    def write_process(self):
        processes = self.processes.keys()
        
