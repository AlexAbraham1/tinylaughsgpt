import llms
import tweepy
import os


def send_tweet(tweet):
    consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
    consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

    client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )
    return client.create_tweet(text=tweet)


def generate_gpt_response(model, prompt) -> str:
    result = model.complete(prompt, temperature=0.8, max_tokens=1000)
    return result.text


def format_gpt_response(response_text: str):
    response_text = response_text.strip()

    response = {
        "tweet": None,
        "hashtags": None
    }
    for line in response_text.split("\n"):
        if line.startswith("Tweet: "):
            response["tweet"] = line[7:]
        elif line.startswith("Hashtags: "):
            response["hashtags"] = line[10:]

    return response


def run():
    model = llms.init(model='gpt-3.5-turbo')
    prompt = """
        Please write a tweet for me about the parenting struggles I have with my toddler. Tweets are limited to 250 characters.
        The tweet can be me recounting a story thsat happened or it can describe a back and forth conversation I had with my toddler.
        
        In addition, please come up with a separate set of hashtags I can use along with my tweet when posting to instagram. The hashtags should be different from the original ones.
        
        Your response format should be the following
        
        Tweet: <tweet here>
        Hashtags: <hashtags here> 
    """

    response = format_gpt_response(generate_gpt_response(model, prompt))
    print(response)

    twitter_status = send_tweet(response["tweet"])
    print(twitter_status)


while __name__ == "__main__":
    run()
    exit()
