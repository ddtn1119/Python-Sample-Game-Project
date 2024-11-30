from flask import Flask, request, jsonify
import random
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')  # Update region if needed
table = dynamodb.Table('Guess-the-Number-Game-Database')  # Replace with your table name

# In-memory storage for active games
games = {}

# Route to start a new game
@app.route('/start-game', methods=['POST'])
def start_game():
    data = request.json
    player_id = data.get('player_id')
    if not player_id:
        return jsonify({"error": "Player ID is required"}), 400
    
    # Initialize a new game
    secret_number = random.randint(1, 100)
    games[player_id] = {
        "secret_number": secret_number,
        "num_guesses": 0
    }
    return jsonify({"message": "Game started!", "player_id": player_id}), 200

# Route to make a guess
@app.route('/make-guess', methods=['POST'])
def make_guess():
    data = request.json
    player_id = data.get('player_id')
    guess = data.get('guess')

    if not player_id or guess is None:
        return jsonify({"error": "Player ID and guess are required"}), 400

    game = games.get(player_id)
    if not game:
        return jsonify({"error": "No active game found for this Player ID"}), 404

    game["num_guesses"] += 1
    if guess == game["secret_number"]:
        # Store game result in DynamoDB
        try:
            table.put_item(
                Item={
                    'PlayerID': player_id,
                    'NumGuesses': game["num_guesses"]
                }
            )
        except ClientError as e:
            return jsonify({"error": f"Failed to save data: {e.response['Error']['Message']}"}), 500

        # End the game
        del games[player_id]
        return jsonify({"message": "You guessed it!", "num_guesses": game["num_guesses"]}), 200

    return jsonify({"hint": "Guess lower!" if guess > game["secret_number"] else "Guess higher!"}), 200

# Health check route
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "Running"}), 200

if __name__ == '__main__':
    app.run(debug=True)
