from flask import Flask, request, jsonify, render_template
from app.rag.pipeline import RAGPipeline


app = Flask(__name__)
pipeline = RAGPipeline()

@app.route("/api/query", methods=["POST"])
def query():
    data = request.get_json() or {}
    q = data.get("query", "").strip()
    if not q:
        return jsonify({"error": "Query required"}), 400
        
    try:
        result = pipeline.run(q)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"})
