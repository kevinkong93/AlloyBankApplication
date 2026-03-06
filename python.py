#flask as main class. render_template to render the HTML form. request to access form data from HTML form submission.
from flask import Flask, render_template, request

#Base64 to encode the token and secret for Basic Auth when I send requests to the Alloy API. 
import base64

# For later when I integrate with Alloy API, I’ll need to import requests and HTTPBasicAuth to send authenticated requests to the API. For now, I’m just printing the captured data to the console.
import requests 
from requests.auth import HTTPBasicAuth

#env variable
import os
from dotenv import load_dotenv
load_dotenv()  # This reads the .env file
#to store token and secret in environment variables for security. I’ll retrieve them in the apply() function when I’m ready to send data to the Alloy API.

#In VS Code terminal, temporarily set environment variables for testing. Worked.
#export ALLOY_TOKEN=your_workflow_token
#export ALLOY_SECRET=your_workflow_secret 

# Parameters confirmed using Alloy API website.
# GET https://sandbox.alloy.co/v1/parameters/ https://developer.alloy.com/public/reference/get_parameters 
# POST https://sandbox.alloy.co/v1/evaluations/ https://developer.alloy.com/public/reference/post_evaluations

# Load Alloy credentials from environment variables
token = os.environ.get("ALLOY_TOKEN")
secret = os.environ.get("ALLOY_SECRET")
if not token or not secret:
    raise ValueError("ALLOY_TOKEN and ALLOY_SECRET should be set in environment variables.")

# Create Basic Auth header 
credentials = f"{token}:{secret}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()
HEADERS = {
    "accept": "qpplication/json",
    "content-type": "application/json",
    "authorization": f"Basic {encoded_credentials}"
}

#inialize Flask app
app = Flask(__name__)

# Route to display the form. The browser sends a GET request when navigating to the page.
@app.route("/")
def form():
    return render_template("form.html")

# Route to handle form submission. The browser sends a POST request when the user clicks Submit. Without the route i’ll get a 404 error.
@app.route("/submit", methods=["POST"])
def submit_application():#captures the form data. request.form contains all submitted form data. I can access each field using request.form["field_name"].
    data = {
        "email_address": request.form["email"], #req
        "phone_number": request.form["phone"],#req
        "address_line_1": request.form["address1"],#req
        "address_country_code": request.form["country"] ,#req, 
        "name_first": request.form["first_name"], 
        "name_last": request.form["last_name"],
        "address_line_2": request.form.get("address2", ""),
        "address_city": request.form.get("city", ""),
        "address_state": request.form.get("state", ""),
        "address_postal_code": request.form.get("zip", ""),
        "document_ssn": request.form.get("ssn", ""),
        "birth_date": request.form.get("dob", "")
    }
# Send POST request to Alloy
    response = requests.post(
        "https://sandbox.alloy.co/v1/evaluations",
        headers=HEADERS,
        json=data
    )
# Generate outcome. Display message based on outcome
    try:
        outcome = response.json().get("summary", {}).get("outcome", "Unknown")
    except Exception:
        return f"Error: {response.text}", 500
#Jessica Rabbit
    if outcome == "Approved":
        return "<h2>Success! Your account has been approved.</h2>"
#Jessica Review
    elif outcome == "Manual Review":
        return "<h2>Thanks for submitting your application, we’ll be in touch shortly.</h2>"
#Jessica Deny
    elif outcome == "Denied":
        return "<h2>Sorry, your application was not successful.</h2>"
    else:
        return f"<h2>Unexpected Outcome: {outcome}</h2>"

# Start the Flask server. The server listens for incoming requests and routes them to the appropriate functions based on the defined routes. I can access the form also at http://localhost:9000/ in my web browser.

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 9000))
    app.run(host="0.0.0.0", port=port, debug=True)