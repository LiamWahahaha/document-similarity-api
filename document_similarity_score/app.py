from flask import Flask, request, jsonify
from flask_api import status


app = Flask(__name__)

from .document_similarity_score import (
    Context,
    ConcreteStrategyJaccardIndex,
    ConcreteStrategyWordVector,
)


@app.route("/")
def hello():
    return "Flask application is up and running"


@app.route("/similarity-score", methods=["POST"])
def similarity_score():
    payload = request.get_json(force=True)
    try:
        document1 = payload["document1"]
        document2 = payload["document2"]
        strategy = payload["strategy"]
        context = Context(ConcreteStrategyWordVector())

        if strategy == 'JaccardIndex':
            context.strategy = ConcreteStrategyJaccardIndex()

        score = context.calculate_document_similarity_score(document1, document2)
        return jsonify({"similarity_score": score}), status.HTTP_200_OK
    except KeyError:
        return (
            jsonify({"error": "paramenters: document1, document2"}),
            status.HTTP_400_BAD_REQUEST,
        )
