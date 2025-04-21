# DataOfUserRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_id** | **int** | ID пользователя | 
**name_pills** | **str** | Название лекарства | 
**limitation_days** | **int** | Сколько дней составлять расписание | 
**number_iters** | **int** | Сколько приёмов лекарства в день | 

## Example

```python
from openapi_client.models.data_of_user_request import DataOfUserRequest

# TODO update the JSON string below
json = "{}"
# create an instance of DataOfUserRequest from a JSON string
data_of_user_request_instance = DataOfUserRequest.from_json(json)
# print the JSON string representation of the object
print(DataOfUserRequest.to_json())

# convert the object into a dict
data_of_user_request_dict = data_of_user_request_instance.to_dict()
# create an instance of DataOfUserRequest from a dict
data_of_user_request_from_dict = DataOfUserRequest.from_dict(data_of_user_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


