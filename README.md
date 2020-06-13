# Table of Contents
1. Create Container
2. Run Migration
3. Testing using Insomnia

## Create Container
1. Copy `.env.docker.example` to `.env` then edit the content based on your preferred configuration
2. Run `docker-compose.yaml`
3. Open `http://localhost`
```
docker-compose up --build -d
```
3. Run migration

## Run Migration
1. Create migration repository

You can create a migration repository with the following command:
```
flask db init
```
This will add a migrations folder to your application. You can create a migration repository inside docker container with the following command:
```
docker-compose exec api flask db init
```

2. Generate initial migration

This will add a migration version each time you update your model.
```
flask db migrate -m "Initial migration."
```
then inside docker container
```
docker-compose exec api flask db migrate -m "Initial migration."
```

3. Apply the migration to the database

Then you can apply the migration to the database with the following command:
```
flask db upgrade
```
then inside docker container
```
docker-compose exec api flask db upgrade
```

### Testing using Insomnia
1. Import `Insomnia.json` to your Insomnia app
2. Change Environment based on your preference