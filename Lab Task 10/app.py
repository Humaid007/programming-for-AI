from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def get_bot_response(user_input):
    user_input = user_input.lower().replace("-", " ").strip()

    if "room" in user_input or "price" in user_input:
        return "Our standard room starts at $99. Deluxe rooms are $149 with ocean view."
    elif "wifi" in user_input or "internet" in user_input:
        return "Yes, high-speed Wi-Fi is free throughout the property."
    elif "location" in user_input or "address" in user_input or "where" in user_input:
        return "We are located at 123 Sunshine Avenue, Miami, FL."
    elif "check in" in user_input or "check out" in user_input:
        return "Check-in is from 3 PM and check-out is at 11 AM."
    elif "restaurant" in user_input or "dining" in user_input or "food" in user_input:
        return "We have 3 restaurants serving Italian, Indian, and Continental cuisines."
    elif "spa" in user_input or "pool" in user_input or "gym" in user_input or "amenities" in user_input:
        return "Yes, we have a spa, gym, and an outdoor swimming pool open 7 AM to 10 PM."
    elif "book" in user_input or "reservation" in user_input:
        return "You can book a room on our website or by calling +1-234-567-890."
    else:
        return "Sorry, I didn’t get that. Try asking about rooms, location, spa, etc."


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["GET"])
def get_response():
    user_msg = request.args.get("msg")
    response = get_bot_response(user_msg)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
