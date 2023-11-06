# Installation
### Clone or Download code from Github.
- You can clone the repository using this command
```
git clone https://github.com/tnnpp/Library-Management-System.git
```
- Or download the repository from my Github
### Create a virtual environment and install dependencies
1. change your directory to Library-Management-System and go to mysite folder
```
cd Library-Management-System
cd mysite
```
2. Installing the virtaualenv.
```
pip install virtualenv
```
3. Create virtual environment using this command.
```
virtualenv venv
```
4. Activate the virtual environment
```
# On Linux or MacOS
source venv/bin/activate
# On MS Windows
venv\Scripts\activate
```
5. Installing Dependencies
```
pip install -r requirement.txt
```
### Run migrations
setting up the database by migration as the code fellows.
```
python manage.py makemigrations
python manage.py migrate
```

### Install data from the data fixtures
loading the data 
```
python manage.py loaddata data/data_dump.json
```
### How to running the appliction
Using following code
```
python manage.py runserver
```
You should see this message printed in the terminal window:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
If you get a message that the port is unavailable, then run the server on a different port (1024 thru 65535) such as:
```
python3 manage.py runserver 12345
```
The website should work at
```
http://127.0.0.1:8000/
```

