import reflex as rx
from app.states.dashboard_state import DashboardState


def nav_item(item: dict) -> rx.Component:
    return rx.el.a(
        rx.icon(item["icon"], class_name="h-5 w-5"),
        rx.el.span(item["label"]),
        href=item.get("href", "#"),
        class_name=rx.cond(
            DashboardState.router.page.path == item["href"],
            "flex items-center gap-3 rounded-lg bg-gray-100 px-3 py-2 text-gray-900 transition-all hover:text-gray-900",
            "flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900",
        ),
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("videotape", class_name="h-6 w-6 text-blue-600"),
                rx.el.span("Own Your Voice", class_name="text-lg font-semibold"),
                class_name="flex h-16 items-center gap-2 border-b px-6",
            ),
            rx.el.nav(
                rx.foreach(DashboardState.nav_items, nav_item),
                class_name="flex flex-col gap-1 p-4 text-sm font-medium",
            ),
            class_name="flex-1 overflow-auto",
        ),
        class_name="flex flex-col border-r bg-white h-screen w-64 shrink-0",
    )