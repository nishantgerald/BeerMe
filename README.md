
---
## Set-up Notes
---
### Update brewery data from root folder
`source beerme/data/update_data.sh`

### Initialize SQLite3 Database
`flask --app beerme init-db`

### Deploy application in debug mode
`flask --app beerme --debug run -p <port>`

### Set-up environment
`pip3 install -r <path to requirements.txt>`

### Once deployed you can head over to your browser at:
`http://127.0.0.1:<port>`

### In order to reset the entire database:
First delete database:
`rm instance/beerme.sqlite`

And then rerun the database initialization function:
`flask --app beerme init-db`

---
## Application Notes
---
* If it's your first time on the page, you will be asked to register.
* If you are registered, go to the login page and enter your credentials.
* Once logged in, you can check in your beers.
* You can search previously logged beers on the `Search` page
* To view stats on your logged beers, check our the `Stats` page
* Once you are done, feel free to hit `Logout` to clear the session.
* All user registations and logged beers will remain stored in the sqlite database as long as the database is untouched. However, ru-running the `init-db` function will reset everything.