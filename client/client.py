import requests
from requests.cookies import RequestsCookieJar


URL = "http://localhost:8080"


dummy_user ={
    "email": "dummy@python.org",
    "password": "password"
}

def fill_dummy_users():
    response = requests.get(
        'http://localhost:8080/fill_dummy',
    )



def create_user():
    response = requests.post(
        URL+'/create_user',
        json=dummy_user
    )
    
    json_response = response.json()
    print(json_response)
    return json_response


def create_a_jwt_token() -> dict:
    response = requests.post(
        URL+'/auth',
        json=dummy_user
    )
        
    if response.status_code != 200:
        raise Exception('Failed to create a JWT token')
    
    json_response = response.json()
    
    return {
        "token": json_response['token'],
        "refresh_token": response.cookies['refresh-Token']
    }


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


def create_cookie():
    response = requests.get(
        URL+'/auth/cookie',
        json=dummy_user,
        cookies={
            'test-Cookie':'SusValue'
        }
    )
    if response.status_code != 200:
        raise Exception('Failed to create a cookie')
    
    json_response = response.json()
    
    print(response.cookies)
    print(json_response)
    return json_response


def visit_refresh_token(refresh_token):
    jar = RequestsCookieJar()
    jar.set('refresh-Token', refresh_token, path='/')
    response = requests.post(
        URL+'/auth/refresh',
        cookies=jar,
    )
    print(response.cookies)
    print(response.json())
    

if __name__ == "__main__":
    create_user()
    tokens = create_a_jwt_token()
    test_header(
        {"Frank-Fruit": "Fruits-Frankly", 
         "Nerd-Thing": "Absurd if this works"}, 
        "/protected/test")
    create_cookie()
    res = visiting_a_protected_route(tokens.get('token'))
    print(res)
    visit_refresh_token(tokens.get('refresh_token'))
    exit(0)