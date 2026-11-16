from pydantic import BaseModel, EmailStr, Field, HttpUrl

class Credentials(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class StoryRequest(BaseModel):
    idea: str = Field(min_length=3, max_length=2000)
    language: str = "hi"
    style: str = "anime"
    episode_minutes: int = Field(default=3, ge=1, le=15)

class ImageRequest(BaseModel):
    prompt: str = Field(min_length=3, max_length=4000)
    character_bible: str = Field(default="", max_length=3000)

class VideoRequest(BaseModel):
    prompt: str = Field(min_length=3, max_length=8000)
    duration: int = Field(default=5, ge=5, le=10)
    aspect_ratio: str = "16:9"
    resolution: str = "720p"

class ImageVideoRequest(BaseModel):
    image_url: HttpUrl
    prompt: str = Field(min_length=3, max_length=4000)
    duration: int = Field(default=5, ge=5, le=10)
    resolution: str = "720p"

class VoiceRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)
    language: str = "hi"
