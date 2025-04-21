# openapi_client.DefaultApi

All URIs are relative to *http://localhost:5000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**next_takings_get**](DefaultApi.md#next_takings_get) | **GET** /next_takings | Получение актуального расписания пользователю (По умолчанию на час вперёд)
[**schedule_get**](DefaultApi.md#schedule_get) | **GET** /schedule | Получение конкретного расписания
[**schedule_post**](DefaultApi.md#schedule_post) | **POST** /schedule | Добавление расписания приёма лекарств для пользователя
[**schedules_get**](DefaultApi.md#schedules_get) | **GET** /schedules | Получение всех расписаний приёма лекарств пользователя


# **next_takings_get**
> List[ReturnUserActualSchedule] next_takings_get(user_id)

Получение актуального расписания пользователю (По умолчанию на час вперёд)

Получение актуального расписания по user_id

### Example


```python
import openapi_client
from openapi_client.models.return_user_actual_schedule import ReturnUserActualSchedule
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:5000
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:5000"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    user_id = 56 # int | ID пользователя

    try:
        # Получение актуального расписания пользователю (По умолчанию на час вперёд)
        api_response = api_instance.next_takings_get(user_id)
        print("The response of DefaultApi->next_takings_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->next_takings_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **int**| ID пользователя | 

### Return type

[**List[ReturnUserActualSchedule]**](ReturnUserActualSchedule.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Успешный запрос |  -  |
**400** | Некорректные данные запроса |  -  |
**404** | Расписание не найдено |  -  |
**500** | Внутренняя ошибка сервера |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **schedule_get**
> ScheduleGet200Response schedule_get(user_id, schedule_id)

Получение конкретного расписания

Возвращает расписание по user_id и schedule_id

### Example


```python
import openapi_client
from openapi_client.models.schedule_get200_response import ScheduleGet200Response
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:5000
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:5000"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    user_id = 56 # int | ID пользователя
    schedule_id = 56 # int | ID расписания

    try:
        # Получение конкретного расписания
        api_response = api_instance.schedule_get(user_id, schedule_id)
        print("The response of DefaultApi->schedule_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->schedule_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **int**| ID пользователя | 
 **schedule_id** | **int**| ID расписания | 

### Return type

[**ScheduleGet200Response**](ScheduleGet200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Успешный запрос |  -  |
**400** | Некорректные данные запроса |  -  |
**404** | Расписание не найдено |  -  |
**500** | Внутренняя ошибка сервера |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **schedule_post**
> object schedule_post(data_of_user_request)

Добавление расписания приёма лекарств для пользователя

Создает новое расписание приема лекарств для указанного пользователя

### Example


```python
import openapi_client
from openapi_client.models.data_of_user_request import DataOfUserRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:5000
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:5000"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    data_of_user_request = openapi_client.DataOfUserRequest() # DataOfUserRequest | 

    try:
        # Добавление расписания приёма лекарств для пользователя
        api_response = api_instance.schedule_post(data_of_user_request)
        print("The response of DefaultApi->schedule_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->schedule_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_of_user_request** | [**DataOfUserRequest**](DataOfUserRequest.md)|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Расписание успешно создано |  -  |
**400** | Некорректные данные запроса |  -  |
**500** | Внутренняя ошибка сервера |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **schedules_get**
> List[UserReturnScheduleData] schedules_get(user_id)

Получение всех расписаний приёма лекарств пользователя

Возвращает все расписания пользователя

### Example


```python
import openapi_client
from openapi_client.models.user_return_schedule_data import UserReturnScheduleData
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:5000
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:5000"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    user_id = 56 # int | ID пользователя

    try:
        # Получение всех расписаний приёма лекарств пользователя
        api_response = api_instance.schedules_get(user_id)
        print("The response of DefaultApi->schedules_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->schedules_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **int**| ID пользователя | 

### Return type

[**List[UserReturnScheduleData]**](UserReturnScheduleData.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Успешный запрос |  -  |
**400** | Некорректные данные запроса |  -  |
**404** | Расписание не найдено |  -  |
**500** | Внутренняя ошибка сервера |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

