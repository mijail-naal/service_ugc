# Проектная работа 9 спринта

### [UGC_Sprint_2](https://github.com/mijail-naal/ugc_sprint_2)


[Приглашение](https://github.com/mijail-naal/ugc_sprint_2/invitations)


<br>


## UGC Service


### Развертывание
#####  *ugc_sprint_2/docker-compose.yml*

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

<br><br>


## Пример сохранения данных в MongoDB
<br>

### Likes 

| user_id          | film_id                                    | like
| ----------       |-------------------------------------       |----------
| user_123         | d9fb3d50-7415-4779-b780-824659acf34e       | true  
|

### Bookmarks

| user_id          | url                                  
| ----------       |-------------------------------------------
| user_123         |https://github.com/mijail-naal/ugc_sprint_1
|

### Reviews

| user_id     | film_id                              | created_at          | user_review         |
|-------------|--------------------------------------|---------------------|---------------------|
| user_123    | 410c62e1-5bab-4194-a042-304af966d228 | 01/02/2024 08:40:00 | Review from user    |
|

<br>


### Тестирование хранилищ

[MondoDB](https://github.com/mijail-naal/ugc_sprint_2/tree/main/storage_comparison) - [PostgreSQL](https://github.com/mijail-naal/ugc_sprint_2/tree/main/storage_comparison)  

