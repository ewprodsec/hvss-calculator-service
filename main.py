import json
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from hvss_calc import Hvss, HvssBaseResult

# HVSS core calculator implementation class to actually calculate the score from provided vector
calc: Hvss = Hvss()

app = FastAPI(
    title="HVSS v1.0",
    description="Healthcare Vulnerability Scoring System (HVSS) Version 1.0 Calculator.",
    version="1.0"
)


@app.get("/score")
async def get_score(vector: str):
    # print(f'DEBUG:\t  Received vector: "{vector}"')
    hvss_result: HvssBaseResult = calc.calculate(vector)
    print(f'DEBUG:  Sending Response:\n{json.dumps(hvss_result, default=lambda o: o.__dict__, indent=2)}')
    return hvss_result


@app.get("/simple", include_in_schema=False)
async def redirect_simple():
    return RedirectResponse(url='/simple/')


@app.exception_handler(404)
async def custom_404_handler(_, __):
    return RedirectResponse("/")


app.mount("/simple", StaticFiles(directory="static/simple", html=True), name="simple")
app.mount("/", StaticFiles(directory="static/fancy", html=True), name="fancy")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
