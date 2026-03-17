# infrastructure/charts/mood_chart_generator.py
import asyncio
import logging
from io import BytesIO
from datetime import datetime, date
from typing import Optional, TypedDict

import matplotlib
from infrastructure.concurrency import executor_pool

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle

from application.services.chart_generator import (
    ChartGeneratorInterface,
    ChartData,
    ChartType,
    ChartTheme,
)

logger = logging.getLogger(__name__)


class ThemeColors(TypedDict):
    bg: str
    fg: str
    grid: str
    line: str
    fill: str
    text: str
    mood_colors: list[str]


class MoodChartGenerator(ChartGeneratorInterface):
    def __init__(self) -> None:
        self._executor = executor_pool.get_executor("chart_generator", max_workers=4)

    THEMES: dict[ChartTheme, ThemeColors] = {
        "light": {
            "bg": "#ffffff",
            "fg": "#1a1a2e",
            "grid": "#e0e0e0",
            "line": "#4361ee",
            "fill": "#4361ee33",
            "text": "#1a1a2e",
            "mood_colors": ["#ef476f", "#ffd166", "#06d6a0", "#118ab2", "#073b4c"],
        },
        "dark": {
            "bg": "#1a1a2e",
            "fg": "#ffffff",
            "grid": "#3a3a5a",
            "line": "#4cc9f0",
            "fill": "#4cc9f033",
            "text": "#ffffff",
            "mood_colors": ["#f72585", "#f8961e", "#f9c74f", "#43aa8b", "#4d908e"],
        },
    }

    async def generate(
        self,
        data: ChartData,
        chart_type: ChartType = "line",
        theme: ChartTheme = "light",
        include_stats: bool = True,
        user_id: Optional[int] = None,
        width: int = 1200,
        height: int = 800,
        dpi: int = 100,
    ) -> BytesIO:
        loop = asyncio.get_running_loop()

        return await loop.run_in_executor(
            self._executor,
            self._generate_sync,
            data,
            chart_type,
            theme,
            include_stats,
            user_id,
            width,
            height,
            dpi,
        )

    def _generate_sync(
        self,
        data: ChartData,
        chart_type: str,
        theme: ChartTheme,
        include_stats: bool,
        user_id: Optional[int],
        width: int,
        height: int,
        dpi: int,
    ) -> BytesIO:
        theme_colors: ThemeColors = self.THEMES[theme]

        fig, ax = plt.subplots(
            figsize=(width / dpi, height / dpi), dpi=dpi, facecolor=theme_colors["bg"]
        )
        ax.set_facecolor(theme_colors["bg"])
        ax.tick_params(colors=theme_colors["fg"])
        for spine in ax.spines.values():
            spine.set_color(theme_colors["grid"])

        dates: list[date] = data["dates"]
        values: list[int] = data["values"]
        stats: dict = data["stats"]
        period_days: int = data["period_days"]

        if chart_type == "line":
            self._draw_line_chart_sync(ax, dates, values, theme_colors)
        elif chart_type == "bar":
            self._draw_bar_chart_sync(ax, dates, values, theme_colors)
        elif chart_type == "calendar":
            self._draw_calendar_chart_sync(ax, dates, values, theme_colors)

        period_label = self._get_period_label(period_days)
        ax.set_title(
            f"Настроение: {period_label}",
            color=theme_colors["fg"],
            fontsize=16,
            fontweight="bold",
            pad=20,
        )

        if include_stats:
            self._draw_stats_box_sync(ax, stats, theme_colors)

        ax.text(
            0.5,
            0.02,
            f"@mood_diary_bbot • {datetime.now().strftime('%d.%m.%Y')}",
            transform=ax.transAxes,
            ha="center",
            fontsize=8,
            color=theme_colors["text"],
            alpha=0.6,
        )

        buffer = BytesIO()
        plt.tight_layout()
        plt.savefig(
            buffer,
            format="png",
            dpi=dpi,
            facecolor=theme_colors["bg"],
            bbox_inches="tight",
        )
        plt.close(fig)

        return buffer

    async def generate_empty(
        self,
        period_days: int,
        theme: ChartTheme = "light",
        width: int = 800,
        height: int = 400,
        dpi: int = 100,
    ) -> BytesIO:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self._executor,
            self._generate_empty_sync,
            period_days,
            theme,
            width,
            height,
            dpi,
        )

    def _generate_empty_sync(
        self,
        period_days: int,
        theme: ChartTheme,
        width: int,
        height: int,
        dpi: int,
    ) -> BytesIO:
        colors: ThemeColors = self.THEMES[theme]

        fig, ax = plt.subplots(
            figsize=(width / dpi, height / dpi),
            dpi=dpi,
            facecolor=colors["bg"],
        )
        ax.set_facecolor(colors["bg"])

        ax.text(
            0.5,
            0.6,
            "[!]",
            transform=ax.transAxes,
            ha="center",
            fontsize=32,
            color=colors["fg"],
            fontweight="bold",
        )

        ax.text(
            0.5,
            0.4,
            f"Нет данных за {period_days} дней",
            transform=ax.transAxes,
            ha="center",
            fontsize=14,
            color=colors["fg"],
            fontweight="bold",
        )
        ax.text(
            0.5,
            0.3,
            "Используй /mood чтобы начать",
            transform=ax.transAxes,
            ha="center",
            fontsize=10,
            color=colors["text"],
            alpha=0.7,
        )

        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)

        buffer = BytesIO()
        plt.tight_layout()
        plt.savefig(
            buffer,
            format="png",
            dpi=dpi,
            facecolor=colors["bg"],
            bbox_inches="tight",
        )
        plt.close(fig)

        return buffer

    async def shutdown(self) -> None:
        self._executor.shutdown(wait=True)
        logger.info("Chart generator executor shutdown")

    def _draw_line_chart_sync(
        self, ax, dates: list[date], values: list[int], colors: ThemeColors
    ) -> None:
        if not dates:
            return
        ax.plot(
            dates, values, color=colors["line"], linewidth=2, marker="o", markersize=4
        )
        ax.fill_between(dates, values, 0, color=colors["fill"], alpha=0.3)
        ax.set_xlabel("Дата", color=colors["fg"])
        ax.set_ylabel("Настроение", color=colors["fg"])
        ax.set_ylim(0, 11)
        ax.set_yticks(range(0, 11, 2))
        ax.grid(True, linestyle="--", alpha=0.3, color=colors["grid"])
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m"))

    def _draw_bar_chart_sync(
        self, ax, dates: list[date], values: list[int], colors: ThemeColors
    ) -> None:
        if not dates:
            return
        x_pos = range(len(dates))
        bar_colors = [colors["mood_colors"][min(v // 2, 4)] for v in values]
        ax.bar(x_pos, values, color=bar_colors, edgecolor=colors["fg"], alpha=0.8)
        ax.set_xlabel("Записи", color=colors["fg"])
        ax.set_ylabel("Настроение", color=colors["fg"])
        ax.set_ylim(0, 11)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(
            [d.strftime("%d.%m") for d in dates], rotation=45, ha="right"
        )

    def _draw_calendar_chart_sync(
        self, ax, dates: list[date], values: list[int], colors: ThemeColors
    ) -> None:
        if not dates:
            return
        from collections import defaultdict

        weeks = defaultdict(list)
        for d, v in zip(dates, values):
            weeks[d.isocalendar()[1]].append((d, v))
        data_matrix = [
            [v for _, v in weeks.get(w, [(None, None)])[:7]]
            + [None] * (7 - len(weeks.get(w, [])))
            for w in sorted(weeks.keys())
        ]
        if data_matrix:
            im = ax.imshow(
                data_matrix, cmap="RdYlGn", aspect="auto", vmin=0, vmax=10, alpha=0.8
            )
            ax.set_yticks(range(len(data_matrix)))
            ax.set_yticklabels([f"W{w}" for w in sorted(weeks.keys())])
            ax.set_xticks(range(7))
            ax.set_xticklabels(["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"])
            plt.colorbar(im, ax=ax, label="Настроение")

    def _draw_stats_box_sync(self, ax, stats: dict, colors: ThemeColors) -> None:
        x_pos, y_pos, box_width, box_height = 0.72, 0.85, 0.25, 0.12
        rect = Rectangle(
            (x_pos, y_pos - box_height),
            box_width,
            box_height,
            transform=ax.transAxes,
            facecolor=colors["fg"],
            alpha=0.1,
            edgecolor=colors["grid"],
            linewidth=1,
        )
        ax.add_patch(rect)

        trend_indicator = {"improving": "+", "declining": "-", "stable": "="}.get(
            stats.get("trend", "stable"), "="
        )
        trend_text = {
            "improving": "растёт",
            "declining": "падает",
            "stable": "стабильно",
        }.get(stats.get("trend", "stable"), "стабильно")

        stats_text = (
            f"Статистика:\n"
            f"• Записей: {stats.get('total_entries', 0)}\n"
            f"• Среднее: {stats.get('avg_mood', 0):.1f}/10\n"
            f"• Диапазон: {stats.get('min_mood', 0)}-{stats.get('max_mood', 0)}\n"
            f"{trend_indicator} Тренд: {trend_text}"
        )

        ax.text(
            x_pos + 0.02,
            y_pos - 0.02,
            stats_text,
            transform=ax.transAxes,
            fontsize=7,
            color=colors["text"],
            va="top",
            family="monospace",
        )

    @staticmethod
    def _get_period_label(days: int) -> str:
        return {
            7: "неделя",
            30: "месяц",
            90: "3 месяца",
            180: "полгода",
            365: "год",
        }.get(days, f"{days} дней")
