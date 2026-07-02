from fastapi import FastAPI,HTTPException,Depends
from pydantic import BaseModel,HttpUrl
from service.analyze_service import analyze_url
from llm.claude import ClaudeLLM

from sqlalchemy.orm import Session
from database.models import Analysis
from database.database import get_db

from fastapi.middleware.cors import CORSMiddleware

from embedding.embedded import Embedder
from embedding.vector_store import VectorStore
from rag.retriever import RAGRetriever

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

embedder = Embedder()
vector_store = VectorStore(dimension=384)

def get_embedder():
    return embedder

def get_vector_store():
    return vector_store

def get_rag_retriever(llm=Depends(get_llm)):
    return RAGRetriever(embedder, vector_store, llm)

class RAGQueryRequest(BaseModel):
    question: str
    k: int = 3


@app.post("/analyze")
async def analyze(
    request : AnalyzeRequest,
    llm=Depends(get_llm), 
    db : Session = Depends(get_db),
    embedder=Depends(get_embedder),
    vector_store=Depends(get_vector_store)
):

    try :
        return await analyze_url(str(request.url), llm, db, embedder, vector_store)
    except Exception as e :
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@app.post('/rag/query')
async def rag_query(
    request : RAGQueryRequest,
    retriever : RAGRetriever = Depends(get_rag_retriever)
):
    try:
        return retriever.query(request.question, request.k)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
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

