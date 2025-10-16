from flask import Flask, jsonify
from controllers import customer_controller

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Flask MVC (tanpa Blueprint) + MongoDB Atlas Bank API 🚀"})

# Rute
app.add_url_rule("/customers", view_func=customer_controller.index, methods=["GET"])
app.add_url_rule("/customers", view_func=customer_controller.store, methods=["POST"])
app.add_url_rule("/customers/<customer_id>", view_func=customer_controller.show, methods=["GET"])
app.add_url_rule("/customers/<customer_id>", view_func=customer_controller.update, methods=["PUT"])
app.add_url_rule("/customers/<customer_id>", view_func=customer_controller.destroy, methods=["DELETE"])

if __name__ == "__main__":
    app.run(debug=True)
