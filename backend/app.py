from flask import Flask, request, redirect;

from model.predictor import predict_disease



app = Flask(
    __name__,
    template_folder="../frontend",
    static_folder="../frontend"
)

@app.route("/profile")
def profile():
    return app.send_static_file("profile.html")

@app.route("/index")
@app.route("/index.html")
def index():
    return app.send_static_file("index.html")


@app.route("/analysis")
def analysis():
    return app.send_static_file("analysis.html")


@app.route("/result-page")
def result_page():
    return app.send_static_file("result.html")


@app.route("/theme.css")
def theme_css():
    return app.send_static_file("theme.css")


@app.route("/theme.js")
def theme_js():
    return app.send_static_file("theme.js")



@app.route("/result", methods=["POST"])
def result():
    selected_symptoms = request.form.getlist("symptoms")
    animal_data = app.config.get("animal_data", {})

    prediction = predict_disease(animal_data, selected_symptoms)

    app.config["prediction"] = prediction
    app.config["symptoms"] = selected_symptoms

    return redirect("/analysis")



@app.route("/get-result")
def get_result():
    prediction = app.config.get("prediction", {})
    symptoms = app.config.get("symptoms", [])

    return {
        "disease": prediction.get("disease", "Unknown"),
        "confidence": int(prediction.get("confidence", 0) * 100),
        "risk": prediction.get("risk", "Low"),
        "symptoms": symptoms
    }




@app.route("/")
def home():
    return app.send_static_file("index.html")

@app.route("/symptoms", methods=["POST"])



def symptoms():
    # collect profile data
    animal_data = {
        "animal_type": request.form.get("animal_type"),
        "age": request.form.get("age"),
        "gender": request.form.get("gender"),
        "weight": request.form.get("weight")
    }

    # store temporarily (demo)
    app.config["animal_data"] = animal_data

    # IMPORTANT: return symptoms.html via Flask
    return app.send_static_file("symptoms.html")

if __name__ == "__main__":
    app.run(debug=True)
