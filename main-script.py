from config import AgentConfig, VoiceConfig
from orchestrator import Orchestrator
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    # Create configurations
    agent_config = AgentConfig(
        serper_api_key=os.getenv("SERPER_API_KEY") # Replace with actual key
    )
    voice_config = VoiceConfig()
    
    # Create orchestrator
    orchestrator = Orchestrator(agent_config, voice_config)
    
    # Generate podcast for specified companies
    companies = ['Apple']
    orchestrator.generate_podcast(companies, "company_podcast.mp3")

if __name__ == "__main__":
    main()
