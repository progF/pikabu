# Shubarkol

**The purpose of the project is to give opportunity to  users to order coal to various places in Kazakhstan.**

## Apps and their functionality:
1. auth_
   - Main User models
   - Authentication
2. moderator
   - Regions, Cities, Zones, Tupics models
   - Uploading prices for coal and shipping for different cities.
   - Uploading prices for certain month
   - Calculating price of order
3. order
   - Creating order
   - Changing order status in admin panel
4. push
   - Making push notifications
   - History of notifications

# To use the project, do following steps:
1. Clone the repository
2. Create an environment
```
venv env
```
3. activate the environment and install all required libraries
On Windows
```
env/Scripts/activate
```
On Unix based system
```
source env/bin/activate
```
Then install requirements
```
pip install -r requirements.txt
```
4. create database "shubarkol" with login role "shubarkol" and password "shubarkol".
5. create all needed tables

```
python manage.py migrate
```

6. Run the project
```
python manage.py runserver
```
or 
```
./manage.py runserver
```

## Used technologies:
- PostgreSql 
- Django Python web framework
- Django Rest Framework
- OneSignal push technology
- smsc.kz
