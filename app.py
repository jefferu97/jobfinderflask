from flask import Flask, render_template, request
import requests

#creating the app 
app = Flask(__name__)

API_URL = "https://remotive.com/api/remote-jobs"

CATEGORIES = [
    "software-dev", "customer-support", "marketing", "sales", 
    "design", "finance", "hr", "writing", "product"
]

#routes 
@app.route("/", methods=["GET", "POST"])
def home():
    jobs = []
    search_term = ""
    selected_category = ""

    if request.method == "POST":
        search_term = request.form.get("search", "").strip()
        selected_category = request.form.get("category", "")

        # Prepare query parameters
        params = {}
        if search_term:
            params["search"] = search_term
        if selected_category:
            params["category"] = selected_category

        # Make API call
        response = requests.get(API_URL, params=params)
        if response.status_code == 200:
            jobs = response.json().get("jobs", [])[:10]  # Get first 10 jobs

    return render_template("index.html", jobs=jobs, categories=CATEGORIES, search_term=search_term, selected_category=selected_category)

if __name__ == "__main__":
    app.run(debug=True)