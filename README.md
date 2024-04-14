# jeeves
CLI for loading, analyzing, and visualizing data through simple text queries. Queries are processed using [CrewAI's](https://github.com/joaomdmoura/crewAI) agentic framework.

## Initialisation
Create a new virtual environment and install the required packages using the following commands:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Windows:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Usage
First, copy the .env.sample file to create a file named `.env`. Populate all variables in the .env file with the appropriate values.

Next, start up your postgres server and populate it with the data you want to analyze. Create a folder `documents` in the root directory and create a `schema.txt` file in the `documents` folder. The `schema.txt` file should contain the schema of the data you want to analyze, as well as any details about the data that you want to include in the analysis. You may also include any documents you would like the program to reference in the `documents` folder.

Run the following command to start the CLI:
```bash
python jeeves.py
```

There may be some initial loading required. After that, you can start querying your data!
