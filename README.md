## Rates CRUD Task  [![Build Status](https://travis-ci.org/proserve/ratetask.svg?branch=master)](https://travis-ci.org/proserve/ratetask)

For The Get Requirements part I have implemented it with two different DB design:
- The first one is the same as the one you gave me  you find it under resources/rates.sql
- In the second one which is under resources/rates_new.sql I have merged regions and ports tables
to one table and I call it locations and I have added a type filed to specify if the location is 
a port or region or maybe something new in the future (let's say airport) here is the design of the new DB

I noticed also that new DB design perform much better in some type of query and the same in most queries
I setup for the that a profiling decorator ()
 
## API Documentation
Please export Doc/postman/ratetask.postman_collection.json file to your postman workspace to explore the api


## Setup 

if  you are using mac you need to install postgres in your machine to be able to install dependencies in requirements.txt
```shell
brew install postgresql
```  

#### Dependencies
Note: in some case I got compilation error while installing psycopg2 
```shell
sudo pip install -r requirements.txt
```

## Run app
#### Run the docker container
```shell 
docker build -t ratestask . # to be run only first time
docker run -p 0.0.0.0:5432:5432 --name ratestask ratestask
```
#### Rename the .env_copy to .env
```shell 
mv .env_copy .env
```
#### Run the app
```shell 
python app.py
```

## Test
```shell 
pytest test*
```
