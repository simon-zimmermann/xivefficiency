from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from db.models_generated.Item import Item


class UniversalisEntry(SQLModel, table=True):
    __tablename__ = "universalis_entry"
    __table_args__ = {'extend_existing': True}
    __allow_unmapped__ = True
    id: Optional[int] = Field(default=None, primary_key=True)
    item_id: Optional[int] = Field(default=None, foreign_key="item.id")
    item: Optional["Item"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[UniversalisEntry.item_id]"})
    quantity: int
    hq: bool
    last_review_time: datetime
    last_import_time: datetime
    single_price: int
    world_id: int  # TODO reference world table
