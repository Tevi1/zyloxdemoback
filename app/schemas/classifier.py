# Classifier schema (weights)
from pydantic import BaseModel, Field

class ClassifierSchema(BaseModel):
    legal: float = Field(ge=0)
    marketing: float = Field(ge=0)
    operations: float = Field(ge=0)
    strategy: float = Field(ge=0)
    analyst: float = Field(ge=0)
    finance: float = Field(ge=0)

    def normalized(self) -> "ClassifierSchema":
        vals = self.model_dump()
        s = sum(vals.values())
        if s == 0:
            equal = round(100/6)
            vals = {k: equal for k in vals}
            drift = 100 - sum(vals.values())
            if drift:
                vals["legal"] += drift
            return ClassifierSchema(**vals)
        raw = {k: (v/s)*100 for k, v in vals.items()}
        rounded = {k: int(round(v)) for k, v in raw.items()}
        drift = 100 - sum(rounded.values())
        for k in sorted(raw, key=raw.get, reverse=True):
            if drift == 0: break
            rounded[k] += 1 if drift > 0 else -1
            drift += -1 if drift > 0 else 1
        return ClassifierSchema(**rounded)

