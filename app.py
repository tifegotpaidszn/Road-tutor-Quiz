from flask import Flask, render_template, request, session

app = Flask(__name__)

# Needed for session (to track score & current question)
app.secret_key = "roadsense-secret-key"  # change if you want

# Quiz questions
quiz = [
    {
        "sign": "Speed Limit 50",
        "answer": "Speed Limit 50",
        "options": ["Stop", "Speed Limit 50", "Yield", "No Entry"],
        "hint": "Signs with a red circle usually indicate a restriction or prohibition."
    },
    {
        "sign": "Stop Sign",
        "answer": "Stop",
        "options": ["Stop", "Yield", "Go", "No Entry"],
        "hint": "The octagon shape is unique for STOP signs in the UK."
    },
    {
        "sign": "No Entry",
        "answer": "No Entry",
        "options": ["No Entry", "Stop", "Give Way", "Turn Left"],
        "hint": "A red circle with a white horizontal bar means NO ENTRY."
    }
]


@app.route("/", methods=["GET", "POST"])
def index():
    # Initialise session values if first visit
    if "current_index" not in session:
        session["current_index"] = 0
        session["score"] = 0

    current_index = session["current_index"]

    # If user just submitted an answer
    if request.method == "POST":
        selected_option = request.form.get("option")

        # Check answer
        correct_answer = quiz[current_index]["answer"]
        if selected_option == correct_answer:
            session["score"] = session.get("score", 0) + 1

        # Move to next question
        session["current_index"] = current_index + 1
        current_index = session["current_index"]

        # If quiz finished → show result
        if current_index >= len(quiz):
            final_score = session.get("score", 0)
            total = len(quiz)

            # Clear for next run
            session.pop("current_index", None)
            session.pop("score", None)

            return render_template("result.html", final_score=final_score, total=total)

    # Still have questions to show
    question = quiz[current_index]
    progress = f"Question {current_index + 1} of {len(quiz)}"

    return render_template("index.html", question=question, progress=progress)


if __name__ == "__main__":
    app.run(debug=True)
