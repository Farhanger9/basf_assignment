import os

from flask import Blueprint, request, jsonify, current_app, send_from_directory
from db import SessionLocal
from repository.sentiment_repository import SentimentRepository
from services.open_ai_service import OpenAIService

azure_bp = Blueprint('azure_bp', __name__)

@azure_bp.route('/output_audio/<filename>')
def serve_audio(filename):
    return send_from_directory(
        directory=os.path.join(os.getcwd(), 'output_audio'),
        path=filename,
        as_attachment=True
    )
@azure_bp.route('/feedback', methods=['GET'])
def feedback():
    try:
        database = SessionLocal()
        repository = SentimentRepository(database)
        data=repository.get_analysis()
        return jsonify(data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify({'error': str(e)})
    finally:
        database.close()


@azure_bp.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        text = data['content']

        azure_service = current_app.config['azure_service']
        result = azure_service.text_analysis(text)

        db = SessionLocal()
        repo = SentimentRepository(db)
        repo.save_analysis(audio_file_path=result["audio_file_path"], analysis=result["analysis"],feedback=text)

        openai_service = OpenAIService(api_key=os.getenv("OPENAI_API_KEY"))
        sentiment = result["analysis"][0]["sentiment"]
        openai_response = openai_service.generate_response(text, sentiment)
        return jsonify({
            "status": "ok",
            "response_to_user": openai_response
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
