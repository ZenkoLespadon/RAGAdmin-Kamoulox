# Run the project

## The first time

### Create a Python virtual environment
python3 -m venv llm-env

### Install all dependencies
pip install -r requirement.txt

### Go into the virtual environment (to do at the root of the project)
source llm-env/bin/activate

### Start the project with uvicorn (to do at the root of the project)
uvicorn src.__main__:app --host SERVER_IP --port SERVICE_PORT


## The following times

### Go into the virtual environment (to do at the root of the project)
source llm-env/bin/activate

### Start the project with uvicorn (to do at the root of the project)
uvicorn src.__main__:app --host SERVER_IP --port SERVICE_PORT



# Add a document into ChromaDB 

### Put the document in src/service/chromadb (mandatory)

### Put the document name at the end of the AddPdfToChroma.py file

### Go into the virtual environment (to do in src/service/chromadb or change the path)
source ../../../llm-env/bin/activate

### Run the program
python3 AddPdfToChroma.py
