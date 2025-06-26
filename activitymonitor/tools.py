from __future__ import annotations
from crewai.tools import tool
import psutil
from typing import List, Tuple, Sequence, Dict
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed


@dataclass
class RunningProcess:
    name: str
    process_user: str
    cpu_percent_of_process: int

    @classmethod
    def prepare_from_process_info(cls, process_info: psutil.Process) -> RunningProcess:
        try:
            return RunningProcess(
                name=process_info.name(),
                process_user=process_info.username(),
                cpu_percent_of_process=process_info.cpu_percent(interval=1.0),
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return None


class ActivityMonitorTools:
    @tool("cpu_percentage")
    def cpu() -> float:
        """Returns CPU Percentage considering all cores"""
        return psutil.cpu_percent(interval=1)


    @tool("memory_percentage")
    def memory() -> float:
        """Returns Memory Percentage considering virtual memory only"""
        return psutil.virtual_memory().percent


    @tool("battery_percentage")
    def battery() -> int:
        """Returns Battery Percentage if available, otherwise returns -1 indicating no battery information is available"""
        battery_details = psutil.sensors_battery()
        if battery_details:
            return battery_details.percent
        else:
            return -1


    @tool("running_process")
    def running_process(count: str = "5") -> List[RunningProcess]:
        """Returns Running Processes Sorted By CPU Usage in descending order"""

        processes: Dict[str, RunningProcess] = {}


        with ThreadPoolExecutor(max_workers=100) as executor:
            future_to_proc = {executor.submit(RunningProcess.prepare_from_process_info, proc): proc for proc in psutil.process_iter()}
            
            for future in as_completed(future_to_proc):
                result = future.result()
                if result is not None:
                    process_prepared = (result)
                    if process_prepared.name not in processes:
                        processes[process_prepared.name] = process_prepared
                    else:
                        processes[process_prepared.name].cpu_percent_of_process += process_prepared.cpu_percent_of_process

        processes_list = list(processes.values())
        processes_list.sort(key=lambda process: process.cpu_percent_of_process, reverse=True)

        if count:
            return processes_list[:int(count)]
        else:
            return processes_list