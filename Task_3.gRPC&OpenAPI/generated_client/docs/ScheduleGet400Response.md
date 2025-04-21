# ScheduleGet400Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**error** | **str** | Описание ошибки | [optional] 
**details** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.schedule_get400_response import ScheduleGet400Response

# TODO update the JSON string below
json = "{}"
# create an instance of ScheduleGet400Response from a JSON string
schedule_get400_response_instance = ScheduleGet400Response.from_json(json)
# print the JSON string representation of the object
print(ScheduleGet400Response.to_json())

# convert the object into a dict
schedule_get400_response_dict = schedule_get400_response_instance.to_dict()
# create an instance of ScheduleGet400Response from a dict
schedule_get400_response_from_dict = ScheduleGet400Response.from_dict(schedule_get400_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


