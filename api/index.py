from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yt_dlp

app = FastAPI()

class VideoRequest(BaseModel):
    url: str

@app.post("/api/parse")
async def parse_video(request: VideoRequest):
    url = request.url
    try:
        # 配置 yt-dlp，只提取信息，不下载视频文件
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'format': 'best', # 获取最佳质量
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            # 尝试获取直链
            video_url = info.get('url')
            title = info.get('title', 'Video')
            thumbnail = info.get('thumbnail')

            return {
                "status": "success",
                "title": title,
                "cover": thumbnail,
                "video_url": video_url
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}
