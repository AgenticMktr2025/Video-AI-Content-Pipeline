import reflex as rx
from app.states.recording_state import RecordingState


def confirmation_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.content(
            rx.radix.primitives.dialog.title("Upload Recording?"),
            rx.radix.primitives.dialog.description(
                "Would you like to upload the recorded video for processing?"
            ),
            rx.el.div(
                rx.radix.primitives.dialog.close(
                    rx.el.button(
                        "Discard",
                        on_click=RecordingState.reset_recording,
                        class_name="bg-gray-200 text-gray-800 px-4 py-2 rounded-md font-medium hover:bg-gray-300",
                    )
                ),
                rx.radix.primitives.dialog.close(
                    rx.el.button(
                        "Upload",
                        on_click=RecordingState.upload_recorded_video,
                        class_name="bg-blue-600 text-white px-4 py-2 rounded-md font-medium hover:bg-blue-700",
                    )
                ),
                class_name="flex justify-end gap-3 mt-4",
            ),
            class_name="bg-white p-6 rounded-lg shadow-lg",
        ),
        open=RecordingState.show_confirmation,
        on_open_change=RecordingState.set_show_confirmation,
    )


def record_video_page() -> rx.Component:
    return rx.el.div(
        confirmation_dialog(),
        rx.el.h1("Record Video", class_name="text-2xl font-bold mb-6"),
        rx.el.div(
            rx.cond(
                RecordingState.camera_ready,
                rx.el.div(
                    rx.el.video(
                        id="video-player",
                        class_name="rounded-lg bg-black border border-gray-200 w-full h-auto",
                        auto_play=True,
                        plays_inline=True,
                        muted=True,
                    ),
                    rx.el.div(
                        rx.cond(
                            RecordingState.is_recording,
                            rx.el.button(
                                rx.icon("circle_stop", class_name="mr-2 h-5 w-5"),
                                "Stop Recording",
                                on_click=rx.call_script(
                                    RecordingState.stop_recording_script
                                ),
                                class_name="flex items-center bg-red-600 text-white px-6 py-3 rounded-full text-lg font-semibold shadow-lg hover:bg-red-700",
                            ),
                            rx.el.button(
                                rx.icon("videotape", class_name="mr-2 h-5 w-5"),
                                "Start Recording",
                                on_click=rx.call_script(
                                    RecordingState.start_recording_script
                                ),
                                class_name="flex items-center bg-blue-600 text-white px-6 py-3 rounded-full text-lg font-semibold shadow-lg hover:bg-blue-700",
                            ),
                        ),
                        class_name="flex justify-center mt-6",
                    ),
                    class_name="w-full max-w-2xl mx-auto",
                ),
                rx.el.div(
                    rx.icon("video-off", class_name="h-12 w-12 text-gray-400"),
                    rx.el.p(
                        "Camera access is required to record video.",
                        class_name="text-gray-500 mt-2",
                    ),
                    rx.el.button(
                        "Enable Camera",
                        on_click=RecordingState.initialize_camera,
                        class_name="mt-4 bg-blue-600 text-white px-4 py-2 rounded-md font-medium hover:bg-blue-700",
                    ),
                    class_name="flex flex-col items-center justify-center p-8 border-2 border-dashed rounded-lg bg-gray-50",
                ),
            )
        ),
        on_mount=RecordingState.initialize_camera,
        class_name="max-w-4xl mx-auto",
    )