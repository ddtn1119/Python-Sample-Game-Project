import pygame
import random
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# Initialize the S3 client
s3 = boto3.client('s3')
bucket_name = 'guess-the-number-game-data-bucket'

def upload_game_data_to_s3(player_id, num_guesses):
    game_data = f"Player ID: {player_id}\nNumber of Guesses: {num_guesses}\n\n"
    file_name = 'game_data.txt'
    try:
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=game_data)
        print(f"Game data uploaded to S3 for player {player_id}.")
    except NoCredentialsError:
        print("No valid AWS credentials found. Please configure them.")
    except Exception as e:
        print(f"Error uploading game data to S3: {e}")

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Guess-the-Number-Game-Database')

def store_game_data(player_id, num_guesses):
    try:
        table.put_item(
            Item={
                'PlayerID': player_id,
                'NumGuesses': num_guesses
            }
        )
        print(f"Game data saved for {player_id}.")
    except ClientError as e:
        print(f"Error saving game data: {e.response['Error']['Message']}")

def guess_random_number(player_id):
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Guess the Number")
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    num = random.randint(1, 100)
    num_guesses = 0
    user_input = ''
    message = "Guess a number between 1 and 100"
    running = True

    while running:
        screen.fill((255, 255, 255))

        # Render the message
        text_surface = font.render(message, True, (0, 0, 0))
        screen.blit(text_surface, (50, 50))

        # Render the user's input
        input_surface = font.render(user_input, True, (0, 0, 0))
        screen.blit(input_surface, (50, 150))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        guess = int(user_input)
                        num_guesses += 1
                        if guess == num:
                            message = f"Correct! Guessed in {num_guesses} tries!"
                            store_game_data(player_id, num_guesses)
                            upload_game_data_to_s3(player_id, num_guesses)
                            running = False
                        elif guess > num:
                            message = "Guess lower!"
                        else:
                            message = "Guess higher!"
                        user_input = ''
                    except ValueError:
                        message = "Enter a valid number!"
                        user_input = ''
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

        clock.tick(30)

    pygame.quit()

def main():
    player_id = input("Enter your Player ID: ")
    guess_random_number(player_id)

if __name__ == "__main__":
    main()
