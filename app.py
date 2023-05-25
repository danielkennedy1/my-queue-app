from chalice import Chalice

# Define the custom authorizer function
def key_is_valid(key):
    if key not in ["87dc40dd-f1b8-46ba-a7b5-10de5bca8d0e"]:
        return False
    return True

app = Chalice(app_name='my-queue-app')
queue = []

@app.route('/')
def hello_world():
    return "Your key is: " + app.current_request.headers['x-api-key']

@app.route('/reset', methods=['DELETE'])
def clear():
    if not key_is_valid(app.current_request.headers['x-api-key']):
        return "Invalid API Key", 403
    queue.clear()
    return "Success", 204

@app.route('/add/{element}', methods=['PUT'])
def add_element(element):
    queue.append(element)
    return "Success", 201

@app.route('/peek', methods=['GET'])
def get_next():
    if len(queue) == 0:
        return "Queue empty", 204
    return queue[0]

@app.route('/next', methods=['DELETE'])
def remove_next():
    if not key_is_valid(app.current_request.headers['x-api-key']):
        return "Invalid API Key", 403
    if len(queue) == 0:
        return "Queue Empty", 204
    return queue.pop(0)

@app.route('/size', methods=['GET'])
def get_size():
    return str(len(queue))

@app.route("/position/{element}", methods=['GET'])
def get_position(element):
    if element not in queue:
        return "Not in Queue", 404
    return str(queue.index(element) + 1)

@app.route("/cancel/{element}", methods=['DELETE'])
def cancel_element(element):
    if not key_is_valid(app.current_request.headers['x-api-key']):
        return "Invalid API Key", 403
    if element not in queue:
        return "Not in Queue", 404
    queue.remove(element)
    return "Success", 204
