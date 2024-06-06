import string
from collections import defaultdict
import data


def find_letter_count(possiblewords, known_positions):
    lettercount = {}
    for letter in set(string.ascii_lowercase):
        lettercount[letter] = sum(letter == word[position] for word in possiblewords for position in [item for item in list(range(5)) if item not in known_positions])
    return {k: v for k, v in sorted(lettercount.items(), key=lambda item: item[1], reverse=True)}


def find_positional_counts(possiblewords, position):
    lettercount = {}
    for letter in set(string.ascii_lowercase):
        lettercount[letter] = sum(letter == word[position] for word in possiblewords)
    return lettercount


def find_word_scores(possiblewords, scorelist, known_positions):
    wordscores, top_scoring, i = defaultdict(list), [], 0
    letterscores = find_letter_count(scorelist, known_positions)
    positionscores = {position: find_positional_counts(scorelist, position) for position in [item for item in list(range(5)) if item not in known_positions]}
    for word in possiblewords:
        score = sum(letterscores[letter] for letter in set(word)) + sum(positionscores[position][word[position]] for position in [item for item in list(range(5)) if item not in known_positions])
        wordscores[score] = wordscores[score] + [word]
    wordscores = {k: v for k, v in sorted(wordscores.items(), key=lambda item: item[1], reverse=True)}
    while len(top_scoring) < 10 and len(top_scoring) != len(possiblewords):
            for word in wordscores[sorted(list(wordscores.keys()), reverse=True)[i]]:
                top_scoring.append(word)
            i += 1
    return top_scoring


def get_top_words(possiblewords, known_letters, known_positions):
    if len(possiblewords) > 2:
        improvement_words = []
        for i in range(6):
            top_scoring = find_word_scores(data.get_valid_words(), possiblewords, known_positions)
            improvement_words.extend([word for word in top_scoring if len(set(letter for letter in word[0])) == 5 and sum(letter in known_letters for letter in word[0]) == i]) 
            improvement_words.extend([word for word in top_scoring if word not in improvement_words and sum(letter in known_letters for letter in word) == i])
            if len(improvement_words) > 0:
                return improvement_words
            if i == 4:
                return possiblewords[:10] if len(possiblewords) > 10 else possiblewords
    return possiblewords


def auto_solve(answer, display=True):
    wordlist = data.get_soultion_words()
    correct_positions, incorrect_positions, rejected_letters, j = dict(), defaultdict(list), [], 0
    while True:
        solutionlist = [word for word in wordlist if all(letter in word for letter in set(sum([item for item in incorrect_positions.values()], []))) and all(letter not in word for letter in rejected_letters) and (all(word[position] == correct_positions[position] for position in correct_positions.keys()) if len(correct_positions.keys()) > 0 else True) and not any(word[position] in incorrect_positions[position] for position in incorrect_positions.keys())]
        solutionpicks = get_top_words(solutionlist, correct_positions.values(), list(correct_positions.keys()))
        attempt = solutionpicks[0]
        if display is True:
            print(attempt)
        # Gather response data
        for position in range(5):
            if attempt[position] == answer[position]:
                correct_positions[position] = attempt[position]
        for position in range(5):
            if attempt[position] not in answer and attempt[position] not in correct_positions.values():
                rejected_letters.append(attempt[position])
            elif attempt[position] != answer[position]:
                incorrect_positions[position] = incorrect_positions[position] + [attempt[position]]
        j += 1
        if attempt == answer:
            break
    if display is True:
        print(f"Solved the wordle for \"{answer}\" in {j} attempts")
    return j


def solve():
    wordlist = data.get_soultion_words()
    correct_positions, incorrect_positions, rejected_letters = dict(), defaultdict(list), []
    while True:
        solutionlist = [word for word in wordlist if all(letter in word for letter in set(sum([item for item in incorrect_positions.values()], []))) and all(letter not in word for letter in rejected_letters) and (all(word[position] == correct_positions[position] for position in correct_positions.keys()) if len(correct_positions.keys()) > 0 else True) and not any(word[position] in incorrect_positions[position] for position in incorrect_positions.keys())]
        solutionpicks = get_top_words(solutionlist, correct_positions.values(), list(correct_positions.keys()))
        print(f"Select{' from' if len(solutionpicks) > 1 else ''}: {solutionpicks if len(solutionpicks) > 1 else solutionpicks[0]}")

        # Gather response data
        if input("Success? ").lower() in ["yes", "y"]: exit()
        correct_positions_input = input("Correct positions (e.g. 2e 4c): ").lower()
        if len(correct_positions_input) > 0:
            correct_positions.update({int(part[0]) - 1: part[1] for part in correct_positions_input.split(" ")})
        rejected_letters.extend([letter for letter in input("Rejected letters: ").lower() if letter not in correct_positions.values()])
        incorrect_positions_input = input("Incorrect positions (e.g. 2e 4c): ").lower()
        if len(incorrect_positions_input) > 0:
            for part in incorrect_positions_input.split(" "):
                incorrect_positions[int(part[0]) - 1] = incorrect_positions[int(part[0]) - 1] + [part[1]]


def measure_performance():
    answerlist = data.get_soultion_words()
    total_words, solutions, max_attempt, i = len(answerlist), defaultdict(int), (0, ""), 0
    for answer in answerlist:
        attempts = auto_solve(answer, False)
        if attempts > max_attempt[0]:
            max_attempt = (attempts, answer)
        solutions[attempts] = solutions[attempts] + 1
        if i % 23 == 0:
            print(str(int(i/total_words * 100)) + "%")
        i += 1
            
    print(f"Quickest solve: {min(solutions.keys())}")
    print(f"Slowest solve: {max(solutions.keys())}")
    print(f"Average solve: {sum(key * value for key, value in solutions.items()) / sum(solutions.values())}")
    print(f"Worst performer: {max_attempt}")
    print(f"Number of wordles not solved in six attempts or fewer: {sum(value for value in solutions.keys() if value > 6)}")
    # score to beat 3.679


if __name__ == "__main__":
    solve()
    # measure_performance()
    # auto_solve("solar") 