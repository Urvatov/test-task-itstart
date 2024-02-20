# Тестовое задание Python-разработчик  

Перейдя в /docs, можно проверить работу системы при помощи Swagger Ui.  
![306379071-f3232e3f-a5b5-4e61-8527-b19a55698ed3](https://github.com/Urvatov/test-task-itstart/assets/117490456/31269e11-cdff-4fd2-a934-283fb01faf16)


## Доступные функции:  
### 1. Добавление пользователя:  
![изображение](https://github.com/Urvatov/test-task-itstart/assets/117490456/557951df-2f31-4da0-a1cf-fe675ebd92d0)  
Для добавления пользователя достаточно указать его имя.  

### 2. Добавление устройства:
![изображение](https://github.com/Urvatov/test-task-itstart/assets/117490456/9726d926-b89d-4e71-80ef-eadaee5de8c6)  
Для добавления устройства нужно указать его название и владельца, если таковой имеется.  

### 3. Добавление статистики с устройства:
![изображение](https://github.com/Urvatov/test-task-itstart/assets/117490456/94ad6aeb-13bd-49a9-b54f-95590c5425cc)
Для добавления статистики необходимо указать данные x y z и дату.  
  
Все отправляемые значения из POST запросов сохраняются в базе данных.  

### 4. Получение статистики с утройства по его id:
![изображение](https://github.com/Urvatov/test-task-itstart/assets/117490456/204d08d6-ce49-4b9b-9f8d-967de736e2c1)
![изображение](https://github.com/Urvatov/test-task-itstart/assets/117490456/be2d9ef2-fef2-4751-8f92-08c448d087d8)



### 5. Получение анализа показаний устройства по его id:  
Если выбрать интервал времени, статистика выведется по интервалу. Если не выбирать, то за все время.
![изображение](https://github.com/Urvatov/test-task-itstart/assets/117490456/d828a772-d025-45ad-af5e-f968b7ef7e4a)
![изображение](https://github.com/Urvatov/test-task-itstart/assets/117490456/e4d3d531-731b-4ae9-9b93-cf8beac28265)


### 6. Получение анализа показаний устройств по id пользователя:  
Резуьтат для всех устройств, если не указано id устройства. Либо для каждого устройства отдельно, если указывать.  
![изображение](https://github.com/Urvatov/test-task-itstart/assets/117490456/957d8cad-d3ef-43db-8568-00a115b16eae)
![изображение](https://github.com/Urvatov/test-task-itstart/assets/117490456/f8da2c72-433c-46b7-9c46-16c356e7b364)

## Нагрузочное тестирование через инструмент locust
Результаты:
![изображение](https://github.com/Urvatov/test-task-itstart/assets/117490456/9929d4dc-bafe-45d0-a178-245e17493508)
