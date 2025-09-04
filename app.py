import newrelic.agent
newrelic.agent.initialize()

from newrelic.agent import (background_task, function_trace)
import os
import time
from flask import Flask, request, make_response
from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route("/health", methods=["GET"])
@newrelic.agent.background_task(name='health_check')
def health_check():
    return make_response("OK", 200)

@app.route("/close-old", methods=["POST"])
@newrelic.agent.background_task(name='close_old_channels')
def close_old_channels():    
    client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
    verifier = SignatureVerifier(signing_secret=os.getenv("SLACK_SIGNING_SECRET"))

    if not verifier.is_valid_request(request.get_data(), request.headers):
        return make_response("Invalid signature", 403)

    user_id = request.form.get("user_id")
    command_text = request.form.get("text", "").strip().lower()
    dry_run = " --dry-run" in command_text

    now = time.time()
    one_year_ago = now - 365 * 24 * 60 * 60
    closed_channels = []

    channels = client.conversations_list(types="public_channel,private_channel").data["channels"]

    for channel in channels:
        history = client.conversations_history(channel=channel["id"], limit=100).data["messages"]

        inactive = [
            msg for msg in history
            if float(msg["ts"]) < one_year_ago and msg.get("user") != user_id
        ]

        if inactive:
            if not dry_run:
                client.chat_postMessage(
                    channel=channel["id"],
                    text="Closing this thread due to inactivity."
                )
            closed_channels.append(channel["name"])

    if dry_run:
        response_text = f"🧪 Dry-run complete. {len(closed_channels)} channels would be closed: {', '.join(closed_channels)}"
    else:
        response_text = f"✅ Closed {len(closed_channels)} channels: {', '.join(closed_channels)}"

    return make_response(response_text, 200)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 3010)))