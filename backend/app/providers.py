from app.config import settings

def provider_status():
    return {
        'gemini': {'configured': bool(settings.gemini_api_key), 'integration': 'implemented', 'features': ['story_generation', 'scene_planning'], 'status': 'configured_unverified' if settings.gemini_api_key else 'missing_credentials'},
        'openai': {'configured': bool(settings.openai_api_key), 'integration': 'implemented', 'features': ['story_generation', 'scene_planning'], 'status': 'configured_unverified' if settings.openai_api_key else 'missing_credentials'},
        'leonardo': {'configured': bool(settings.leonardo_api_key), 'integration': 'implemented', 'features': ['character_images', 'scene_images'], 'status': 'configured_unverified' if settings.leonardo_api_key else 'missing_credentials'},
        'kling': {'configured': bool(settings.kling_api_key or (settings.kling_access_key and settings.kling_secret_key)), 'integration': 'implemented', 'features': ['text_to_video', 'image_to_video', 'task_polling'], 'status': 'configured_unverified' if (settings.kling_api_key or (settings.kling_access_key and settings.kling_secret_key)) else 'missing_credentials'},
        'elevenlabs': {'configured': bool(settings.elevenlabs_api_key and settings.elevenlabs_voice_id), 'integration': 'implemented', 'features': ['hindi_voiceover', 'multilingual_tts'], 'status': 'configured_unverified' if (settings.elevenlabs_api_key and settings.elevenlabs_voice_id) else 'missing_credentials'},
        'renderer': {'configured': True, 'integration': 'implemented', 'features': ['mp4_concat', '720p_h264_aac'], 'status': 'available' if __import__('shutil').which(settings.ffmpeg_path) else 'ffmpeg_missing'},
    }

def require_provider(name: str):
    info = provider_status().get(name)
    if not info or not info['configured']:
        raise RuntimeError(f'{name.title()} credentials are missing. Add the required values to backend/.env and restart the API.')
