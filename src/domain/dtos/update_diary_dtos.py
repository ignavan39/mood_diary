from dataclasses import dataclass
from typing import Any, Dict, Optional
from datetime import date as date_type


@dataclass
class UpdateDiaryDTO:
    id: int
    rating: Optional[int] = None
    date: Optional[date_type] = None

    def has_changes(self) -> bool:
        return any(
            [
                self.rating is not None,
                self.date is not None,
            ]
        )

    def get_fields_to_update(self) -> Dict[str, Any]:
        fields: Dict[str, Any] = {}

        if self.rating is not None:
            fields["rating"] = self.rating

        if self.date is not None:
            fields["date"] = self.date

        return fields
