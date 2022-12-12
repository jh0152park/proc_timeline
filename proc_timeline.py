import os
import miner
import report_generator

log = ""
model = ""
for file in os.listdir(os.getcwd()):
    if "dumpsys_meminfo" in file:
        model = file.split("_")[1]
        log = open(file, "r", errors="ignore").readlines()
        break

meminfo = miner.Miner(log)
meminfo.start_parsing()

report = report_generator.Report(model)

report.bring_processes_info(meminfo.get_processes_info())
report.bring_scenario(meminfo.get_scenario())
report.bring_launch_time(meminfo.get_launch_time())
report.bring_test_apps(meminfo.get_test_apps())

report.write_scenario()
report.write_processes()
report.write_processes_detail()

report.close_sheet()
