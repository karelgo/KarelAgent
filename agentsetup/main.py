from fastapi import FastAPI, Request

from agents import (
    DataIngestionAgent, DataCleaningAgent, AnalyticsAgent, VisualizationAgent, ReportingAgent
)
from ceo_agent import ceo_approval_tool

app = FastAPI()
ingest_agent = DataIngestionAgent("IngestionAgent", ceo_approval_tool)
clean_agent = DataCleaningAgent("CleaningAgent", ceo_approval_tool)
analytics_agent = AnalyticsAgent("AnalyticsAgent", ceo_approval_tool)
visualization_agent = VisualizationAgent("VisualizationAgent", ceo_approval_tool)
reporting_agent = ReportingAgent("ReportingAgent", ceo_approval_tool)

@app.post("/ingest")
async def ingest(request: Request):
    data = await request.json()
    return {"result": ingest_agent.ingest(data.get("data"))}

@app.post("/clean")
async def clean(request: Request):
    data = await request.json()
    return {"result": clean_agent.clean(data.get("data"))}

@app.post("/analyze")
async def analyze(request: Request):
    data = await request.json()
    return {"result": analytics_agent.analyze(data.get("data"))}

@app.post("/visualize")
async def visualize(request: Request):
    data = await request.json()
    return {"result": visualization_agent.visualize(data.get("data"))}

@app.post("/report")
async def report(request: Request):
    data = await request.json()
    return {"result": reporting_agent.report(data.get("data"))}
