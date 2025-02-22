from typing import List, Tuple
from elevenlabs.client import ElevenLabs
from elevenlabs import play
from pydub import AudioSegment
import os
from config import VoiceConfig

class TextToSpeech:
    """Handles text-to-speech conversion and audio processing"""
    
    def __init__(self, config: VoiceConfig):
        self.config = config
        self.client = ElevenLabs()
        
    def generate_audio(self, conversation: List[Tuple[str, str]], output_filename: str) -> None:
        """Generate audio file from conversation"""
        audio_files = []
        
        # Generate individual audio files
        for i, (speaker, text) in enumerate(conversation):
            filename = f"temp_part_{i}.mp3"
            voice_id = self.config.host_voice_id if speaker == "Host" else self.config.guest_voice_id
            self._text_to_speech(text, voice_id, filename)
            audio_files.append(filename)
        
        # Combine audio files
        self._combine_audio_files(audio_files, output_filename)
        
        # Cleanup
        self._cleanup_temp_files(audio_files)
    
    def _text_to_speech(self, text: str, voice_id: str, filename: str) -> None:
        """Convert text to speech"""
        audio_stream = self.client.text_to_speech.convert_as_stream(
            text=text,
            voice_id=voice_id,
            model_id=self.config.model_id,
            output_format=self.config.output_format
        )
        
        with open(filename, "wb") as f:
            for chunk in audio_stream:
                if isinstance(chunk, bytes):
                    f.write(chunk)
    
    def _combine_audio_files(self, audio_files: List[str], output_filename: str) -> None:
        """Combine multiple audio files into one"""
        combined = AudioSegment.empty()
        for file in audio_files:
            segment = AudioSegment.from_mp3(file)
            combined += segment
            combined += AudioSegment.silent(duration=self.config.pause_duration)
        
        combined.export(output_filename, format="mp3")
    
    @staticmethod
    def _cleanup_temp_files(files: List[str]) -> None:
        """Remove temporary audio files"""
        for file in files:
            if os.path.exists(file):
                os.remove(file)
