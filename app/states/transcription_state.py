import reflex as rx
import openai
import os
import logging


class TranscriptionState(rx.State):
    is_transcribing: dict[str, bool] = {}
    transcripts: dict[str, str] = {}

    @rx.event(background=True)
    async def transcribe_video(self, filename: str):
        async with self:
            self.is_transcribing[filename] = True
            self.transcripts[filename] = "Transcription in progress..."
        try:
            client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
            video_path = rx.get_upload_dir() / filename
            with open(video_path, "rb") as audio_file:
                transcript = await client.audio.transcriptions.create_async(
                    model="whisper-1", file=audio_file, response_format="text"
                )
            async with self:
                self.transcripts[filename] = transcript
                self.is_transcribing[filename] = False
        except Exception as e:
            logging.exception(f"Error transcribing video: {e}")
            async with self:
                self.transcripts[filename] = f"Error: {e}"
                self.is_transcribing[filename] = False