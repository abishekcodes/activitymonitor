from __future__ import annotations
from crewai.tools import tool
import psutil
from typing import List, Tuple, Sequence, Dict, Optional
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed


@dataclass
class RunningProcess:

    @dataclass
    class Child:
        pid_of_child: int
        cpu_percent_of_child: int
        process_user_of_child: str

    name: str
    cpu_percent_of_process: int
    children: List[RunningProcess.Child] = field(default_factory=list)

    @classmethod
    def prepare_from_process_info(cls, process_info: psutil.Process) -> RunningProcess:

        try:
            cpu_percent = process_info.cpu_percent(interval=1.0)
            return RunningProcess(
                name=process_info.name(),
                cpu_percent_of_process=cpu_percent,
                children=[
                    RunningProcess.Child(
                        pid_of_child=process_info.pid,
                        cpu_percent_of_child=cpu_percent,
                        process_user_of_child=process_info.username(),
                    )
                ]
            )

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return None
        
    def __add__(self, other: RunningProcess) -> RunningProcess:
        return RunningProcess(
            name=self.name,
            cpu_percent_of_process=self.cpu_percent_of_process+other.cpu_percent_of_process,
            children=sorted(self.children + other.children, reverse=True, key=lambda child: child.cpu_percent_of_child)
        )
    

    @classmethod
    def as_table(cls, processes: List[RunningProcess]) -> str:
        """Returns a string representation of the RunningProcess in a table format."""
        table_data = "\n\n"
        table_data += f"{'Name':<40} {'User':<20} {'CPU %':<10} {'PID':<10}"
        table_data += "\n" + "-" * 80 + "\n"
        for process in processes:
            short_name = process.name[:30] + "..." if len(process.name) > 30 else process.name
            table_data += f"\n{short_name:<40} {"-":<20} {process.cpu_percent_of_process:<10.2f} {'-':<10}"
            table_data += "\n" + "-" * 80 + "\n"
            table_data += "\n".join([
                f"{process.name:<40} {child.process_user_of_child:<20} {child.cpu_percent_of_child:<10.2f} {child.pid_of_child:<10}"
                for child in process.children
            ])
            table_data += "\n" + "-" * 80 + "\n"
        return table_data


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
                        processes[process_prepared.name] += process_prepared

        processes_list = list(processes.values())
        processes_list.sort(key=lambda process: process.cpu_percent_of_process, reverse=True)

        if count:
            return processes_list[:int(count)]
        else:
            return processes_list