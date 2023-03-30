import pytest
import requests

HOSTNAME = "0.0.0.0:8000" 

@pytest.fixture(scope="session", params=[
    "https://upload.wikimedia.org/wikipedia/commons/2/29/Aesir_amstaffs_2016_blue_puppies.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/6/69/Rottweiler_-52773841920.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Kot-027.jpg/1280px-Kot-027.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/b/bb/Kittyply_edit1.jpg"
])
def test_image_url(request):
    return {"image_url": request.param}

def test_predict(test_image_url):
    response = requests.post(f"http://{HOSTNAME}/predict/", json=test_image_url)
    print(response.content)
    print(response.reason)
    print(response.text)
    assert response.status_code == 200

    response_data = response.json()
    assert "dog" in response_data
    assert "cat" in response_data
    assert isinstance(response_data["dog"], float)
    assert isinstance(response_data["cat"], float)
    assert response_data["dog"] + response_data["cat"] == pytest.approx(1.0, rel=1e-5)
