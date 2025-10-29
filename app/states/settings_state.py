import reflex as rx


class SettingsState(rx.State):
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_default_region: str = "us-east-1"
    s3_bucket_name: str = ""
    linkedin_client_id: str = ""
    linkedin_client_secret: str = ""
    twitter_api_key: str = ""
    twitter_api_secret: str = ""

    @rx.event
    def handle_submit(self, form_data: dict):
        """Handle the form submit."""
        self.aws_access_key_id = form_data.get("aws_access_key_id", "")
        self.aws_secret_access_key = form_data.get("aws_secret_access_key", "")
        self.aws_default_region = form_data.get("aws_default_region", "us-east-1")
        self.s3_bucket_name = form_data.get("s3_bucket_name", "")
        self.linkedin_client_id = form_data.get("linkedin_client_id", "")
        self.linkedin_client_secret = form_data.get("linkedin_client_secret", "")
        self.twitter_api_key = form_data.get("twitter_api_key", "")
        self.twitter_api_secret = form_data.get("twitter_api_secret", "")
        return rx.toast.success("Settings saved successfully!")