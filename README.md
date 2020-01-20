# Shubarkol

**The purpose of the project is to give opportunity to  users to order coal to various places in Kazakhstan.**

## Apps and their functionality:
1. ###### auth_
   - Main User models
   - Authentication
2. ###### moderator
   - Regions, Cities, Zones, Tupics models
   - Uploading prices for coal and shipping for different cities.
   - Uploading prices for certain month
   - Calculating price of order
3. ###### order
   - Creating order
   - Changing order status in admin panel
4. ###### push
   - Making push notifications
   - History of notifications

## Endpoints:
1. ###### auth_
   - /auth/send_sms/ - takes users phone and sends activation code
   - /auth/check_code/1/ - checks if activation code entered correctly
   - /auth/change_details/ - changes users full name field
2. ###### moderator
   - /moderator/regions/ - request to get all existing regions
   - /moderator/cities/?region_id=5 - request to get all existing cities in existing region
   - /moderator/cityzones/?city_id=2 - request to get all existing cityzones in city
   - /moderator/calculate_total_price/?city_id=1&weight=5 - request to get total price of tones and shipping
   - /moderator/address/add/ - request for adding new address to user
   - /moderator/address/update/ - query for updating existed address
   - /moderator/address/delete/ - request for deleting address
   - /moderator/get_busy_days/?city_id=2&zone_id=34 - request to return busy days which is filtered by limits of tupic

3. ###### order
   - /order/user_orders/ - users can get their own orders
   - /order/create_order/ - request to create new order
   - /order/get_status/1/ - request to check order status
   - /order/post_comment/ - request for posting comment for certain order
   - /order/get_status_by_order_number/458-9864-31/ - request to check order status by order number
4. ###### push
   - /push/user_notifications/ - request to get user's notifications history
   - /push/pushtokens/ - adding pushtoken and player_id for user



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
