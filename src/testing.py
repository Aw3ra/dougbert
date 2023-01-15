import discord_stuff
import generate_tweet

test_tweet = 'This is a test tweet with a bunch of info on how to get the tweets, im adding some extra characters so the tweet gets longer and longer to test the validity of making longer tweets'


response = generate_tweet.get_response(test_tweet, 'Doug')
print(response)