## Install poetry
```bash
pip install poetry
```

## Install dependencies
```bash
poetry install
```

## Running the Tool
- Create a file called .env and paste your openai key there, Refer .env_example file for the variable name
- You can then use the following command to run the application
    ```bash
    python main.py
    ```

## Running Test Cases
```bash
pytest -v
```

## About this tool
- This is an LLM Agent who can answer any query regarding the following things
    1. CPU Percentage
    2. Memory Percentage
    3. Battery Percentage
    4. Running Process sorted based on cpu usage in descending order