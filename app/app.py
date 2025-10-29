import reflex as rx
from app.states.dashboard_state import DashboardState
from app.components.sidebar import sidebar
from app.components.video_upload import video_upload_page
from app.components.video_library import video_library_page
from app.components.content_drafts import content_drafts_page
from app.components.video_snippets import video_snippets_page
from app.components.analytics import analytics_page
from app.components.settings import settings_page
from app.components.record_video import record_video_page


def index() -> rx.Component:
    return page_with_sidebar(video_upload_page())


def library() -> rx.Component:
    return page_with_sidebar(video_library_page())


def drafts() -> rx.Component:
    return page_with_sidebar(content_drafts_page())


def snippets() -> rx.Component:
    return page_with_sidebar(video_snippets_page())


def analytics() -> rx.Component:
    return page_with_sidebar(analytics_page())


def settings() -> rx.Component:
    return page_with_sidebar(settings_page())


def record() -> rx.Component:
    return page_with_sidebar(record_video_page())


def page_with_sidebar(content: rx.Component) -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(content, class_name="flex-1 p-6 bg-gray-50 min-h-screen"),
        class_name="flex min-h-screen w-screen bg-white font-['Inter']",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index)
app.add_page(library)
app.add_page(drafts)
app.add_page(snippets)
app.add_page(analytics)
app.add_page(settings)
app.add_page(record)