# Classifier schema (weights + routing)
from pydantic import BaseModel, Field

class ClassifierSchema(BaseModel):
    legal: float = Field(ge=0)
    marketing: float = Field(ge=0)
    operations: float = Field(ge=0)
    strategy: float = Field(ge=0)
    analyst: float = Field(ge=0)
    finance: float = Field(ge=0)
    top_k: list[str]
    routing_reason: str
    needs_data: list[str]

    def normalized(self) -> "ClassifierSchema":
        vals = self.model_dump()
        # Separate weights from other fields
        weight_keys = ["legal", "marketing", "operations", "strategy", "analyst", "finance"]
        weights = {k: vals[k] for k in weight_keys}
        
        s = sum(weights.values())
        if s == 0:
            equal = round(100/6)
            weights = {k: equal for k in weight_keys}
            drift = 100 - sum(weights.values())
            if drift:
                weights["legal"] += drift
        else:
            raw = {k: (v/s)*100 for k, v in weights.items()}
            rounded = {k: int(round(v)) for k, v in raw.items()}
            drift = 100 - sum(rounded.values())
            for k in sorted(raw, key=raw.get, reverse=True):
                if drift == 0: break
                rounded[k] += 1 if drift > 0 else -1
                drift += -1 if drift > 0 else 1
            weights = rounded
        
        # Combine normalized weights with other fields
        return ClassifierSchema(
            **weights,
            top_k=vals["top_k"],
            routing_reason=vals["routing_reason"],
            needs_data=vals["needs_data"]
        )

