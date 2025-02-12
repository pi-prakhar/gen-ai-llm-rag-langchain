# Makefile Commands for Python Project with Virtual Environment

## How It Works:

### 1. Create Virtual Environment  
```sh
make venv
```
Creates the virtual environment if it doesn’t exist.

### 2. Enter Virtual Environment  
```sh
make enter
```
Displays the command to activate the virtual environment.

### 3. Exit Virtual Environment  
```sh
make exit
```
Displays the command to deactivate the virtual environment.

### 4. Check If Inside Virtual Environment  
```sh
make check
```
Checks if you are inside the virtual environment.

### 5. Run Setup Scripts  
```sh
make setup
```
Runs `create_db.py` and `rag_pipeline.py` inside the virtual environment.

### 6. Run the Main Script  
```sh
make run
```
Runs `main.py` inside the virtual environment.

### 7. Install Requirements  
```sh
make install
```
Installs dependencies from `requirements.txt` (only if inside the virtual environment).