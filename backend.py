from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from gtts import gTTS
from fastapi.responses import FileResponse
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

class TextToSpeechRequest(BaseModel):
    text: str
    lang: str = "en"

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from gtts import gTTS
from fastapi.responses import FileResponse
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import tempfile

app = FastAPI()

class TextToSpeechRequest(BaseModel):
    text: str
    lang: str = "en"

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/tts/")
async def text_to_speech(request: TextToSpeechRequest):
    try:
        tts = gTTS(text=request.text, lang=request.lang)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            tts.save(fp.name)
            return FileResponse(fp.name, media_type='audio/mp3', filename=fp.name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)



