if  you are using mac you need to install postgres in your machine to be able to install dependencies in requirements.txt
```shell
brew install postgresql
```  
## progress
##### - GET requirements ==> done
##### - POST requirements ==> in-progress
##### - Batch processing ==> in-progress
## Test
form root directory run
```shell 
pytest
```

## Run app
#### Run the docker container
```shell 
docker build -t ratestask . # to be run only first time
docker run -p 0.0.0.0:5432:5432 --name ratestask ratestask
```
#### rename the .env_copy to .env
```shell 
mv .env_copy .env
```
#### run the app
```shell 
python app.py
```