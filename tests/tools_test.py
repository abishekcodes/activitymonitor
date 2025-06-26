from activitymonitor.tools import ActivityMonitorTools, RunningProcess
from typing import List

def test_tool_running_process():
    processes: List[RunningProcess] = ActivityMonitorTools.running_process._run(count='100')
    assert processes[0].cpu_percent_of_process is not None
    assert len(processes) > 0

    prev_cpu = float('inf')
    for process in processes:
        assert prev_cpu >= process.cpu_percent_of_process
        prev_cpu = process.cpu_percent_of_process

def test_tool_cpu():
    cpu = ActivityMonitorTools.cpu._run()
    assert isinstance(cpu, float)
    
def test_tool_memory():
    memory = ActivityMonitorTools.memory._run()
    assert isinstance(memory, float)

def test_tool_battery():
    battery = ActivityMonitorTools.battery._run()
    assert isinstance(battery, int)