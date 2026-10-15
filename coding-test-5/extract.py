import base64
from typing import List, Optional
from pydantic import BaseModel, Field
from gemini_client import client, MODEL

class Item(BaseModel):
    name: str = Field(description="Food or drink item name")
    quantity: int = Field(description="Quantity ordered, 1 if not shown")
    price: float = Field(description="Line price as a plain number, no currency symbols")

class Receipt(BaseModel):
    store: str = Field(description="Restaurant or store name")
    purchase_date: Optional[str] = Field(description="Purchase date in YYYY-MM-DD format")
    total: float = Field(description="Final total paid, as a plain number")
    items: List[Item]
    fees: float = Field(description="Sum of all non-item charges: delivery, service, packaging, tax. 0 if none")
    
PROMPT = (
    "Extract the purchase details from this food order receipt. "
    "Return the date as YYYY-MM-DD. Prices are plain numbers "
    "(e.g. 'Rp 55.000' -> 55000). If a field is not visible, use null."
)

def extract_receipt(image_bytes: bytes, mime_type: str) -> Receipt:
    interaction = client.interactions.create(
        model=MODEL,
        input=[
            {"type": "text", "text": PROMPT},
            {
                "type": "image",
                "data": base64.b64encode(image_bytes).decode("utf-8"),
                "mime_type": mime_type,
            },
        ],
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": Receipt.model_json_schema(),
        },
    )
    return Receipt.model_validate_json(interaction.output_text)