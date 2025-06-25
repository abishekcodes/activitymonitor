#!/usr/bin/env python
import os
from activitymonitor.crew import ITOpsCrew

def run():

    from dotenv import load_dotenv
    load_dotenv()

    inputs = {
        'user_query': input("\nWhat would you like to monitor?")
    }

    result = ITOpsCrew().crew().kickoff(inputs=inputs)
    print(result)

if __name__ == "__main__":
    run()