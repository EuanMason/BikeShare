# ProgSD - Bike Share 

Programming and System Development Team Project.
The main objective is to create a bike share program based on three roles (Customer, Operator, Manager). 

# Basic Git Commands
To keep the track of your local work please always remember to check your repository and pull changes before starting to work.
```
git status                  # to check is your local copy is up to date
git pull                    # to downlaod the changes if any
git add <file>              # to add a file on tracking. It means, if you want to upload first need to add it
git commit -m "<message>"   # to commit all the changes that you added before
git push                    # to upload the changes to the repository
```

# Basic Django
Django is the framework we are using to develop as a local server for both frontend and backend.
**Both groups** need to keep the correct track of the server and the data (the sql file)

## Frontend
Before starting to use the webserver, you need to run the following commands in order. Remember your cmd must be at ***bakeshare*** folder
```
python manage.py migrate
python manage.py runserver
```

The first command, allows you to get all changes that may occur for various reasons in the database.
The second command allows you to run the server and can see it works in your localhost.

## Backend
Before starting to use the webserver, you need to run the following commands in order. Remember your cmd must be at ***bakeshare*** folder
```
python manage.py migrate
python manage.py runserver
```

The first command, allows you to get all changes that may occur for various reasons in the database.
The second command allows you to run the server and can see it works in your localhost, which will be used for the REST and the frontend.

### Need to change a Model
When changing a Model you need to create the migration
```
python manage.py makemigrations bikeshareapp
python manage.py migrate
```
Please be extremely  careful about this, because it could affect enormously when applying changes. 

# Making changes

## Frontend
Please place all the templates at * *bikeshare\templates\bikeshareapp* *.
All the extra framworks should be at * *bikeshare\templates\js* * (for js files) or  *bikeshare\templates\css* * (for css files)

## Backend
To add functionalities please use the file **custom_actions_rest_view.py**, this is at * *bikeshare\bikeshareapp* *.
There you will find four sections separated by a comment. Add your method where appropriate.
Keep in mind the following:
- Always add the decorator ```@api_view``` to the method and specify the methods allowed. 
- If you add a method, you will need to add the url in urls.py at * * bikeshare\bikeshare * *.
- When adding the method to the url.py file, make sure to specify correctly the url format and the method like ```path('add-money-to-wallet/', addMoney)```


# If question
Please ask in the Teams Group Chat :) 