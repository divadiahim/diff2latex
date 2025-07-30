from typing import List, Tuple
from pydantic import RootModel, Field


class ColorMap(RootModel):
    root: List[Tuple[str, str]] = Field(
        default_factory=list,
        description="List of characters and their corresponding colors.",
    )
