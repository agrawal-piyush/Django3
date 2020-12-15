#django Libraries
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate,login
from .forms import LoginForm,UserRegistrationForm,SearchForm
from django.contrib import messages
from .models import Search1
from django.contrib.auth.decorators import login_required
#project Libraries
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

#Home page
@login_required
def dashboard(request):
    return render(request,'registration/dashboard.html')

def user_login(request):
    if request.method=='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['username'],password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponse('Authenticated Successfuly')
                else:
                    return HttpResponse('Disabled Account')
            else:
                return HttpResponse('Invalid Login')
    else:
        form=LoginForm()
    return render (request,'registration/login.html',{'form':form})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new = user_form.save(commit =False)
            new.set_password(user_form.cleaned_data['password'])
            new.save()
            return render(request,'registration/register_done.html',{'new_user':new})
    else:
        user_form = UserRegistrationForm()
    return render(request,'registration/register.html',{'user_form':user_form})

#Now views for twitter sentiments
def SAF(request):
    global keyword
    form = SearchForm()
    if request.method =='POST':
        form=SearchForm(request.POST,request.FILES)
        if form.is_valid():
            keyword=form.cleaned_data.get("search")
            form.save()
            #Twiter work started from here
            #authentication
            consumer_key = 'Enter The consumer_key'
            consumer_secret = 'Enter The consumer_secret'
            access_token = 'Enter The access_token'
            access_token_secret = 'Enter The access_token_secret'
            try:
                auth= OAuthHandler(consumer_key,consumer_secret)
                auth.set_access_token(access_token,access_token_secret)
                api=tweepy.API(auth)
            except:
                print("Authentication Fail")
            #list for tweet results
            l=[]
            #method  to fetch tweets
            tweets = []
            try:
                     #method to fetch tweets
                    fetched_tweets = api.search(q = keyword, count = 200)
                    for tweet in fetched_tweets:
                        parsed_tweet = {}
                        parsed_tweet['text'] = tweet.text
                        parsed_tweet['sentiment'] = get_sentiment(tweet.text)
                        #checkig retweeting
                        if tweet.retweet_count > 0:
                            if parsed_tweet not in tweets:
                                tweets.append(parsed_tweet)
                        else:
                            tweets.append(parsed_tweet)


                #Error handling like tweet not found or other
            except tweepy.TweepError as e:
                    print("Error : " + str(e))

            #fetching tweets with appreciating sentiment
            ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'Appriciative']
            #storing the percentage in list
            l.append(100*len(ptweets)/len(tweets))
            #fetching criticizing tweets
            ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'Criticize']
            #storing the percentage in list
            l.append(100*len(ntweets)/len(tweets))
            #storing the percentage in list of neutral tweets
            l.append(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets))
            '''
            json_records = ptweets.reset_index().to_json(orient ='text')
            data =[]
            data = json.loads(json_records)
                #positive = ptweets[ptweets['text']:10]
                '''

            return render(request,"registration/Result.html",{'k1':l[0],
            'k2':l[1],'k3':l[2],'k4':keyword,'positive':ptweets[:20],'negative':ntweets[:20]})
    return render(request,"registration/Searchform.html",{'form':form})
def Record(request):
        ud=Search1.objects.filter(username=request.user)
        return render(request,'registration/record.html',{'UD':ud})

def clean(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
#method to find sentiment of tweets
def get_sentiment(tweet):
    #textblob object
    analysis = TextBlob(clean(tweet))
    #finding polarity
    if (analysis.sentiment.polarity > 0):
        return 'Appriciative'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'Criticize'
