from fastapi import FastAPI,HTTPException,Depends
from pydantic import BaseModel,HttpUrl
from service.analyze_service import analyze_url
from llm.claude import ClaudeLLM

from sqlalchemy.orm import Session
from database.models import Analysis
from database.database import get_db

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    url: HttpUrl


def get_llm():
    return ClaudeLLM()

@app.post("/analyze")
async def analyze(request : AnalyzeRequest,llm=Depends(get_llm), db : Session = Depends(get_db)):

    try :
        return await analyze_url(str(request.url), llm, db)
    except Exception as e :
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@app.get('/history')
def history(db : Session = Depends(get_db)):
    return db.query(Analysis).all()

@app.get("/history/{id}")
def history_detail(
    id: int,
    db: Session = Depends(get_db)
):

    return db.query(Analysis).filter(
        Analysis.id == id
    ).first()

@app.delete("/history/{id}")
def delete_history(
    id: int,
    db: Session = Depends(get_db)
):

    result = db.query(
        Analysis
    ).filter(
        Analysis.id == id
    ).first()

    if result is None:

        return {
            "message":"Not Found"
        }

    db.delete(result)

    db.commit()

    return {
        "message":"Deleted"
    }

