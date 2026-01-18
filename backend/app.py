from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

class Voter(BaseModel):
    id: str
    name: str
    eligible: bool

class Ballot(BaseModel):
    voter_id: str
    candidate: str

class ElectionResult(BaseModel):
    candidate: str
    votes: int

voters = []  # In-memory storage
ballots = []
results = {}  # In-memory storage

@app.post('/register', response_model=Voter)
async def register_voter(voter: Voter):
    if voter.id in [v.id for v in voters]:
        raise HTTPException(status_code=400, detail='Voter already registered')
    voters.append(voter)
    return voter

@app.post('/vote', response_model=Ballot)
async def cast_vote(ballot: Ballot):
    if ballot.voter_id not in [v.id for v in voters]:
        raise HTTPException(status_code=400, detail='Voter not registered')
    ballots.append(ballot)
    results[ballot.candidate] = results.get(ballot.candidate, 0) + 1
    return ballot

@app.get('/results', response_model=List[ElectionResult])
async def get_results():
    return [ElectionResult(candidate=c, votes=v) for c, v in results.items()]