from flask import Flask
from services.azure_cognitive import AzureCognitiveService
from routes.azure_routes import azure_bp
from dotenv import load_dotenv
from flask_cors import CORS

import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Read envs and inject service
    api_key = os.getenv("AZURE_API_KEY")
    endpoint = os.getenv("AZURE_ENDPOINT")
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    speech_region = os.getenv("AZURE_SPEECH_REGION")
    print(api_key)
    azure_service = AzureCognitiveService(api_key=api_key, endpoint=endpoint,speech_key=speech_key,speech_region=speech_region)
    app.config['azure_service'] = azure_service

    app.register_blueprint(azure_bp)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
