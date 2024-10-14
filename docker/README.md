### Running
- Create the container
```
docker compose up
```
- To remove the container use
  - <b>THIS WILL DELETE ALL NON PERSISTENT DATA</b>
```
docker compose down
```

### Connecting
- Database connection can be achieved via
```
psql -U username -d database -h host -p port
```

### Environment Variables
Docker compose assumes `.env` file to be in root directory with the file. To specify an alternative, run with:
- `docker compose --env-file /path/to/.env up`


### Prerequisites
At least `Docker version 26.1.1`

To install docker please go to [this](https://docs.docker.com/engine/install/) website

