import reflex as rx
from app.states.analytics_state import AnalyticsState


def stat_card(icon: str, title: str, value: rx.Var[int]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-6 w-6 text-gray-500"),
            class_name="p-3 bg-gray-100 rounded-lg",
        ),
        rx.el.div(
            rx.el.p(title, class_name="text-sm font-medium text-gray-600"),
            rx.el.p(value, class_name="text-2xl font-bold"),
        ),
        class_name="flex items-center gap-4 p-4 bg-white border rounded-lg",
    )


def legend_item(color: str, name: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(class_name=f"w-3 h-3 rounded-full", background_color=color),
        rx.el.span(name, class_name="text-sm text-gray-600"),
        class_name="flex items-center gap-2",
    )


def analytics_page() -> rx.Component:
    return rx.el.div(
        rx.el.h1("Analytics Dashboard", class_name="text-2xl font-bold mb-6"),
        rx.el.div(
            stat_card("video", "Total Videos Uploaded", AnalyticsState.total_videos),
            stat_card("file-text", "Total Content Drafts", AnalyticsState.total_drafts),
            stat_card(
                "scissors", "Total Snippets Created", AnalyticsState.total_snippets
            ),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8",
        ),
        rx.el.div(
            rx.el.h2(
                "Content Generation Over Time", class_name="text-lg font-semibold mb-4"
            ),
            rx.el.div(
                legend_item("#8884d8", "Videos"),
                legend_item("#82ca9d", "Drafts"),
                legend_item("#ffc658", "Snippets"),
                class_name="flex justify-center gap-4 mb-4",
            ),
            rx.recharts.line_chart(
                rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
                rx.recharts.x_axis(data_key="month"),
                rx.recharts.y_axis(),
                rx.recharts.tooltip(),
                rx.recharts.line(
                    data_key="videos", stroke="#8884d8", name="Videos", type_="monotone"
                ),
                rx.recharts.line(
                    data_key="drafts", stroke="#82ca9d", name="Drafts", type_="monotone"
                ),
                rx.recharts.line(
                    data_key="snippets",
                    stroke="#ffc658",
                    name="Snippets",
                    type_="monotone",
                ),
                data=AnalyticsState.monthly_data,
                height=300,
            ),
            class_name="p-6 bg-white border rounded-lg",
        ),
        class_name="max-w-7xl mx-auto",
    )