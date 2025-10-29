import reflex as rx
import asyncio
import boto3
import logging
from app.states.settings_state import SettingsState
from app.states.base_state import BaseState


class DashboardState(BaseState):
    nav_items: list[dict[str, str]] = [
        {"label": "Upload Video", "icon": "upload-cloud", "href": "/"},
        {"label": "Record Video", "icon": "radio-tower", "href": "/record"},
        {"label": "Video Library", "icon": "video", "href": "/library"},
        {"label": "Content Drafts", "icon": "file-text", "href": "/drafts"},
        {"label": "Video Snippets", "icon": "scissors", "href": "/snippets"},
        {"label": "Analytics", "icon": "bar-chart-2", "href": "/analytics"},
        {"label": "Settings", "icon": "settings", "href": "/settings"},
    ]
    upload_progress: int = 0
    is_uploading: bool = False
    uploaded_files: list[str] = []

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        self.is_uploading = True
        self.upload_progress = 0
        yield
        settings = await self.get_state(SettingsState)
        s3_configured = (
            settings.aws_access_key_id
            and settings.aws_secret_access_key
            and settings.s3_bucket_name
        )
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.filename
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)
            if s3_configured:
                try:
                    s3 = boto3.client(
                        "s3",
                        aws_access_key_id=settings.aws_access_key_id,
                        aws_secret_access_key=settings.aws_secret_access_key,
                        region_name=settings.aws_default_region,
                    )
                    s3.upload_file(
                        outfile,
                        settings.s3_bucket_name,
                        f"videos/master/{file.filename}",
                    )
                    yield rx.toast.success(f"{file.filename} uploaded to S3.")
                except Exception as e:
                    logging.exception(f"S3 upload failed: {e}")
                    yield rx.toast.error(f"S3 upload failed for {file.filename}.")
            for i in range(101):
                self.upload_progress = i
                await asyncio.sleep(0.01)
                yield
            self.uploaded_files.append(file.filename)
        self.is_uploading = False
        yield