from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
client = OpenAI(api_key = os.getenv("AIPIPE_API_KEY"),
                base_url ="https://aipipe.org/openai/v1")

class ChatRequest(BaseModel):
    comment: str

class ChatResponse(BaseModel):
    sentiment: str
    rating : int

@app.get("/comment")
async def get_comment():
    return {"message": "This is a comment."}

@app.post("/comment")
async def generate_comment(request: ChatRequest):
    
    if not request.comment.strip():
        raise HTTPException(status_code=400, detail="Comment cannot be empty.")
    
    try:
        response = client.beta.chat.completions.parse(
            model = "gpt-4.1-mini",
            messages = [
                {"role" : "system",
                "content" : ("You are a helpful assistant that analyzes user comments and provides sentiment analysis and a rating out of 5."
                            "The sentiment can be positive, negative, or neutral."
                            "The rating should be based on the sentiment, with positive comments receiving higher ratings and negative comments receiving lower ratings."
                            "Neutral comments should receive a rating of 3."
                            )
                },
                {
                    "role" : "user",
                    "content" : f"Analyze the following comment and provide the sentiment and rating: {request.comment}"
                }
            ],
            response_format = ChatResponse,
        )

        result = response.choices[0].message.parsed
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))