import requests
import json


def asana_request(url, data, method):
    url = "https://app.asana.com/api/1.0/" + url
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer 0/6179ee23d060cf637b048019515a9627"
    }

    response = requests.request(method, url, verify=False, data=data, headers=headers)

    data = json.loads(response.text)
    print('111111111111111')
    print(data)
    print('6666666666666')
    if data['data']:
        return data['data']['gid']
    else:
        return False


def create_project(name):
    url = "projects"
    data = {'data': {'name': name, 'workspace': '1151586388166420'}}
    return asana_request(url, json.dumps(data), "POST")


def update_project_name(project_id, name):
    url = "projects/" + project_id
    data = {'data': {'name': name}}
    return asana_request(url, json.dumps(data), "PUT")


def create_task(text, user_id, project_id):
    url = "tasks"
    data = {"data": {"name": text, "assignee": user_id, "assignee_status": "upcoming", "projects": [project_id],
                     "workspace": "1151586388166420"}}
    return asana_request(url, json.dumps(data), "POST")


def change_task_project(task_id, old_project_id, new_project_id):
    url = "tasks/" + str(task_id) + "/addProject"
    data = {'data': {'project': new_project_id, 'insert_before': None}}
    asana_request(url, json.dumps(data), "POST")
    url = "tasks/" + str(task_id) + "/removeProject"
    data = {'data': {'project': old_project_id}}
    asana_request(url, json.dumps(data), "POST")


def update_task(task_id, name, user_id, project_id):
    url = "tasks/" + str(task_id)
    data = {"data": {"name": name, "assignee": str(user_id)}}
    return asana_request(url, json.dumps(data), "PUT")