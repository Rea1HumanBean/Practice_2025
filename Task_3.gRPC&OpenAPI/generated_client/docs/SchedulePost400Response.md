# SchedulePost400Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**error** | **str** | Описание ошибки | [optional] 
**details** | **str** | Детали ошибки | [optional] 

## Example

```python
from openapi_client.models.schedule_post400_response import SchedulePost400Response

# TODO update the JSON string below
json = "{}"
# create an instance of SchedulePost400Response from a JSON string
schedule_post400_response_instance = SchedulePost400Response.from_json(json)
# print the JSON string representation of the object
print(SchedulePost400Response.to_json())

# convert the object into a dict
schedule_post400_response_dict = schedule_post400_response_instance.to_dict()
# create an instance of SchedulePost400Response from a dict
schedule_post400_response_from_dict = SchedulePost400Response.from_dict(schedule_post400_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


