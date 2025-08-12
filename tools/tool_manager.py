from typing import Union, Any, Optional

from model.models import ToolInfo
from tools.sleep_tools import get_sleep_report, get_month_sleep_report


class ToolManager:
    def __init__(self):
        self.__tools = [
            ToolInfo(
                name="sleep_report",
                description=
                "Daily sleep report with two parameters:\n"
                "   - patient_id: A unique identifier for the patient.\n"
                "   - date: The date for query registers in the database (Use YYYY-MM-DD format)\n",
                params=["patient_id", "date"],
                function=get_sleep_report,
            ),
            ToolInfo(
                name="month_sleep_report",
                description="Month sleep report",
                params=["patient_id", "month", "year"],
                function=get_month_sleep_report,
            )
        ]

    def get_tools(self) -> list[ToolInfo]:
        return self.__tools

    def find_by_name(self, tool_name) -> Union[Optional[ToolInfo], Any]:
        for tool in self.__tools:
            if tool.name == tool_name:
                return tool
        return None
