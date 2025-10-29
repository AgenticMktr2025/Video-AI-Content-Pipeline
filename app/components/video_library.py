import reflex as rx
from app.states.dashboard_state import DashboardState
from app.states.transcription_state import TranscriptionState


def video_card(filename: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("video", class_name="h-8 w-8 text-gray-500"),
            rx.el.span(filename, class_name="text-sm font-medium truncate"),
            class_name="flex items-center gap-4",
        ),
        rx.cond(
            TranscriptionState.is_transcribing[filename],
            rx.el.div(
                rx.spinner(size="3"),
                rx.el.span("Transcribing...", class_name="text-sm text-gray-500"),
                class_name="flex items-center gap-2",
            ),
            rx.el.button(
                "Transcribe",
                on_click=lambda: TranscriptionState.transcribe_video(filename),
                class_name="bg-blue-600 text-white px-3 py-1 rounded-md text-sm font-medium hover:bg-blue-700",
            ),
        ),
        rx.cond(
            TranscriptionState.transcripts.contains(filename),
            rx.el.div(
                rx.el.p("Transcript:", class_name="font-semibold text-sm mt-4 mb-2"),
                rx.el.div(
                    rx.el.p(
                        TranscriptionState.transcripts[filename],
                        class_name="text-xs text-gray-600",
                    ),
                    class_name="p-2 bg-gray-100 rounded-md max-h-32 overflow-y-auto",
                ),
                class_name="w-full mt-2",
            ),
        ),
        class_name="flex flex-col items-start justify-between p-4 border rounded-lg bg-white gap-4",
    )


def video_library_page() -> rx.Component:
    return rx.el.div(
        rx.el.h1("Video Library", class_name="text-2xl font-bold mb-6"),
        rx.cond(
            DashboardState.uploaded_files.length() == 0,
            rx.el.div(
                rx.icon("video_off", class_name="h-12 w-12 text-gray-400 mx-auto mb-4"),
                rx.el.p(
                    "No videos uploaded yet.", class_name="text-center text-gray-500"
                ),
                rx.el.a(
                    "Upload a video to get started.",
                    href="/",
                    class_name="text-blue-600 font-semibold mt-2 text-center block",
                ),
                class_name="flex flex-col items-center justify-center p-8 border-2 border-dashed rounded-lg",
            ),
            rx.el.div(
                rx.foreach(DashboardState.uploaded_files, video_card),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
            ),
        ),
        class_name="max-w-7xl mx-auto",
    )