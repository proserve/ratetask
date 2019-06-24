## Rates CRUD Task  [![Build Status](https://travis-ci.org/proserve/ratetask.svg?branch=master)](https://travis-ci.org/proserve/ratetask)

For The Get Requirements part I have implemented it with two different DB design:
- The first one is the same as the one you gave me  you find it under resources/rates.sql
- In the second one which is under resources/rates_new.sql I have merged regions and ports tables
to one table and I call it locations and I have added a type filed to specify if the location is 
a port or region or maybe something new in the future (let's say airport) here is the design of the new DB
![alt text](https://00e9e64bac96a3bcdf69a3a01b426ea97bf1314ce18716cc7e-apidata.googleusercontent.com/download/storage/v1/b/staging.menadx-storybook.appspot.com/o/rates.png?qk=AD5uMEuGyi-JuxlkcuF_2E4O0pIXjnq_IQFhfyrp6vUJF4D4L7kFhC-fp7A7kWsgPIc1ZWykyJ4pUw2HoOqABwy828czcFsQwbiWNFKwkmjpQKVM_j8ysmsUOho3km1Xb-Jyu8DDOQgrm02R1OeiuDo8y1fBRdwRAtbcWF1fvdLXosGysdJsfe_fWz_FQwCjXS7Z5PCXeTkr5PX9NadxvjivBjaZKb2GBhIuVQD1Uv-ZNJ6D1QsCbY0BdSYRkSjy1T6AqJ_rqd6lEVqf6-IA6PadFKZQOV2vBLOgEKhhWQG5Cv262gA8nfka06-yARtlC6iQoFT3hdyLUDDDmc6trHpsZ2vyPmsATHFLyVUm5G4IY1wf0fFaXxdeqiBGpSTuCyw2RGnsF9ETl6P_agPHKng6opsJJcTw4h1ikFfv1Ox_9Cu3--MF45jpn7_Cy1OzZn-2ct_bJQY3iwIjGIptWpFEbeVaf1CDiRfiWHaGRXoF6VSG3YM1LrgP8Z76LaYKlxAa20iun1ppItlDLulp8GCeCHDYDreFw0f8YVl_qutibpCtl_zcD94xdQylI8rJKfuqtrbqe9HJvINcTSsxhPOs8uWMj_tjAu5KHAVWmw7rdprAUZhdQdHNruehIt0x0ZTp4T4EcXJPxQXlQVgH7Sz9RSGYiQbBo_IzV2383HnwXNwy9IvGBU-4QBXzPY_OtvghJaYfZ_P8-kWS9zPW3mJ_LeaniZ-Krylq1ci6yHUzW1ggAWDa6-uDCkvDpzko1lKH6rqpLoSMKgyQNqGsuHAXwYkAaSbsUuCMA5vWXYmqMEKTTZcE9iY)
I noticed also that new DB design perform much better in some type of queries and the same in most queries
I setup for the that a profiling decorator ([you find it here](https://github.com/proserve/ratetask/blob/master/helpers/helpers.py#L45)).
 
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


## Batch Processing

