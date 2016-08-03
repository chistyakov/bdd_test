# Task from job interview
## Task
> 1. Написать на Python Web-сервис(заглушку), такой, что:
>  * принимает по http параметр - id
>  * на основе полученного id возвращает json с ФИО пользователя
> 2. Написать на Python автотесты для функционального тестирования этого Web-сервиса 


> 1. Write a Python web-service (stub). It should:
>  * receive the parameter 'id' via HTTP
>  * return JSON with full name of user by id
> 2. Write autotest for functional testing of the web-service using Python

## How to run
```shell
vagrant up
vagrant ssh
```

### Run server
```shell
/vagrant/main.py
```
The server uses the port 8080

### Run autotests

#### Acceptance tests
```shell
cd /vagrant
behave
```

#### Unit tests
```shell
cd /vagrant
python -m unittest unittest_main
```
