import reflex as rx
from app.states.dashboard_state import DashboardState


def uploaded_video_card(filename: str) -> rx.Component:
    return rx.el.div(
        rx.icon("video", class_name="h-6 w-6 text-gray-500"),
        rx.el.span(filename, class_name="text-sm font-medium truncate"),
        class_name="flex items-center gap-4 p-4 border rounded-lg bg-white",
    )


def video_upload_page() -> rx.Component:
    return rx.el.div(
        rx.el.h1("Upload Video", class_name="text-2xl font-bold mb-6"),
        rx.upload.root(
            rx.el.div(
                rx.icon(
                    "cloud_upload", class_name="h-12 w-12 text-gray-400 mx-auto mb-4"
                ),
                rx.el.p(
                    "Drag and drop your video here or ",
                    rx.el.span(
                        "click to browse", class_name="font-semibold text-blue-600"
                    ),
                    class_name="text-center text-gray-500",
                ),
                class_name="flex flex-col items-center justify-center p-8",
            ),
            id="video_upload",
            border="2px dashed #d1d5db",
            padding="1rem",
            border_radius="0.5rem",
            width="100%",
            on_drop=DashboardState.handle_upload(
                rx.upload_files(upload_id="video_upload")
            ),
        ),
        rx.cond(
            DashboardState.is_uploading,
            rx.el.div(
                rx.el.p("Uploading...", class_name="text-sm font-medium mb-2"),
                rx.el.div(
                    rx.el.div(
                        class_name="bg-blue-600 h-2.5 rounded-full",
                        style={
                            "width": DashboardState.upload_progress.to_string() + "%"
                        },
                    ),
                    class_name="w-full bg-gray-200 rounded-full h-2.5",
                ),
                class_name="mt-4",
            ),
        ),
        rx.cond(
            DashboardState.uploaded_files.length() > 0,
            rx.el.div(
                rx.el.h2(
                    "Uploaded Files", class_name="text-xl font-semibold mt-8 mb-4"
                ),
                rx.el.div(
                    rx.foreach(DashboardState.uploaded_files, uploaded_video_card),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4",
                ),
            ),
        ),
        class_name="max-w-4xl mx-auto",
    )