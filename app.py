from flask import Flask, render_template, request, session

app = Flask(__name__)  # ✅ fixed
app.secret_key = "roadsense-secret-key"

# Quiz questions WITH IMAGE PATHS
quiz = [
    {
        "sign": "Speed Limit 50",
        # make sure this file exists under static/images
        "image": "images/speed_limit_50.jpg",
        "answer": "Speed Limit 50",
        "options": ["Stop", "Speed Limit 50", "Yield", "No Entry"],
        "hint": "Signs with a red circle usually indicate a restriction or prohibition."
    },
    {
        "sign": "Stop Sign",
        "image": "images/stop_sign.jpg",  # static/images/stop_sign.jpg
        "answer": "Stop",
        "options": ["Stop", "Yield", "Go", "No Entry"],
        "hint": "The octagon shape is unique for STOP signs in the UK."
    },
    {
        "sign": "No Entry",
        "image": "images/no_entry.png",  # static/images/no_entry.png
        "answer": "No Entry",
        "options": ["No Entry", "Stop", "Give Way", "Turn Left"],
        "hint": "A red circle with a white horizontal bar means NO ENTRY."
    }
]


@app.route("/", methods=["GET", "POST"])
def index():
    # first visit → init session
    if "current_index" not in session:
        session["current_index"] = 0
        session["score"] = 0

    current_index = session["current_index"]

    if request.method == "POST":
        selected_option = request.form.get("option")
        correct_answer = quiz[current_index]["answer"]

        if selected_option == correct_answer:
            session["score"] += 1

        session["current_index"] += 1
        current_index = session["current_index"]

        # finished quiz → show result
        if current_index >= len(quiz):
            final_score = session["score"]
            total = len(quiz)

            session.pop("current_index", None)
            session.pop("score", None)

            return render_template("result.html", final_score=final_score, total=total)

    # still questions left
    question = quiz[current_index]
    progress = f"Question {current_index + 1} of {len(quiz)}"

    return render_template("index.html", question=question, progress=progress)


if __name__ == "__main__":  # ✅ fixed
    app.run(debug=True)
