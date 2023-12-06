from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
# In-memory data store (replace this with a database in a real-world scenario)
users = {}

# Endpoint to get all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify({'users': users})

# Endpoint to get a specific user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify({'user': user})
    else:
        return jsonify({'error': 'User not found'}), 404

# Endpoint to create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    # Ensure required fields are present
    if 'name' not in data or 'email' not in data:
        return jsonify({'error': 'Name and email are required'}), 400

    # Generate a new user ID
    new_user_id = len(users) + 1

    # Create the new user
    new_user = {'id': new_user_id, 'name': data['name'], 'email': data['email']}
    users[new_user_id] = new_user

    return jsonify({'message': 'User created successfully', 'user': new_user}), 201

# Endpoint to update an existing user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()

    # Update user data
    user['name'] = data.get('name', user['name'])
    user['email'] = data.get('email', user['email'])

    return jsonify({'message': 'User updated successfully', 'user': user})

# Endpoint to delete a user
@app.route('/users', methods=['DELETE'])
def delete_user():
    global users
    users = {}
    return jsonify({'message': 'All users deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
