import json
import random


class Question:
    def __init__(self, question_text, answers, correct_answer):
        self.question_text = question_text
        self.answers = answers
        self.correct_answer = correct_answer

    def is_correct(self, answer):
        # Check if the given answer is correct
        return answer == self.correct_answer


def load_questions_from_json(file_path):
    # Load questions from a JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)
    questions = []
    for item in data["trivia_questions"]:
        question = Question(
            item["question"],
            item["answers"],
            item["correct_answer"]
        )
        questions.append(question)
    return questions


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def increment_score(self):
        # Increment the player's score by 1
        self.score += 1

    def get_score(self):
        # Get the player's current score
        return self.score


class TriviaGame:
    def __init__(self, questions, players):
        self.questions = questions
        self.players = players
        self.current_question_index = 0
        self.current_player_index = 0
        self.is_game_over = False
        random.shuffle(self.questions)  # Shuffle the questions for randomness

    def get_current_question(self):
        # Get the current question without advancing the index
        if self.current_question_index < len(self.questions):
            return self.questions[self.current_question_index]
        else:
            return None

    def check_answer(self, question, answer):
        # Check if the answer is correct and update the player's score
        current_player = self.players[self.current_player_index]
        if question.is_correct(answer):
            current_player.increment_score()
            self.current_question_index += 1  # Move to the next question only if the answer is correct
            return True
        else:
            return False

    def next_player(self):
        # Move to the next player in the list
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def get_current_player(self):
        # Get the current player
        return self.players[self.current_player_index]

    def has_more_questions(self):
        # Check if there are more questions and the game is not over
        return self.current_question_index < len(self.questions) and not self.is_game_over

    def get_winner(self):
        # Determine the player with the highest score
        return max(self.players, key=lambda player: player.get_score())

    def end_game(self):
        # Set the game status to over
        self.is_game_over = True


def display_question(question):
    # Display the current question and possible answers
    print(question.question_text)
    for key, value in question.answers.items():
        print(f"{key}: {value}")


def get_user_answer():
    """
    Prompt the user for an answer and validate it.
    Returns the answer if valid (a number between 1 and 4), or None if the user chooses to quit.
    """
    while True:
        answer = input("Your answer (number or . to quit): ")
        if answer == ".":
            return None
        elif answer.isdigit() and 1 <= int(answer) <= 4:
            return answer
        else:
            print("Invalid input. Please enter a number between 1 and 4 or '.' to quit.")


def display_score(score):
    # Display the current score
    print(f"Your current score is: {score}\n")


def display_final_scores(players):
    # Display the final scores of all players
    print("\nFinal Scores:")
    print("-----------------------------")
    print(f"{'Player':<20} {'Score':<5}")
    print("-----------------------------")
    for player in players:
        print(f"{player.name:<20} {player.get_score():<5}")
    print("-----------------------------")


def main():
    # Load questions and initialize players and game
    questions = load_questions_from_json('trivia_questions.json')

    num_players = int(input("Enter number of players: "))
    players = []
    for i in range(num_players):
        player_name = input(f"Enter name for player {i + 1}: ")
        players.append(Player(player_name))

    game = TriviaGame(questions, players)

    while game.has_more_questions():
        question = game.get_current_question()
        current_player = game.get_current_player()
        print(f"{current_player.name}'s turn!\n")
        display_question(question)
        answer = get_user_answer()
        if answer is None:
            game.end_game()  # End the game if the player inputs "."
            break
        if game.check_answer(question, answer):
            print("Correct!")
        else:
            print("Wrong!")
        display_score(current_player.get_score())
        game.next_player()

    display_final_scores(players)
    winner = game.get_winner()
    print(f"Game over! The winner is {winner.name} with a score of {winner.get_score()}")


if __name__ == "__main__":
    main()
