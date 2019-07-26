from flask import Flask
app = Flask("Nutrition Mate")

@app.route("/")
def hello():
    return "This will be Nutrition Mate!"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
