import requests

# The POST request to our node server
def drawLandmarks(landmarks):
    # print('recvei:', landmarks)
    res = requests.post('http://127.0.0.1:3000/landmarks', json=landmarks)
    returned_data = res.json()
    result = returned_data['received']
    print("Response fro JS:", result)




