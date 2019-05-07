# Project: Item Catalog

What is this project?

We have several categories of sports and inside every sport, there are many items along with their description.
There are two cases here:
1. User not logged in: He can only view categories, items under each category and description of items. He will not be able to add, edit or delete things.
2. User is logged in: In this case, he can add a new item where item name, description and category it belongs to are needed. Then he can edit this item and he can even delete it.

Set up system environment
Use virtual box (https://github.com/udacity/fullstack-nanodegree-vm) to run this project. Follow below steps to do this:
1. Clone above repo to local machine: git clone https://github.com/udacity/fullstack-nanodegree-vm
2. Go inside vagrant folder
3. Run command: $vagrant up
4. Run command: $vagrant ssh
you are inside vm now!

Now, clone this (item-catalog) project inside fullstack-nanodegree-vm/vagrant because this is shared folder with vm /vagrant, we are doing this beacause we will be running in vm as everything will be already setup there.
We need to set up few more things here in order to run final project:
1. Database: run database_setup.py file to setup sqlalchemy db : $python database_setup.py
2. Populate this db with some initial data: $python populate_db.py

Now the final command that will bring our api application up and running:
$python views.py  

Application will run at localhost:5000
Api endpoints:

1. List all categories: http://localhost:5000/catalogs
2. List items within a category: http://localhost:5000/catalog/<string:sport_name>/items
3. Show item description: http://localhost:5000/catalogs/<string:sport_name>/<string:item_name>
4. Create new item: http://localhost:5000/catalog/new
5. Edit an item: http://localhost:5000/catalogs/<string:sport_name>/<string:item_name>/edit
5. Delete an item: http://localhost:5000/catalogs/<string:sport_name>/<string:item_name>/delete
6. Json repsonse of all catagories along with its items: http://localhost:5000/catalogs/JSON


