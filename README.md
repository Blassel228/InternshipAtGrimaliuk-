In order to install all needed packages execute "pip install -r requirements.txt" in your terminal.
You can run the application in Docker using the next command "docker build -t app".
Launching a server is performed by "uvicorn app.main:app --reload --port any_port_you_want".
In order to generate a revision file use command "alembic revision --autogenerate".
In order to make a migration, use command "alembic upgrade revision_name".
