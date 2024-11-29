import random
import boto3
from botocore.exceptions import ClientError

# Initialize DynamoDB resource with a specified region
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')  # Update region if needed
table = dynamodb.Table('Guess-the-Number-Game-Database')  # Replace with your table name

# Function to store game data in DynamoDB
def store_game_data(player_id, num_guesses):
    try:
        # Save player's guesses count in the DynamoDB table
        response = table.put_item(
            Item={
                'PlayerID': player_id,  # Directly use the player ID string
                'NumGuesses': num_guesses  # Directly use the number for NumGuesses
            }
        )
        print(f"Game data saved for {player_id}.")
    except ClientError as e:
        print(f"Error occurs when saving game data: {e.response['Error']['Message']}")

def guess_random_number(player_id):
    print("Welcome to Guess the Number!")
    print("Help me guess a number between 1 and 100.")
    num = random.randint(1, 100)  # Updated to avoid 0
    num_guesses = 0
    while True:
        try:
            guess = int(input("Guess a number between 1 and 100: "))
            num_guesses += 1
            if guess == num:
                print(f"You guessed the number in {num_guesses} tries!")
                store_game_data(player_id, num_guesses)  # Save game data to DynamoDB
                return True
            elif guess > num:
                print("Guess lower!")
            else:
                print("Guess higher!")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    player_id = input("Enter your Player ID: ")  # Unique identifier for the player
    guess_random_number(player_id)

if __name__ == "__main__":
    main()
