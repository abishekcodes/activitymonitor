from activitymonitor.crew import ITOpsCrew
from pathlib import Path

def run():

    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(env_path)

    inputs = {
        'user_query': input("\nHi I am your IT Ops Crew, I can provide with information about your system. What would you like to know? (e.g., CPU usage, memory usage, battery status, running processes): ").strip()
    }

    result = ITOpsCrew().crew().kickoff(inputs=inputs)
    print(result)

if __name__ == "__main__":
    run()