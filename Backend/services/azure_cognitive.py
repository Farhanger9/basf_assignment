import os
import uuid

from flask import jsonify
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech.audio import AudioOutputConfig


class AzureCognitiveService:
    def __init__(self, api_key, endpoint, speech_key, speech_region):
        self.api_key = api_key
        self.endpoint = endpoint
        self.speech_key = speech_key
        self.speech_region = speech_region

    def text_analysis(self, text):
        try:
            credential = AzureKeyCredential(self.api_key)
            client = TextAnalyticsClient(self.endpoint, credential)
            response = client.analyze_sentiment(documents=[text])
            response_data = []

            for doc in response:
                result = {
                    "sentiment": doc.sentiment,
                    "confidence_scores": {
                        "positive": doc.confidence_scores.positive,
                        "neutral": doc.confidence_scores.neutral,
                        "negative": doc.confidence_scores.negative
                    }
                }
                response_data.append(result)

            audio_path= self.synthesize_speech_with_emotion(text, doc.sentiment)
            combined_result = {
                "text": text,
                "analysis": response_data,
                "audio_file_path": audio_path
            }

            return combined_result

        except Exception as e:
            return  e

    def synthesize_speech_with_emotion(self, text, sentiment):
        speech_config = speechsdk.SpeechConfig(
            subscription=self.speech_key,
            region=self.speech_region
        )
        speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"

        # Adjust pitch and rate based on sentiment
        if sentiment == "positive":
            prosody = '<prosody rate="+10%" pitch="+5%">'
        elif sentiment == "negative":
            prosody = '<prosody rate="-10%" pitch="-5%">'
        else:
            prosody = '<prosody rate="0%" pitch="0%">'

        ssml = f"""
        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
            <voice name='en-US-JennyNeural'>
                {prosody}
                    {text}
                </prosody>
            </voice>
        </speak>
        """

        # ✅ Save to file
        output_folder = "output_audio"
        os.makedirs(output_folder, exist_ok=True)
        filename = f"{uuid.uuid4().hex}.mp3"
        output_path = os.path.join(output_folder, filename)

        audio_config = AudioOutputConfig(filename=output_path)
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        result = synthesizer.speak_ssml_async(ssml).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print(f"Speech synthesized and saved to {output_path}")
            return output_path
        else:
            print("Speech synthesis failed:", result.reason)
            return None
