from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    rm_output = None
    rm_table = None
    plate_output = None
    plate_used = None
    error = None

    if request.method == "POST":
        mode = request.form.get("mode")

        if mode == "rm":
            try:
                weight = int(request.form.get("weight_used"))
                reps = int(request.form.get("reps"))
            except:
                error = "Please enter whole numbers."
                return render_template("index.html", error=error)

            if reps <= 0 or reps > 10:
                error = "invalid rep count"
            else:
                Brzycki = weight * (36 / (37 - reps))
                Lander = weight * (100 / (101.3 - (2.67123 * reps)))
                RPM = int(((Brzycki + Lander) / 2) // 1)

                rm_output = RPM

                training_table = [50, 52.5, 55, 57.5, 60, 62.5, 65, 67.5, 70, 72.5, 75, 77.5,
                                  80, 82.5, 85, 87.5, 90, 92.5, 95, 97.5, 100]

                rm_table = []
                for i in training_table:
                    percent = int(RPM * (i / 100))
                    rm_table.append((i, percent))

        elif mode == "plates":
            try:
                total_weight = int(request.form.get("desired_weight"))
            except:
                error = "Please enter a whole number."
                return render_template("index.html", error=error)

            bar_weight = 45
            both_sides = (total_weight - bar_weight) / 2

            plates = [45, 35, 25, 10, 5, 2.5]
            used = []

            for i in plates:
                count = int(both_sides // i)
                if count > 0:
                    used.append((i, count))
                    both_sides -= i * count

            plate_output = total_weight
            plate_used = used

    return render_template(
        "index.html",
        rm_output=rm_output,
        rm_table=rm_table,
        plate_output=plate_output,
        plate_used=plate_used,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)
