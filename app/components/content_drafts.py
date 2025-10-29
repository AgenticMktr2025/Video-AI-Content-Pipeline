import reflex as rx
from reflex_monaco import monaco
from app.states.content_generation_state import ContentGenerationState
from app.states.dashboard_state import DashboardState


def draft_editor_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(
            rx.el.button("Open Editor", class_name="invisible", id="open-editor-button")
        ),
        rx.radix.primitives.dialog.content(
            rx.radix.primitives.dialog.title(ContentGenerationState.active_draft_title),
            monaco(
                value=ContentGenerationState.active_draft_content,
                language="markdown",
                height="50vh",
                theme="vs-dark",
                on_change=ContentGenerationState.set_active_draft_content,
            ),
            rx.el.div(
                rx.radix.primitives.dialog.close(
                    rx.el.button(
                        "Save and Close",
                        on_click=ContentGenerationState.save_active_draft,
                        class_name="bg-blue-600 text-white px-4 py-2 rounded-md font-medium hover:bg-blue-700",
                    )
                ),
                class_name="flex justify-end mt-4",
            ),
            class_name="bg-white p-6 rounded-lg shadow-lg w-full max-w-4xl",
            style={"background_color": "white"},
        ),
        open=ContentGenerationState.editor_is_open,
        on_open_change=ContentGenerationState.set_editor_is_open,
    )


def draft_card(draft: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("file-text", class_name="h-6 w-6 text-gray-500"),
                rx.el.h3(draft["title"], class_name="font-semibold"),
            ),
            rx.el.span(
                draft["status"],
                class_name=rx.cond(
                    draft["status"] == "draft",
                    "px-2 py-1 text-xs font-medium text-yellow-800 bg-yellow-100 rounded-full",
                    "px-2 py-1 text-xs font-medium text-green-800 bg-green-100 rounded-full",
                ),
            ),
            class_name="flex items-center justify-between",
        ),
        rx.el.p(
            draft["content"].to_string()[:150] + "...",
            class_name="text-sm text-gray-600 mt-2",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("disc_3", class_name="h-4 w-4 mr-2"),
                "Edit",
                on_click=lambda: ContentGenerationState.open_draft_editor(draft["id"]),
                class_name="flex items-center bg-gray-200 text-gray-800 px-3 py-1 rounded-md text-sm font-medium hover:bg-gray-300",
            ),
            rx.el.button(
                rx.icon("copy", class_name="h-4 w-4 mr-2"),
                "Copy",
                on_click=rx.set_clipboard(draft["content"]),
                class_name="flex items-center bg-blue-100 text-blue-800 px-3 py-1 rounded-md text-sm font-medium hover:bg-blue-200",
            ),
            rx.el.button(
                rx.icon("send", class_name="h-4 w-4 mr-2"),
                "Send to Ghostwriter",
                on_click=lambda: rx.toast.info(
                    "Ghostwriter integration not yet implemented."
                ),
                class_name="flex items-center bg-purple-100 text-purple-800 px-3 py-1 rounded-md text-sm font-medium hover:bg-purple-200",
            ),
            class_name="flex items-center gap-2 mt-4",
            flex_wrap="wrap",
        ),
        class_name="bg-white p-4 border rounded-lg flex flex-col gap-2",
    )


def content_drafts_page() -> rx.Component:
    return rx.el.div(
        draft_editor_modal(),
        rx.el.h1("Content Drafts", class_name="text-2xl font-bold mb-6"),
        rx.el.div(
            rx.el.select(
                rx.foreach(
                    DashboardState.uploaded_files, lambda f: rx.el.option(f, value=f)
                ),
                placeholder="Select a video to generate content...",
                on_change=ContentGenerationState.set_selected_video,
                class_name="w-full md:w-1/3 p-2 border rounded-md",
            ),
            rx.el.button(
                "Generate Drafts",
                on_click=ContentGenerationState.generate_drafts,
                is_loading=ContentGenerationState.is_generating,
                class_name="bg-blue-600 text-white px-4 py-2 rounded-md font-medium hover:bg-blue-700 disabled:bg-gray-400",
                disabled=ContentGenerationState.selected_video == "",
            ),
            class_name="flex items-center gap-4 mb-6",
        ),
        rx.cond(
            ContentGenerationState.drafts.length() == 0,
            rx.el.div(
                rx.icon(
                    "file-plus-2", class_name="h-12 w-12 text-gray-400 mx-auto mb-4"
                ),
                rx.el.p(
                    "No content drafts generated yet. Select a video and click 'Generate Drafts'.",
                    class_name="text-center text-gray-500",
                ),
                class_name="flex flex-col items-center justify-center p-8 border-2 border-dashed rounded-lg mt-8",
            ),
            rx.el.div(
                rx.foreach(ContentGenerationState.drafts, draft_card),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
            ),
        ),
        class_name="max-w-7xl mx-auto",
    )