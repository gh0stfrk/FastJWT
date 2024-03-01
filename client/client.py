import requests

# TODO: Complete this wrapper
def verfify_success(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
    return wrapper


URL = "http://localhost:8080"

dummy_user ={
    "email": "dummy@python.org",
    "password": "password"
}

def fill_dummy_users():
    response = requests.get(
        'http://localhost:8080/fill_dummy',
    )


@verfify_success
def create_user():
    response = requests.post(
        URL+'/create_user',
        json=dummy_user
    )
    
    json_response = response.json()
    print(json_response)
    return json_response


def create_a_jwt_token():
    response = requests.post(
        URL+'/auth',
        json=dummy_user
    )
    
    if response.status_code != 200:
        raise Exception('Failed to create a JWT token')
    
    json_response = response.json()
    print("Inside the token", json_response['token'])
    return json_response['token']



def visiting_a_protected_route(token):
    response = requests.get(
        URL+'/protected',
        headers={
            "Auth-Token": token,
            "Nerd-Thing": "Absurd if this works"
        }
    )
    
    if response.status_code != 200:
        raise Exception('Failed to visit a protected route')
    
    json_response = response.json()
    assert json_response['email'] == dummy_user['email']

    return json_response

def test_header(header: dict, path: str):
    response = requests.get(
        URL+path,
        headers=header
    )
    if response.status_code != 200:
        raise Exception('Failed to visit a protected route')

    json_response = response.json()
    print(json_response)
    return json_response
    

if __name__ == "__main__":
    create_user()
    token = create_a_jwt_token()
    print(token) 
    test_header(
        {"Frank-Fruit": "SussyNigga", 
         "Nerd-Thing": "Absurd if this works"}, 
        "/protected/test")
    res = visiting_a_protected_route(token)
    print(res)
    exit(0)