from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ClaimInput(BaseModel):
    wages: float
    medical: float

@app.post("/predict/")
def fake_predict(input: ClaimInput):
    # Simulate a fake model prediction for testing
    prediction = input.wages * 2 + input.medical * 0.5
    return {"predicted_settlement": prediction}
