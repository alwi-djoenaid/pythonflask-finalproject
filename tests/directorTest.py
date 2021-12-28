from flask import Flask
import json
import config

connexApp = config.connex_app
connexApp.add_api('swagger.yml')
connexApp = connexApp.app
client = connexApp.test_client()

def testBaseRoute():
    """
        Menguji get all directors
    """

    url = "api/directors"

    response = client.get(url)
    assert response.status_code == 200

def testPostRoute():
    """
        Untuk menjalankan test ini, setiap melakukan test
        harap mengubah atribut name pada mockPayload,
        karena terdapat validasi bahwa atribut tsb bersifat unik
    """

    url = "api/directors"

    requestHeaders = {
        'Content-Type': 'application/json'
    }

    mockPayload = {
        "department": "Directing",
        "gender": 2,
        "name": "Bart",
        "uid": 12345
    }

    response = client.post(url, data = json.dumps(mockPayload), headers=requestHeaders)
    assert response.status_code == 201

def testPutRoute():
    """
        Menguji method PUT untuk api Directors
    """

    requestHeaders = {
        'Content-Type': 'application/json'
    }

    url = "api/directors/7114"

    mockPayload = {
        "department": "Animation",
        "gender": 2,
        "name": "Homer",
        "uid": 54321
    }

    response = client.put(url, data = json.dumps(mockPayload), headers=requestHeaders)
    assert response.status_code == 200