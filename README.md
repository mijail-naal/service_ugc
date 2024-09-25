# Проектная работа 8 спринта

### [UGC_Sprint_1](https://github.com/mijail-naal/ugc_sprint_1)


[Приглашение](https://github.com/mijail-naal/ugc_sprint_1/invitations)


<br>


## UGC Service


### Развертывание
#####  *ugc_sprint_1/docker-compose.yml*

```Bash
docker compose up --build -d
```

<br>


### Запуск тестов API

```Bash
docker exec -it ugc sh -c "python3 -m pytest"
```

<br> 


### Запуск ETL 
#####  *etl/docker-compose.yml - (После успешного запуска сервисов Kafka и Clickhouse)*

```Bash
docker start ugc_etl
```

<br>


### Пример сообщение в Kafka 

| KEY              | VALUE               
| ----------       |--------------------------
| user_123         | CLICK - event description - created - start time - end time               
|

<br>


### Пример сохранения данных в Clickhouse

| user_id     | action      | description         | event_time          | start_time    | end_time     
|-------------|-------------|---------------------|---------------------|---------------|---------------
| user_123    | CLICK       | event description   | 01/02/2024 08:40:00 | 08:46:00      | 09:47:00 
| user_456    | VIEW        | event description   | 03/02/2024 12:00:00 | 16:34:36      | 16:52:27 
| user_123    | VIEW        | event description   | 05/02/2024 06:30:00 | 06:35:00      | 09:47:00 
|  


<br>


## Архитектура

<br>


![Diagram](architecture/diagram.png)

<br>


### Тестирование хранилищ

[Clickhouse](https://github.com/mijail-naal/ugc_sprint_1/tree/main/storage_comparison)  [Vertica](https://github.com/mijail-naal/ugc_sprint_1/tree/main/storage_comparison) [PostgreSQL](https://github.com/mijail-naal/ugc_sprint_1/tree/main/storage_comparison)


<br>


# Проектная работа 8 спринта

Проектные работы в этом модуле выполняются в командах по 3-4 человека. Процесс обучения аналогичен сервису, где вы изучали асинхронное программирование. Роли в команде и отправка работы на ревью не меняются.

Распределение по командам подготовит команда сопровождения. Куратор поделится с вами списками в Пачке в канале #group_projects.

Задания на спринт вы найдёте внутри тем.
