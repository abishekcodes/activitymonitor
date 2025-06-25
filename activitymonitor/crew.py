from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from typing import List
from activitymonitor.tools import RunningProcess
from activitymonitor.tools import ActivityMonitorTools


@CrewBase
class ITOpsCrew():
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @task
    def cpu_monitor(self) -> Task:
        return Task(
            config=self.tasks_config['cpu_monitor']
        )
    
    @task
    def memory_monitor(self) -> Task:
        return Task(
            config=self.tasks_config['memory_monitor']
        )
    
    @task
    def battery_monitor(self) -> Task:
        return Task(
            config=self.tasks_config['battery_monitor']
        )
    
    @task
    def running_process(self) -> Task:
        return Task(
            config=self.tasks_config['running_process']
        )

    @agent
    def sysadmin_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['sysadmin_agent'], # type: ignore[index]
            verbose=True,
            tools=[
                ActivityMonitorTools.battery,
                ActivityMonitorTools.cpu,
                ActivityMonitorTools.memory,
                ActivityMonitorTools.running_process
            ],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )