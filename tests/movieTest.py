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

    url = "api/Movies"

    response = client.get(url)
    assert response.status_code == 200

def testTopFiveMovies():
    """
        Menguji API GET api/Movies/top5movies
    """

    url = "api/Movies/top5movies"

    response = client.get(url)
    assert response.status_code == 200

def testTopFiveRevenue():
    """
        Menguji API GET api/Movies/top5revenue
    """

    url = "api/Movies/top5revenue"

    response = client.get(url)
    assert response.status_code == 200