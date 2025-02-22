from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from config import AgentConfig, VoiceConfig
from orchestrator import Orchestrator
import os
from dotenv import load_dotenv

load_dotenv()

# Create configurations
agent_config = AgentConfig(
    serper_api_key = os.getenv("SERPER_API_KEY")  # Replace with actual key
)
voice_config = VoiceConfig()

# Create orchestrator
orchestrator = Orchestrator(agent_config, voice_config)

# Initialize FastAPI app
app = FastAPI()

# Define request model
class PodcastRequest(BaseModel):
    companies: list[str]
    output_file: str = "company_podcast.mp3"

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}
import logging

logging.basicConfig(level=logging.INFO)

@app.post("/generate-podcast")
def generate_podcast(request: PodcastRequest):
    try:
        # Validate input
        if not request.companies:
            raise HTTPException(status_code=400, detail="No companies provided")

        logging.info(f"Generating podcast for companies: {request.companies}")

        # Generate podcast
        orchestrator.generate_podcast(request.companies, request.output_file)

        logging.info(f"Podcast generated successfully: {request.output_file}")

        # Return success response
        return {"message": f"Podcast generated successfully and saved as {request.output_file}"}

    except Exception as e:
        logging.error(f"Error generating podcast: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)