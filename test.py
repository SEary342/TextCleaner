from textcleaner.textprocess import process_text

config = {
    "remove": ["ID#", "Points:", "Not flagged", "Flag Question", "Question text"],
    "replace": {"IncorrectIncorrect": "Incorrect", "CorrectCorrect": "Correct"},
}

print(process_text("IncorrectIncorrect", config))
