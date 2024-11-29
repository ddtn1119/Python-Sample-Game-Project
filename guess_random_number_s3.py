import random
import boto3
from botocore.exceptions import NoCredentialsError

# Initialize the S3 client
s3 = boto3.client('s3')
bucket_name = 'guess-the-number-game-data-bucket'  # Replace with your bucket name

# Function to upload game data to S3
def upload_game_data_to_s3(player_id, num_guesses):
    game_data = f"Player ID: {player_id}\nNumber of Guesses: {num_guesses}\n\n"
    file_name = 'game_data.txt'

    try:
        # Upload the file to S3
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=game_data)
        print(f"Game data uploaded to S3 for player {player_id}.")
    except NoCredentialsError:
        print("No valid AWS credentials found. Please configure them.")
    except Exception as e:
        print(f"Error uploading game data to S3: {e}")

def guess_random_number(player_id):
    print("Welcome to Guess the Number!")
    print("Help me guess a number between 1 and 100.")
    num = random.randint(0, 100)
    num_guesses = 0
    while True:
        try:
            guess = int(input("Guess a number between 0 and 100: "))
            num_guesses += 1
            if guess == num:
                print(f"You guessed the number in {num_guesses} tries!")
                upload_game_data_to_s3(player_id, num_guesses)  # Upload game data to S3
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
