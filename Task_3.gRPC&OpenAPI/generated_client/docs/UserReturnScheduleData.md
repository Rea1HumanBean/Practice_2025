# UserReturnScheduleData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name_medication** | **str** | Название лекарства | 
**first_day** | **date** | Название лекарства | 
**limitation_days** | **int** | Сколько дней составлять расписание | [optional] 
**daily_schedule** | **List[str]** | Сколько приёмов лекарства в день | 

## Example

```python
from openapi_client.models.user_return_schedule_data import UserReturnScheduleData

# TODO update the JSON string below
json = "{}"
# create an instance of UserReturnScheduleData from a JSON string
user_return_schedule_data_instance = UserReturnScheduleData.from_json(json)
# print the JSON string representation of the object
print(UserReturnScheduleData.to_json())

# convert the object into a dict
user_return_schedule_data_dict = user_return_schedule_data_instance.to_dict()
# create an instance of UserReturnScheduleData from a dict
user_return_schedule_data_from_dict = UserReturnScheduleData.from_dict(user_return_schedule_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


