### Project Name: Online Examination System

##### Project developed using Django and Oracle SQL database  

##### This Project Contains Two Modules

- app_exam
- app_user

##### Project ERD File inside `erd-file` directory

##### Project Database File inside `database-file` directory

### Create Database

```sql
-- create a user 'dj' with password 'dj' and grant administrator privilege
create user dj identified BY dj;
grant dba to dj;
-- run the 'exam-ddl.sql' from the root directory in a new query to create the tables
```

###  Connecting to Database

```sql
sqlplus / as sysdba
show con_name; -- assuming it to be 'CDB$ROOT'
show pdbs; -- assuming it to be 'ORCLPDB'
alter session set container=ORCLPDB;
alter pluggable database open; -- opening the pluggable database
conn dj/dj@orclpdb -- assuming you want to connect user 'dj' with password 'dj'
show user; -- to show the currently connected user
-- if you want to change the password of the user
alter user dj identified by dj account unlock;
```

### Lister Service (If Required)

```bash
lsnrctl reload # to restart listener
lsnrctl stop # to stop listener
lsnrctl start # to start listener
```

### Cloning Project

```bash
git clone https://github.com/digital-animal/online-examination-system.git
```

### Installing Requirement 

```python
-- to install the requirements install the requirements
cd online-examination-system
pip install -r requirements.txt
```

### Running Project on Localhost

```python
python manage.py runserver
# then open in the link 127.0.0.1:8000 in browser
```

### Accessing Django Admin

```python
-- to access django admin, first you have to migrate the database
python manage.py migrate
python manage.py createsuperuser
$ Username: newuser
$ Email address: newuser@email.com
$ Password: newuser
$ Password (again): newuser
# then open in the link 127.0.0.1:8000/admin in browser and login
```

### Project Demonstration Link

```bash
https://drive.google.com/file/d/1rCMAefnw2K2wvnQwAr1rzJskvFPXiRgj/view?usp=sharing
```

