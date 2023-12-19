import json
import random
from difflib import get_close_matches


# Load the knowledge base from a JSON FILE (yap, json))
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, "r", encoding="utf-8") as file:
        data: dict = json.load(file)

    return data


# Save the knowledge base
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


# Find best match in the knowledge base
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None


# Return answer for question
def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if type(q["question"]) == str:
            if q["question"] == question:
                return q["answer"] if type(q["answer"]) == str else random.choice(q["answer"])
        else:
            if question in list(q["question"]):
                return q["answer"] if type(q["answer"]) == str else random.choice(q["answer"])


# Run chatbot. Really, simple run.
def run_assistant():
    knowledge_base: dict = load_knowledge_base("knowledge_base.json")
    while True:
        user_input: str = input("User: ")

        if user_input.lower() == "quit":
            print("Assistant: Goodbye.")
            break

        best_match: str | None = find_best_match(user_input, [element for q in knowledge_base["questions"] for element in q["question"]])

        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f"Assistant: {answer}")
        else:
            print("Bot: I don\'t know the answer. Can you teach me?")
            new_answer: str = input("Type the answer or \"skip\" to skip: ")

            if new_answer.lower() != "skip":
                knowledge_base["questions"].append({
                    "question": user_input,
                    "answer": new_answer
                })
                save_knowledge_base("knowledge_base.json", knowledge_base)

                print("Assistant: Thank you! I learned a new response!")


if __name__ == "__main__":
    run_assistant()
