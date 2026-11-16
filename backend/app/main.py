from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from jose import jwt, JWTError
from .config import settings
from .db import init_db, connect
from .security import hash_password, verify_password, make_token
from .schemas import Credentials, StoryRequest, ImageRequest, VideoRequest, ImageVideoRequest, VoiceRequest
from . import providers
app=FastAPI(title="YONO AI API",version="0.1.0")
app.add_middleware(CORSMiddleware,allow_origins=settings.origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
@app.on_event("startup")
def startup(): init_db()
def user_id(authorization:str=Header(default="")):
    if not authorization.startswith("Bearer "): raise HTTPException(401,"Login required")
    try: return int(jwt.decode(authorization[7:],settings.jwt_secret,algorithms=["HS256"])["sub"])
    except (JWTError,ValueError,KeyError): raise HTTPException(401,"Invalid or expired token")
@app.get("/health")
def health(): return {"ok":True,"service":"yono-ai-api"}
@app.get("/api/v1/providers/status")
def status():
    return {"openai":bool(settings.openai_api_key),"leonardo":bool(settings.leonardo_api_key),
      "kling":bool(settings.kling_api_key),"elevenlabs":bool(settings.elevenlabs_api_key and settings.elevenlabs_voice_id)}
@app.post("/api/v1/auth/signup")
def signup(b:Credentials):
    try:
        with connect() as c:
            cur=c.execute("INSERT INTO users(email,password_hash) VALUES(?,?)",(b.email.lower(),hash_password(b.password))); c.commit()
        return {"access_token":make_token(cur.lastrowid),"token_type":"bearer"}
    except Exception: raise HTTPException(409,"Email already registered or database error")
@app.post("/api/v1/auth/login")
def login(b:Credentials):
    with connect() as c: u=c.execute("SELECT id,password_hash FROM users WHERE email=?",(b.email.lower(),)).fetchone()
    if not u or not verify_password(b.password,u["password_hash"]): raise HTTPException(401,"Incorrect email or password")
    return {"access_token":make_token(u["id"]),"token_type":"bearer"}
@app.post("/api/v1/story/generate")
async def make_story(b:StoryRequest, uid:int=Depends(user_id)):
    try: return {"provider":"openai","story_json":await providers.story(b.idea,b.language,b.style,b.episode_minutes)}
    except providers.ProviderNotConfigured as e: raise HTTPException(503,str(e))
    except Exception as e: raise HTTPException(502,f"OpenAI failed: {str(e)[:250]}")
@app.post("/api/v1/images/generate")
async def make_image(b:ImageRequest, uid:int=Depends(user_id)):
    try: return {"provider":"leonardo","task":await providers.image(b.prompt,b.character_bible)}
    except providers.ProviderNotConfigured as e: raise HTTPException(503,str(e))
    except Exception as e: raise HTTPException(502,f"Leonardo failed: {str(e)[:250]}")
@app.post("/api/v1/videos/text-to-video")
async def make_video(b:VideoRequest, uid:int=Depends(user_id)):
    try: return {"provider":"kling","task":await providers.video(b.prompt,b.duration,b.aspect_ratio,b.resolution)}
    except providers.ProviderNotConfigured as e: raise HTTPException(503,str(e))
    except Exception as e: raise HTTPException(502,f"Kling failed: {str(e)[:250]}")
@app.post("/api/v1/voice/synthesize")
async def make_voice(b:VoiceRequest, uid:int=Depends(user_id)):
    try: return Response(await providers.voice(b.text),media_type="audio/mpeg",headers={"Content-Disposition":"attachment; filename=narration.mp3"})
    except providers.ProviderNotConfigured as e: raise HTTPException(503,str(e))
    except Exception as e: raise HTTPException(502,f"ElevenLabs failed: {str(e)[:250]}")


@app.post("/api/v1/videos/image-to-video")
async def make_image_video(b: ImageVideoRequest, uid: int = Depends(user_id)):
    try:
        task = await providers.image_to_video(str(b.image_url), b.prompt, b.duration, b.resolution)
        return {"provider": "kling", "mode": "image-to-video", "task": task}
    except providers.ProviderNotConfigured as e:
        raise HTTPException(503, str(e))
    except Exception as e:
        raise HTTPException(502, f"Kling image-to-video failed: {str(e)[:250]}")

@app.get("/api/v1/videos/{task_id}")
async def get_video_task(task_id: str, uid: int = Depends(user_id)):
    try:
        return await providers.task_status(task_id)
    except providers.ProviderNotConfigured as e:
        raise HTTPException(503, str(e))
    except Exception as e:
        raise HTTPException(502, f"Kling task status failed: {str(e)[:250]}")
