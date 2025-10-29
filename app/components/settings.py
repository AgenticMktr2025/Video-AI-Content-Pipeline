import reflex as rx
from app.states.settings_state import SettingsState


def settings_input(
    label: str, placeholder: str, name: str, input_type: str = "text"
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="font-medium text-sm text-gray-700"),
        rx.el.input(
            name=name,
            placeholder=placeholder,
            type=input_type,
            class_name="w-full px-3 py-2 mt-1 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
        ),
        class_name="w-full",
    )


def settings_section(title: str, *children) -> rx.Component:
    return rx.el.div(
        rx.el.h2(title, class_name="text-lg font-semibold border-b pb-2 mb-4"),
        rx.el.div(*children, class_name="grid grid-cols-1 md:grid-cols-2 gap-6"),
        class_name="bg-white p-6 rounded-lg border",
    )


def settings_page() -> rx.Component:
    return rx.el.div(
        rx.el.h1("Settings", class_name="text-2xl font-bold mb-6"),
        rx.el.form(
            rx.el.div(
                settings_section(
                    "Cloud Storage (S3)",
                    settings_input(
                        "AWS Access Key ID",
                        "Enter your AWS Access Key ID",
                        "aws_access_key_id",
                    ),
                    settings_input(
                        "AWS Secret Access Key",
                        "Enter your AWS Secret Access Key",
                        "aws_secret_access_key",
                        input_type="password",
                    ),
                    settings_input(
                        "Default Region", "e.g., us-east-1", "aws_default_region"
                    ),
                    settings_input(
                        "S3 Bucket Name", "Enter your S3 bucket name", "s3_bucket_name"
                    ),
                ),
                settings_section(
                    "Social Media Integrations",
                    settings_input(
                        "LinkedIn Client ID",
                        "Enter your LinkedIn Client ID",
                        "linkedin_client_id",
                    ),
                    settings_input(
                        "LinkedIn Client Secret",
                        "Enter your LinkedIn Client Secret",
                        "linkedin_client_secret",
                        input_type="password",
                    ),
                    settings_input(
                        "X (Twitter) API Key", "Enter your X API Key", "twitter_api_key"
                    ),
                    settings_input(
                        "X (Twitter) API Secret",
                        "Enter your X API Secret",
                        "twitter_api_secret",
                        input_type="password",
                    ),
                ),
                rx.el.div(
                    rx.el.button(
                        "Save Settings",
                        type="submit",
                        class_name="bg-blue-600 text-white px-6 py-2 rounded-md font-medium hover:bg-blue-700",
                    ),
                    class_name="flex justify-end mt-6",
                ),
                class_name="flex flex-col gap-6",
            ),
            on_submit=SettingsState.handle_submit,
        ),
        class_name="max-w-4xl mx-auto",
    )