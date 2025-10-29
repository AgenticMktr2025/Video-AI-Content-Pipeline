import reflex as rx
import openai
import os
import logging
import uuid
import json
import subprocess
from typing import TypedDict
from app.states.transcription_state import TranscriptionState


class Snippet(TypedDict):
    id: str
    video_filename: str
    title: str
    hook: str
    start: float
    end: float
    status: str
    snippet_path: str


class SnippetGenerationState(rx.State):
    selected_video: str = ""
    is_generating: bool = False
    snippets: list[Snippet] = []
    is_cutting: dict[str, bool] = {}

    @rx.event
    async def generate_snippets(self):
        if not self.selected_video:
            yield rx.toast.error("Please select a video first.")
            return
        self.is_generating = True
        yield
        try:
            transcription_state = await self.get_state(TranscriptionState)
            transcript = transcription_state.transcripts.get(self.selected_video)
            if (
                not transcript
                or transcript.startswith("Error")
                or transcript.startswith("Transcription in progress")
            ):
                yield rx.toast.error("Transcription not available or failed.")
                self.is_generating = False
                return
            client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
            prompt = f"""Analyze the following video transcript to identify 3-5 snippet-worthy moments, each between 15 and 60 seconds. For each moment, provide a short, catchy title, a hook caption, and the precise start and end timestamps. Respond with ONLY a valid JSON array of objects.\n\nTranscript: '{transcript}'\n\nJSON format:\n[\n  {{\n    "title": "Snippet Title",\n    "hook": "Catchy hook for social media.",\n    "start": 0.0,\n    "end": 0.0\n  }}\n]\n"""
            response = await client.chat.completions.create_async(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
            )
            generated_content = response.choices[0].message.content
            snippet_suggestions = json.loads(generated_content)
            if isinstance(snippet_suggestions, dict):
                key = list(snippet_suggestions.keys())[0]
                snippet_suggestions = snippet_suggestions[key]
            for suggestion in snippet_suggestions:
                new_snippet = Snippet(
                    id=str(uuid.uuid4()),
                    video_filename=self.selected_video,
                    title=suggestion["title"],
                    hook=suggestion["hook"],
                    start=suggestion["start"],
                    end=suggestion["end"],
                    status="suggested",
                    snippet_path="",
                )
                self.snippets.append(new_snippet)
        except Exception as e:
            logging.exception(f"Error generating snippets: {e}")
            yield rx.toast.error(f"Failed to generate snippets: {e}")
        finally:
            self.is_generating = False
            yield

    @rx.event(background=True)
    async def cut_snippet(self, snippet_id: str):
        async with self:
            self.is_cutting[snippet_id] = True
        snippet_to_cut = None
        for s in self.snippets:
            if s["id"] == snippet_id:
                snippet_to_cut = s
                break
        if not snippet_to_cut:
            async with self:
                self.is_cutting[snippet_id] = False
            return
        try:
            master_video_path = rx.get_upload_dir() / snippet_to_cut["video_filename"]
            output_filename = f"snippet_{snippet_id}.mp4"
            output_path = rx.get_upload_dir() / output_filename
            command = [
                "ffmpeg",
                "-i",
                str(master_video_path),
                "-ss",
                str(snippet_to_cut["start"]),
                "-to",
                str(snippet_to_cut["end"]),
                "-c",
                "copy",
                str(output_path),
            ]
            process = subprocess.run(command, capture_output=True, text=True)
            if process.returncode != 0:
                raise Exception(f"ffmpeg error: {process.stderr}")
            async with self:
                for i, s in enumerate(self.snippets):
                    if s["id"] == snippet_id:
                        self.snippets[i]["status"] = "ready"
                        self.snippets[i]["snippet_path"] = output_filename
                        break
                self.is_cutting.pop(snippet_id, None)
        except Exception as e:
            logging.exception(f"Error cutting snippet: {e}")
            async with self:
                self.is_cutting[snippet_id] = False