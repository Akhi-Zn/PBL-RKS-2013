from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

# API Keys & config
ABSTRACT_API_KEY = "5fdede75753445958ca91af1fc739b2a"
EMAILJS_SERVICE_ID = "service_yut6khr"
EMAILJS_TEMPLATE_ID = "template_4t9vgjn"
EMAILJS_USER_ID = "wKX0FoQ2qKvI7dUXL"

# Cek validitas email dari Abstract API
def check_email_abstract(email):
    url = f"https://emailvalidation.abstractapi.com/v1/?api_key={ABSTRACT_API_KEY}&email={email}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "deliverability": data.get("deliverability"),
            "is_valid_format": data.get("is_valid_format", {}).get("value"),
            "is_disposable": data.get("is_disposable_email", {}).get("value"),
            "is_mx_found": data.get("is_mx_found", {}).get("value"),
            "email": email
        }
    else:
        return {"error": "API Error"}

# Kirim hasil ke email menggunakan EmailJS
def send_emailjs(to_email, content):
    url = "https://api.emailjs.com/api/v1.0/email/send"
    headers = {"Content-Type": "application/json"}
    payload = {
        "service_id": "service_yut6khr",
        "template_id": "template_4t9vgjn",
        "user_id": "wKX0FoQ2qKvI7dUXL",
        "template_params": {
            "user_email": to_email,
            "result_info": content
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.status_code == 200

# Halaman utama
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        email = request.form["email"]
        result = check_email_abstract(email)
        if "error" not in result:
            result_text = (
                f"Deliverability: {result['deliverability']}\n"
                f"Valid Format: {result['is_valid_format']}\n"
                f"Disposable: {result['is_disposable']}\n"
                f"MX Record Found: {result['is_mx_found']}"
            )
            send_emailjs(email, result_text)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
