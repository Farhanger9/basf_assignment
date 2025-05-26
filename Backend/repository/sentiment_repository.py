import json
from sqlalchemy.sql import text


class SentimentRepository:
    def __init__(self, db_session):
        self.db = db_session

    def save_analysis(self, audio_file_path, analysis,feedback):
        insert_query = text("""
            INSERT INTO sentiment_analysis (
                feedback,
                audio_file_path,
                analysis
            ) VALUES (
                :feedback,
                :audio_path,
                :analysis
            )
        """)
        self.db.execute(insert_query, {
            "feedback": feedback,
            "audio_path": audio_file_path,
            "analysis": json.dumps(analysis)
        })
        self.db.commit()

    def get_analysis(self):
        select_query = text("SELECT * FROM sentiment_analysis ORDER BY created_at DESC")
        result = self.db.execute(select_query).mappings().all()
        return [dict(row) for row in result]