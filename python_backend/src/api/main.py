from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union
import random

# --- Import live cricket scrape logic ---
import sys
import os
LIVE_CRICKET_PATH = os.path.join(os.path.dirname(__file__), "live_cricket.py")
if LIVE_CRICKET_PATH not in sys.modules:
    # classic import workaround for src/api/live_cricket.py
    from . import live_cricket
else:
    import live_cricket

# --- FASTAPI APP SETUP ---
app = FastAPI(
    title="CricketAI Scenario Analyzer API",
    description="API for AI-powered cricket scenario generation, Q&A, predictive analysis, and statistical visualizations.",
    version="1.0.0",
    openapi_tags=[
        {"name": "Scenario Generation", "description": "Generate AI cricket scenarios from match details."},
        {"name": "Q&A", "description": "Generate and interact with scenario-based questions."},
        {"name": "Analysis", "description": "AI-driven match analysis endpoints."},
        {"name": "Visualization", "description": "Data APIs for batsman and bowler visualizations."}
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models ---

# PUBLIC_INTERFACE
class MatchDetails(BaseModel):
    """Details of the ongoing or input cricket match."""
    team_a: str = Field(..., description="Name of Team A")
    team_b: str = Field(..., description="Name of Team B")
    current_score: str = Field(..., description="Current score in format 'runs/wickets'")
    overs: float = Field(..., description="Current over, e.g. 14.2")
    venue: Optional[str] = Field(None, description="Stadium or ground name")
    batsmen: List[str] = Field(..., description="List of batsmen on the field")
    bowlers: List[str] = Field(..., description="List of bowlers on the field")
    match_context: Optional[str] = Field(None, description="Any extra scenario, e.g. chase/defend/comment")

class ScenarioRequest(BaseModel):
    """Request for scenario generation."""
    match_details: MatchDetails

class ScenarioResponse(BaseModel):
    """AI-generated cricket scenario response."""
    scenario: str = Field(..., description="Text describing the scenario")
    scenario_id: str = Field(..., description="Unique scenario identifier")

class QuestionRequest(BaseModel):
    """Request for generating a cricket scenario question."""
    scenario_id: str = Field(..., description="ID of the previously generated scenario")

class QuestionResponse(BaseModel):
    """AI-generated scenario-based question."""
    question: str
    question_id: str

class AnswerRequest(BaseModel):
    """Request with user's answer to the scenario (prediction)"""
    question_id: str
    answer: str = Field(...,description="User's answer, e.g. 'yes' or 'no'")

class AnalysisRequest(BaseModel):
    """Request for analysis based on user scenario prediction."""
    scenario_id: str
    question_id: str
    user_answer: str = Field(..., description="'yes' or 'no' (the user's prediction)")

class AnalysisResponse(BaseModel):
    """AI-generated analysis text with feedback."""
    analysis: str
    recommendation: Optional[str]

class VisualizationResponse(BaseModel):
    """Match visualizations: batsman and bowler stats."""
    batsmen_performance: Dict[str, Dict[str, Union[int, float]]]
    bowlers_performance: Dict[str, Dict[str, Union[int, float]]]

# --- API ROUTES ---

@app.get("/", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {"message": "Healthy"}

# PUBLIC_INTERFACE
@app.post("/generate-scenario", response_model=ScenarioResponse, tags=["Scenario Generation"], summary="Generate a scenario", description="Generate an AI-powered cricket scenario based on match details.")
def generate_scenario(req: ScenarioRequest):
    """
    Generate a cricket scenario based on live or input match details.

    Parameters:
    - req: ScenarioRequest - includes teams, score, overs, venue, batsmen, bowlers, and context.

    Returns a unique scenario and scenario_id.
    """
    # FAKE DATA FOR DEMO PURPOSES (stub; replace with AI integration as needed)
    fake_scenarios = [
        "With 30 runs needed from 18 balls, can Team A's batsmen hold their nerve against the pace attack?",
        "Team B must defend 150 with spin in the last five overs – will their strategy pay off?",
        "Batsman Smith faces the bowler Khan, one wicket in hand with 12 to win off 6 balls – what happens next?",
    ]
    scenario = random.choice(fake_scenarios)
    scenario_id = f"SCN{random.randint(1000, 9999)}"
    return ScenarioResponse(scenario=scenario, scenario_id=scenario_id)

# PUBLIC_INTERFACE
@app.post("/generate-question", response_model=QuestionResponse, tags=["Q&A"], summary="Generate scenario-based question", description="Generate a yes/no question based on the scenario for user prediction.")
def generate_question(req: QuestionRequest):
    """
    Generate a yes/no style question about the current scenario.

    Parameters:
    - req: QuestionRequest - scenario_id as input.

    Returns: question text and question_id.
    """
    # Example question bank for demonstration
    fake_questions = [
        "Will Team A chase down the target successfully?",
        "Will the batsman score a six in this over?",
        "Will this be a wicket over for the bowler?",
        "Will the team hit more than 3 fours in the next 2 overs?",
    ]
    question = random.choice(fake_questions)
    question_id = f"Q{random.randint(10000,99999)}"
    return QuestionResponse(question=question, question_id=question_id)

# PUBLIC_INTERFACE
@app.post("/analyze-scenario", response_model=AnalysisResponse, tags=["Analysis"], summary="Get AI match scenario analysis", description="Analyze user's answer (prediction) for the scenario and generate insights/feedback.")
def analyze_scenario(req: AnalysisRequest):
    """
    Analyze the user's yes/no prediction in the context of the scenario and deliver AI-driven insights.

    Parameters:
    - req: AnalysisRequest containing scenario_id, question_id, and user's answer

    Returns analysis string and optional recommendation.
    """
    # FAKE/Static analysis for demo
    analysis_texts = [
        ("The chase looks tough, but with wickets in hand, an aggressive batting approach could turn things around.",
         "Recommend Team A to keep rotating strike and target weak bowlers."),
        ("Team B's bowlers have the edge. A disciplined field setup is key.",
         "Bringing back the main bowler might increase pressure."),
        ("It's likely to go to the last over—a thrilling finish is on the cards!",
         "Saving key batters for the final overs could help."),
    ]
    analysis, rec = random.choice(analysis_texts)
    return AnalysisResponse(analysis=analysis, recommendation=rec)

# PUBLIC_INTERFACE
@app.get("/generate-analysis", response_model=AnalysisResponse, tags=["Analysis"], summary="AI match analysis (alt)", description="Get a match analysis insight directly (extra endpoint for versatility).")
def get_match_analysis(scenario_id: str):
    """
    Generate general match analysis for a scenario.

    Query Parameters:
    - scenario_id: string (ID to reference scenario context)
    """
    # FAKE: Just reusing some analysis samples
    texts = [
        ("Team A’s run rate needs a push. Targeting weak bowlers could help boost the chase.", "Try promoting a pinch hitter if required."),
        ("The pitch favors spinners now. Tight lines will restrict scoring.", "Consider bringing in a spinner."),
    ]
    analysis, recommendation = random.choice(texts)
    return AnalysisResponse(analysis=analysis, recommendation=recommendation)

# PUBLIC_INTERFACE
@app.get("/visualizations", response_model=VisualizationResponse, tags=["Visualization"], summary="Performance visualizations", description="Get fake/statistical data for batsman and bowler visualization charts.")
def get_visualizations(match_id: Optional[str] = None):
    """
    Provides artificial or sample batsman/bowler data for frontend plotting.

    Query Parameters:
    - match_id: string (optional, to fetch match-specific stats)
    """
    batsmen_performance = {
        "S. Smith": {"runs": 56, "balls": 34, "fours": 7, "sixes": 2, "strike_rate": 164.7},
        "V. Kohli": {"runs": 78, "balls": 53, "fours": 8, "sixes": 3, "strike_rate": 147.2},
        "R. Sharma": {"runs": 32, "balls": 21, "fours": 4, "sixes": 1, "strike_rate": 152.3}
    }
    bowlers_performance = {
        "M. Starc": {"overs": 4, "runs": 28, "wickets": 2, "economy": 7.0},
        "J. Bumrah": {"overs": 4, "runs": 24, "wickets": 3, "economy": 6.0},
        "R. Ashwin": {"overs": 3, "runs": 22, "wickets": 1, "economy": 7.3}
    }
    return VisualizationResponse(
        batsmen_performance=batsmen_performance,
        bowlers_performance=bowlers_performance
    )

# --- LIVE MATCH ENDPOINT ---

# PUBLIC_INTERFACE
class LiveMatchDetails(BaseModel):
    """Schema for live cricket match details as scraped from Google."""
    team_a: str = Field(..., description="Name of Team A")
    team_b: str = Field(..., description="Name of Team B")
    score_a: str = Field(..., description="Score for Team A (runs/wickets)")
    score_b: str = Field(..., description="Score for Team B (runs/wickets)")
    overs: str = Field(..., description="Current over if available, e.g. '14.2'")
    status: str = Field(..., description="Current match status: 'Live', 'Complete', or progress description")

# PUBLIC_INTERFACE
@app.get(
    "/live-match-details",
    response_model=List[LiveMatchDetails],
    tags=["Live Data"],
    summary="Fetch live cricket match details",
    description="""
Fetch live cricket match details scraped from Google.
Returns a list of ongoing or recent matches, with teams, scores, overs, and match status.
Data is scraped in real-time from the public Google search page for "cricket match".
""",
    responses={
        200: {"description": "List of live cricket match details"},
        404: {"description": "No matches found or scraping failed"},
        500: {"description": "Internal error during fetch/scraping"}
    }
)
def get_live_match_details():
    """
    Get a list of live cricket match details by scraping Google search for "cricket match".

    Returns:
        200: List of match objects if found.
        404: No data found (no live matches or structure changed).
        500: Scraping/connection failure.
    """
    try:
        matches = live_cricket.fetch_live_cricket_details("cricket match")
        if matches is None or len(matches) == 0:
            raise HTTPException(status_code=404, detail="No live matches found (or Google result structure changed).")
        # Return as pydantic-validated models (avoids missing fields)
        return [LiveMatchDetails.model_validate(m) for m in matches]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Live match fetch error: {str(e)}")

# --- OPENAPI ENHANCEMENT (for clarity in docs) ---
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description + "\n\nNotes:\n- All endpoints return example data only by default, except `/live-match-details` which fetches real data from Google scraping.\n- Use scenario_id and question_id returned from prior endpoints as required.\n- The `/live-match-details` endpoint may break if Google's public search results layout changes.",
        routes=app.routes,
        tags=app.openapi_tags
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
