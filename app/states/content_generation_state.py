import reflex as rx
import openai
import os
import logging
import uuid
from typing import TypedDict
from app.states.transcription_state import TranscriptionState


class Draft(TypedDict):
    id: str
    video_filename: str
    title: str
    content: str
    status: str


class ContentGenerationState(rx.State):
    selected_video: str = ""
    is_generating: bool = False
    drafts: list[Draft] = []
    editor_is_open: bool = False
    active_draft_id: str = ""
    active_draft_content: str = ""
    active_draft_title: str = ""

    @rx.event
    async def generate_drafts(self):
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
                return
            client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
            prompt = f"Based on the following video transcript, generate 3 distinct pieces of long-form content (e.g., blog post, LinkedIn article, newsletter). For each piece, provide a title and the content in markdown format.\n\n            Transcript: '{transcript}'\n\n            Respond in the following format:\n\n            TITLE: [Title of the first content piece]\n            CONTENT:\n            [Markdown content of the first piece]\n            ---\n            TITLE: [Title of the second content piece]\n            CONTENT:\n            [Markdown content of the second piece]\n            ---\n            TITLE: [Title of the third content piece]\n            CONTENT:\n            [Markdown content of the third piece]\n            "
            response = await client.chat.completions.create_async(
                model="gpt-4", messages=[{"role": "user", "content": prompt}]
            )
            generated_content = response.choices[0].message.content
            content_pieces = generated_content.strip().split("---")
            for piece in content_pieces:
                if "TITLE:" in piece and "CONTENT:" in piece:
                    title_part, content_part = piece.split("CONTENT:", 1)
                    title = title_part.replace("TITLE:", "").strip()
                    content = content_part.strip()
                    new_draft = Draft(
                        id=str(uuid.uuid4()),
                        video_filename=self.selected_video,
                        title=title,
                        content=content,
                        status="draft",
                    )
                    self.drafts.append(new_draft)
        except Exception as e:
            logging.exception(f"Error generating drafts: {e}")
            yield rx.toast.error(f"Failed to generate drafts: {e}")
        finally:
            self.is_generating = False
            yield

    @rx.event
    def open_draft_editor(self, draft_id: str):
        for draft in self.drafts:
            if draft["id"] == draft_id:
                self.active_draft_id = draft_id
                self.active_draft_title = draft["title"]
                self.active_draft_content = draft["content"]
                self.editor_is_open = True
                return

    @rx.event
    def save_active_draft(self):
        for i, draft in enumerate(self.drafts):
            if draft["id"] == self.active_draft_id:
                self.drafts[i]["content"] = self.active_draft_content
                self.drafts[i]["status"] = "reviewed"
                break
        self.editor_is_open = False