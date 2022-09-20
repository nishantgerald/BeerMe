**Everything below must be run from the root folder:**

### Update brewery data
`source beerme/data/update_data.sh`

### Initialize SQLite3 Database
`flask --app beerme init-db`

### Deploy application in developer mode
`flask --app beerme --debug run -p <port>`

#### Once deployed you can head over to your browser at:
`http://127.0.0.1:<port>`