from flask import Flask, request, jsonify
import time
from openai_client import get_openai_client
import os

def setup_routes(app):
    """Define Flask routes."""
    client = get_openai_client()
    FILE_ID = os.getenv("FILE_ID")
    ASSISTANT_ID = os.getenv("ASSISTANT_ID")

    @app.route('/start-session', methods=['POST'])
    def start_session():
        """Creates a new thread for the user session."""
        thread = client.beta.threads.create()
        return jsonify({"message": "New session started.", "thread_id": thread.id})

    @app.route('/ask-question', methods=['POST'])
    def ask_question():
        """Processes user query against the uploaded file using OpenAI's File Search."""
        data = request.json
        thread_id = data.get("thread_id")
        question = data.get("question")

        if not thread_id or not question:
            return jsonify({"error": "Missing thread_id or question"}), 400

        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=question,
            attachments=[
                {"file_id": FILE_ID, "tools": [{"type": "file_search"}]}
            ]
        )

        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=ASSISTANT_ID
        )

        while True:
            run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            if run_status.status in ["completed", "failed"]:
                break
            time.sleep(2)

        if run_status.status == "failed":
            return jsonify({"error": "Assistant failed to process request."}), 500

        messages = client.beta.threads.messages.list(thread_id=thread_id)

        assistant_response = next((message.content[0].text.value for message in messages.data if message.role == "assistant"), None)
        
        if assistant_response:
            return jsonify({"response": assistant_response})

        return jsonify({"error": "No response received"}), 500