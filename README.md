# Booking
- Youtube apresentation Link: [https://youtu.be/5hZNbNkdwkU](https://youtu.be/5hZNbNkdwkU)

## Distinctiveness and Complexity
- This project has the purpose of offering a way for restaurant owners and customers  to manage and booking tables, respectively, selecting the time and the desired table. Inside the system, users are separated into two types: Customers and Restaurant Owners. Customers can search restaurants, booking tables and cancel their own bookings. Restaurant Owners can manage their restaurants, adding and removing tables, change days of work and hours of work, manage bookings, confirm them when the client is inside the restaurant or cancel them, and they can even see the contact information of each user who has a booking. Instead of the other projects  did during the course, this is not an e-commerce, email, social media, search page or wiki website, this project is more similar to a library or like a hotel system, where the only purpose is to manage the time of the bookings, and allowing peoples to find new restaurants. The system doesn't deal with any value or stock information. Therefore, it's a logistic system for booking table in restaurants.


- The complexity of this project is to deal with images saved inside the system, deal with two types of users, where each of them can access different pages, and deal with the complex time system. Each restaurant inside the system has a booking time, this is the range of time that each table can be booked, so, for example, if a restaurant has a booking time of 1 hour and a table is booked at 07:00 PM, that means the system will not book that table until at 08:00 PM and can't let the table be booked after at 06:01 PM, because if a table is booked at 06:01 PM, the booking time will finish at 07:01 PM, conflicting with another booking. Another functionality inside the system  is manage the booking: a restaurant owner can confirm or cancel a booking, and beyond that, users can see user contact information. A customer can only cancel his booking, there being no option for confirmation. Each user can access different pages, but if a user tries to access a not allowed page, he will be redirected to his home page.

- The application is totally mobile-responsive. Developed with Django in back-end, has 6 models developed: User, DayOfWeek, Category, Restaurant, Table, Booking. The front-end was developed with Bootstrap 5.3 and uses JavaScript to load pages, form buttons, and also change content in a dynamic way without the need to reload the entire page. JavaScript is also used to set the preferred theme.

## Files Description
Bellow is the description of the content and purpose of each file present inside the project:
- `booking`: the main directory of application
    - [`settings.py`](booking\settings.py): this file contains all settings for the project, including changes in Media file, default user model and other.
    - [`urls.py`](booking\urls.py): this file contains the defaults route and including the url's from restaurant application.
- `media\images`: this directory is used for storage of all images upload inside the system, and it is divided in some directories
    - `backgroud`: this is the folder of all background images of all restaurants.
    - `logo`: this is the folder of all logo images from all restaurants
    - `menu`: this is the folder of the menu images from all restaurants.
- `restaurant`: this is the folder where the main application was developed, all files here represents the system by itself:
    - `static`: this folder contains the Javascript files and CSS file.
        - [`styles.css`](restaurant\static\restaurant\styles.css): this file contains the entire css used for the system, besides sytem uses Bootstrap, some changes was need for visual purposes, and to set a limit size for images and containers. Used inside the [layout.html](restaurant\templates\restaurant\layout.html) page.
        - [`booking.js`](restaurant\static\restaurant\booking.js): this file contains the functions to dynamic change the booking status without the need of reloading the page and communicating with python via an endpoint, its also enable the poppover functionality to see clients contact data. Used inside the [bookings.html](restaurant\templates\restaurant\bookings.html) page.
        - [`restaurant.js`](restaurant\static\restaurant\restaurant.js):this file constains the functions to dynamic search and change the bookings available, communicating with python via an endpoint, this JS file control the entire logic behing the booking system inside [`restaurant.html`](restaurant\templates\restaurant\restaurant.html).
        - [`tables.js`](restaurant\static\restaurant\tables.js): this file contains the logic behind the page of register tables, making two dynamic form, one for auto generated tables and other for custom tables, this JS also comunicate with python via an endpoint to save the tables. Used inside [`tables.html`](restaurant\templates\restaurant\tables.html)
        - [`update_tables.js`](restaurant\static\restaurant\update_tables.js): this file is very similar to [`tables.js`](restaurant\static\restaurant\tables.js) but has a lot of aditional logic functions to remove tables that is already register inside the system and to change some table information, this file also created dynamic fields if a new table is add. Used in [`update_table.html`](restaurant\templates\restaurant\update_table.html).
    - `template\restaurant`: this folder contains all HTML pages that are used in the system
        - [`layout.html`](restaurant\templates\restaurant\layout.html): this page contains the base HTML that every other file, inside this pages you can se the navbar and the theme selection content.
        - ['bookings.html'](restaurant\templates\restaurant\bookings.html) page that shows a list of all bookings based on a list provided by python.
        - ['login.html'](restaurant\templates\restaurant\login.html) page to login user, has two forms one for customers and other for Restaurant owners.
        - ['new_restaurant.html'](restaurant\templates\restaurant\new_restaurant.html) page to registar or update a restaurant.
        - ['register.html'](restaurant\templates\restaurant\register.html) page used to register or update an user.
        - ['restaurant_list.html'](restaurant\templates\restaurant\restaurant_list.html) page used everytime that is need to show a restaurant list.
        - ['restaurant.html'](restaurant\templates\restaurant\restaurant.html) page that shows restaurant info and if is accessed by a customer allows him to book a tablem, if is accessed by the restaurant owner, allows him to manage bookings, edit restaurant info and change tables info.
        - ['tables.html'](restaurant\templates\restaurant\tables.html) this page is used only to register tables.
        - ['update_table.html'](restaurant\templates\restaurant\update_table.html) this page is used only to update tables, it was developed separeted of tables because the dynamic field of each table conflict when create one.
    - [`admin.py`](restaurant\admin.py): this file contains the admin permissions to edit models inside the admin django page
    - [`forms.py`](restaurant\forms.py): this file contains the django forms used to register and update User and Restaurant models
    - [`models.py`](restaurant\models.py): this file contains the models structure, here you will find the 5 models used in this project:User,DayOfWeek,Category,Restaurant,Table,Booking
    - [`tests.py`](restaurant\tests.py) : this file contains some test cases for models and for select models queries, including searching for tables without bookings, testing saving images (for this test it will needed to change the value of IMAGE_PATH variable)
    - [`urls.py`](restaurant\urls.py): this file contains all URL's that can be acessed in the system, some URL's need login and can only be accessed base on your type user (Customer or Restaurant Owner)
    - [`views.py`](restaurant\views.py): this file contais all controllers of the system, here you gonna find the logic behind the login, register User, Restaurant and Tables and the time booking logic.Bellow is a explanation about each method:
        - ``index``: function responsible for render the index page. Login is required for access this view.
        - `login_view`: view responsible for render the login html page and for do the login when a POST request is made.
        - `logout_view`: view responsible for logout the user from the system. Login is required for access this view.
        - `restaurant` view responsible for search restaurants, save a new restaurant, get a restaurant based on id, list all restaurant from the user(only if user is a Restaurant Owner).Login is required for access this view.
        - ``save_days_of_work``: this functions is used to save the days of work for a restaurant, is used in ``restaurant`` and on `update_restaurant`.
        - `tables`: view responsible for get tables from an restaurant, update table info, delete table, render update table or register table page. Login is required for access this view.
        - `booking`: view responsible for get bookings, update bookings, get bookings hour, tables available for booking based in a date.Login is required for access this view.
        - `get_tables_without_booking`: this function returns the list of tables that can be booked for an restaurant. This function is used in `do_get_request_booking` function.
        - `set_timezone`: function that set a timezone for a date before save or search in django models. Used in `get_tables_without_booking` function,`booking` view, `get_bookings` function.
        - `get_bookings`: functions that returns all bookings based on date and status for a restaurant. Used in `do_get_request_booking` function.
        - `do_get_request_booking`: functions responsible for handle the GET request in `booking` view, this function returns a JSON with all tables available in a date and time, render the page of booking list for customer and for Restaurant Owner when a restaurant is choosen
        - `update_restaurant`: view responsible for load the page for update restaurant and for update restaurant inside the system. Login is required for access this view.
        - `user`: view responsible for render the update user.


- [`requirements.txt`](requirements.txt): this file contains the dependencies of the system please note that is only two dependencies: django and pillow, its recommended to use python 3.10 to run system

## How to run
- To run the project execute the steps bellow:
    - On your terminal inside the root of the project type the commands :
        - pip install -r requirements.txt
        - python manage.py makemigrations restaurant
        - python manage.py migrate
        - python manage.py runserver
    - Open your browser and type [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- If you download the code and the db.sqlite3 the following user are available. For tests purpose, all passwords are "1234":
    - test@example.com (Restaurant Owner and super user, you can access [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin))
    - dante@example.com (Customer user)
    - tommy@example.com (Customer user)
    - internationalfood@food.com (Restaurant owner with some restaurant's )
    - friends@food.com (Restaurant owner with some restaurant's )


## Certificate Link
- [https://cs50.harvard.edu/certificates/af2d9043-3cea-4402-98ab-c3610a6d7e3f.png?size=letter](https://cs50.harvard.edu/certificates/af2d9043-3cea-4402-98ab-c3610a6d7e3f.png?size=letter)