# fdk-reports-bff

## Developing
### Setup
```
% pip install pipenv    # package management tool
% pip install invoke    # a task execution tool & library
% pip install pytest    # test framework
% pipenv install --dev  # install packages from Pipfile including dev
```


#### Run application 

```
% docker-comopose up -d                             # start mockserver
% pipenv shell                                      # open a session in the virtual environment
% FLASK_APP=src FLASK_ENV=development flask run     # run application
```
## Testing
### Running tests
```
% invoke unit-test
options:
--install: install pip-dependencies, used by github actions
```
```
% invoke contract-test 
options:
--build: build image for testing before run
--compose: start docker compose for testing before run
--image: name of the image that should be tested. Defaults to digdir/fulltext-search:latest
```
#### Updating mock data
1. delete data for the url in ./mock/mappings
2. Start wiremock: `docker-compose up` 
3. Start [record and playback](http://wiremock.org/docs/record-playback/) with target url 
4. run the wanted http requests (replace the target url with `localhost:8080`) 

### Other invoke tasks
```
build-image                 # build docker image
options:
--tags                      # commaseperated list of tags for image        
```

```
stop-docker        #shut down containers used in contracttests
options:
--clean                      #remove associated containers and networks
--remove                     #remove associated containers, networks and images   
```
 
``` 
record_harvest_data # record mock_dat from harvesters, prerequisite: wiremock running record and playback on root url
--old                      # wether to record data from old (as opposed to new) harvesters, defaults to false 
--env                      # which environment that should be updated (must be same as target for recordings). Defaults to production  
```

## Troubleshooting
### Mac: unknown locale: UTF-8 in Python
`open ~/.bash_profile:`

```
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
```
restart terminal