from dataclasses import dataclass
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class AgentConfig:
    """Configuration for the LLM and Agent settings"""
    model: str = "openai/gpt-4o"
    temperature: float = 0.8
    max_tokens: int = 1500
    serper_api_key:str = os.getenv("SERPER_API_KEY") # Replace with actual key

@dataclass
class VoiceConfig:
    """Configuration for voice settings"""
    host_voice_id: str = "iP95p4xoKVk53GoZ742B"
    guest_voice_id: str = "cgSgspJ2msm6clMCkdW9"
    model_id: str = "eleven_multilingual_v2"
    output_format: str = "mp3_44100_128"
    pause_duration: int = 500  # milliseconds
