import json
from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException
from pydantic import HttpUrl
from models import ContentItem
from processors import TwitterFeedProcessor


class TweetService:
    """Service to handle all tweet operations."""

    def __init__(self, file_path: str = "sample_posts.json"):
        self.file_path = file_path
        self.tweets = self.load_tweets()

    def load_tweets(self) -> List[ContentItem]:
        """Load tweets from file into memory."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as fp:
                raw_tweets = json.load(fp)["data"][:100]

            processor = TwitterFeedProcessor()
            tweets = [
                processor.process_tweet(tweet, idx).dict()
                for idx, tweet in enumerate(raw_tweets)
            ]

            # Ensure data is serialized properly
            for item in tweets:
                item["url"] = (
                    str(item["url"]) if isinstance(item["url"], HttpUrl) else ""
                )
                item["embeded_image"] = (
                    str(item["embeded_image"])
                    if isinstance(item["embeded_image"], HttpUrl)
                    else ""
                )
                item["created_at"] = (
                    item["created_at"].isoformat()
                    if isinstance(item["created_at"], datetime)
                    else ""
                )

                item["retweet_by"] = item.get("retweet_by", "")
                item["quoted_by"] = item.get("quoted_by", "")
                if item["embeded_images"]:
                    for i, url in enumerate(item["embeded_images"]):
                        item["embeded_images"][i] =  str(url)


            return tweets

        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="Feed file not found.")
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=400, detail="Invalid JSON format in feed file."
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_tweets(self) -> List[ContentItem]:
        """Return the list of tweets."""
        return self.tweets

    def find_tweet(self, tweet_id: int) -> Optional[dict]:
        """Find a tweet by its ID."""
        return next((tweet for tweet in self.tweets if (tweet["id"]) == str(tweet_id)), None)

    def like_tweet(self, tweet_id: int) -> dict:
        """Toggle like status for a tweet."""
        tweet = self.find_tweet(tweet_id)
        if tweet is None:
            raise HTTPException(status_code=404, detail="Tweet not found.")

        tweet["engagements"]["liked"] = not tweet["engagements"]["liked"]
        tweet["engagements"]["likes"] += 1 if tweet["engagements"]["liked"] else -1
        return tweet

    def retweet_tweet(self, tweet_id: int) -> dict:
        """Toggle retweet status for a tweet."""
        tweet = self.find_tweet(tweet_id)
        if tweet is None:
            raise HTTPException(status_code=404, detail="Tweet not found.")

        tweet["engagements"]["retweeted"] = not tweet["engagements"]["retweeted"]
        tweet["engagements"]["retweets"] += (
            1 if tweet["engagements"]["retweeted"] else -1
        )
        return tweet
