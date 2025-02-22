from typing import List
from pydub import AudioSegment
from elevenlabs import play
from config import AgentConfig, VoiceConfig
from agent_processor import AgentProcessor
from text_to_speech import TextToSpeech

class Orchestrator:
    """Orchestrates the entire process of generating podcast content and audio"""
    
    def __init__(self, agent_config: AgentConfig, voice_config: VoiceConfig):
        self.agent_processor = AgentProcessor(agent_config)
        self.text_to_speech = TextToSpeech(voice_config)
    
    def generate_podcast(self, companies: List[str], output_filename: str) -> None:
        """Generate complete podcast from company list"""
        # Get conversation script from agents
        conversation = self.agent_processor.process_companies(companies)
        
        if not conversation:
            print("Error: No conversation generated")
            return
        
        # Generate audio from conversation
        self.text_to_speech.generate_audio(conversation, output_filename)
        print(f"Podcast generated successfully: {output_filename}")
        
        # Play the generated podcast
        #self._play_podcast(output_filename)
    
    @staticmethod
    def _play_podcast(filename: str) -> None:
        """Play the generated podcast"""
        try:
            audio = AudioSegment.from_mp3(filename)
            play(audio.export(format="mp3"))
        except Exception as e:
            print(f"Error playing podcast: {e}")
