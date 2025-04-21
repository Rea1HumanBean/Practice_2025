# ScheduleGet200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_id** | **int** |  | [optional] 
**schedule_id** | **int** |  | [optional] 
**name_pills** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.schedule_get200_response import ScheduleGet200Response

# TODO update the JSON string below
json = "{}"
# create an instance of ScheduleGet200Response from a JSON string
schedule_get200_response_instance = ScheduleGet200Response.from_json(json)
# print the JSON string representation of the object
print(ScheduleGet200Response.to_json())

# convert the object into a dict
schedule_get200_response_dict = schedule_get200_response_instance.to_dict()
# create an instance of ScheduleGet200Response from a dict
schedule_get200_response_from_dict = ScheduleGet200Response.from_dict(schedule_get200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


