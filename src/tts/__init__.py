"""
语音合成模块
"""

from .edge_tts_engine import EdgeTTSEngine, AudioMerger
from .fish_speech import FishSpeechTTS

__all__ = ["EdgeTTSEngine", "AudioMerger", "FishSpeechTTS"]
