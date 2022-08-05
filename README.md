# fdk-reports-bff


## Developing
### Requirements
- [poetry](https://python-poetry.org/)
- [nox](https://nox.thea.codes/en/stable/)
- [nox-poetry](https://pypi.org/project/nox-poetry/)

### Install software:
```
% pip install poetry==1.1.7
% pip install nox==2021.6.12
% pip install nox-poetry==0.8.6
% poetry install
```

### Running the service locally
```
% docker-compose up -d
% poetry shell
% FLASK_APP=fdk_reports_bff FLASK_ENV=development flask run --port=5000
```

## Testing
### Running tests
#### All tests
```
% nox
```

#### Unit tests
```
% nox -s unit_tests
```

#### Contract tests
```
% nox -s contract_tests
```

### FetchServiceException when updating data
 1. Check if mock server is running:  `GET /http://localhost:8080/organizations`  
 2. If no response restart containers

For other mock data issues see [mock_data.md in readme resources](readme_resources/mock_data.md)

### ConnectionError etc. when updating data
1. Check if elasticsearch is running and available `GET http://localhost:9200/`
2. If no response restart containers

### ElasticSearch: no indexed data

`To manually update data, post request:`

```
http://localhost:5000/updates?ignore_previous=true
```
