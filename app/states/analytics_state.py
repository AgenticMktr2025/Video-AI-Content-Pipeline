import reflex as rx
from typing import TypedDict


class MonthlyStat(TypedDict):
    month: str
    videos: int
    drafts: int
    snippets: int


class AnalyticsState(rx.State):
    monthly_data: list[MonthlyStat] = [
        {"month": "Jan", "videos": 4, "drafts": 12, "snippets": 20},
        {"month": "Feb", "videos": 6, "drafts": 18, "snippets": 30},
        {"month": "Mar", "videos": 5, "drafts": 15, "snippets": 25},
        {"month": "Apr", "videos": 8, "drafts": 24, "snippets": 40},
        {"month": "May", "videos": 7, "drafts": 21, "snippets": 35},
        {"month": "Jun", "videos": 10, "drafts": 30, "snippets": 50},
    ]

    @rx.var
    def total_videos(self) -> int:
        return sum((d["videos"] for d in self.monthly_data))

    @rx.var
    def total_drafts(self) -> int:
        return sum((d["drafts"] for d in self.monthly_data))

    @rx.var
    def total_snippets(self) -> int:
        return sum((d["snippets"] for d in self.monthly_data))