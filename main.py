from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from services import TweetService  # Import the new service

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize TweetService
tweet_service = TweetService()


@app.get("/")
async def home(request: Request):
    tweets = tweet_service.get_tweets()
    return templates.TemplateResponse(
        "index.html", {"request": request, "tweets": tweets}
    )


@app.get("/feed", response_model=list)
async def get_feed():
    """Returns the processed tweet feed."""
    return JSONResponse(tweet_service.get_tweets())  


@app.post("/like/{tweet_id}")
async def like_tweet(request: Request, tweet_id: int):
    """Handles liking a tweet."""
    tweet = tweet_service.like_tweet(tweet_id)
    return templates.TemplateResponse(
        "like_button.html", {"request": request, "tweet": tweet}
    )


@app.post("/retweet/{tweet_id}")
async def retweet_tweet(request: Request, tweet_id: int):
    """Handles retweeting a tweet."""
    tweet = tweet_service.retweet_tweet(tweet_id)
    return templates.TemplateResponse(
        "retweet_button.html", {"request": request, "tweet": tweet}
    )

# add endpoints for 
