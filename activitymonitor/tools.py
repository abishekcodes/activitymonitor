from crewai.tools import tool
import psutil
from typing import TypedDict


class RunningProcess(TypedDict):
    name: str
    username: str
    pid: int
    cpu_percent: int


class ActivityMonitorTools:
    @tool("cpu_percentage")
    def cpu() -> str:
        """'Returns CPU Percentage'"""
        return f"The CPU is at {psutil.cpu_percent(interval=1)}% (all cores total)"


    @tool("memory_percentage")
    def memory() -> str:
        """Returns Memory Percentage"""
        return f"Memory is at {psutil.virtual_memory().percent}% (virtual memory)"


    @tool("battery_percentage")
    def battery() -> str:
        """Returns Battery Percentage"""
        battery_details = psutil.sensors_battery()
        if battery_details:
            return f"Battery is at {battery_details.percent}%"
        else:
            return "No Battery"


    @tool("running_process")
    def running_process(count: str = "10") -> str:
        """Returns Running Processes Sorted By CPU Usage in descending order"""

        processes = []
        for proc in psutil.process_iter(list(RunningProcess.__annotations__.keys())):
            processes.append(RunningProcess(**proc.info))

        processes.sort(key=lambda process: (process['cpu_percent'] is not None, process['cpu_percent']), reverse=True)

        processes_string = ""
        for process_index, process in enumerate(processes, start=1):
            if process_index > int(count):
                break
            processes_string += f"{process_index})\t{process['pid']}\t{process['name']}\t{process['cpu_percent']}\n"
        return processes_string