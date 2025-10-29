import reflex as rx
from app.states.snippet_generation_state import SnippetGenerationState
from app.states.dashboard_state import DashboardState


def snippet_card(snippet: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(snippet["title"], class_name="font-semibold"),
                rx.el.p(
                    f"{snippet['start']}s - {snippet['end']}s",
                    class_name="text-xs text-gray-500",
                ),
                class_name="flex flex-col",
            ),
            rx.el.span(
                snippet["status"],
                class_name=rx.cond(
                    snippet["status"] == "suggested",
                    "px-2 py-1 text-xs font-medium text-purple-800 bg-purple-100 rounded-full",
                    "px-2 py-1 text-xs font-medium text-green-800 bg-green-100 rounded-full",
                ),
            ),
            class_name="flex items-start justify-between",
        ),
        rx.el.p(snippet["hook"], class_name="text-sm text-gray-600 mt-2 italic"),
        rx.cond(
            snippet["status"] == "ready",
            rx.el.div(
                rx.video(
                    url=rx.get_upload_url(snippet["snippet_path"]),
                    width="100%",
                    height="auto",
                    playing=False,
                    controls=True,
                    class_name="rounded-lg mt-2",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("linkedin", class_name="h-4 w-4 mr-2"),
                        "Post to LinkedIn",
                        class_name="flex items-center bg-blue-600 text-white px-3 py-1 rounded-md text-sm font-medium hover:bg-blue-700",
                        on_click=lambda: rx.toast.info(
                            "LinkedIn integration not yet implemented."
                        ),
                    ),
                    rx.el.button(
                        rx.icon("twitter", class_name="h-4 w-4 mr-2"),
                        "Post to X",
                        class_name="flex items-center bg-black text-white px-3 py-1 rounded-md text-sm font-medium hover:bg-gray-800",
                        on_click=lambda: rx.toast.info(
                            "X/Twitter integration not yet implemented."
                        ),
                    ),
                    class_name="flex items-center gap-2 mt-2",
                ),
            ),
            rx.el.button(
                "Create Snippet",
                is_loading=SnippetGenerationState.is_cutting[snippet["id"]],
                on_click=lambda: SnippetGenerationState.cut_snippet(snippet["id"]),
                class_name="mt-4 w-full bg-green-600 text-white px-3 py-1 rounded-md text-sm font-medium hover:bg-green-700 disabled:bg-gray-400",
            ),
        ),
        class_name="bg-white p-4 border rounded-lg flex flex-col gap-2",
    )


def video_snippets_page() -> rx.Component:
    return rx.el.div(
        rx.el.h1("Video Snippets", class_name="text-2xl font-bold mb-6"),
        rx.el.div(
            rx.el.select(
                rx.foreach(
                    DashboardState.uploaded_files, lambda f: rx.el.option(f, value=f)
                ),
                placeholder="Select a video to generate snippets...",
                on_change=SnippetGenerationState.set_selected_video,
                class_name="w-full md:w-1/3 p-2 border rounded-md",
            ),
            rx.el.button(
                "Generate Snippets",
                on_click=SnippetGenerationState.generate_snippets,
                is_loading=SnippetGenerationState.is_generating,
                class_name="bg-blue-600 text-white px-4 py-2 rounded-md font-medium hover:bg-blue-700 disabled:bg-gray-400",
                disabled=SnippetGenerationState.selected_video == "",
            ),
            class_name="flex items-center gap-4 mb-6",
        ),
        rx.cond(
            SnippetGenerationState.snippets.length() == 0,
            rx.el.div(
                rx.icon("scissors", class_name="h-12 w-12 text-gray-400 mx-auto mb-4"),
                rx.el.p(
                    "No snippets generated yet. Select a video and click 'Generate Snippets'.",
                    class_name="text-center text-gray-500",
                ),
                class_name="flex flex-col items-center justify-center p-8 border-2 border-dashed rounded-lg mt-8",
            ),
            rx.el.div(
                rx.foreach(SnippetGenerationState.snippets, snippet_card),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
            ),
        ),
        class_name="max-w-7xl mx-auto",
    )