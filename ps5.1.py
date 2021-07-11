# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid=guid
        self.title=title
        self.description=description
        self.link=link
        self.pubdate=pubdate
    def get_guid(self):
        return self.guid
    def get_title(self):
        return self.title
    def get_description(self):
        return self.description
    def get_link(self):
        return self.link
    def get_pubdate(self):
        return self.pubdate
    def __str__(self):
        return 'GUID:'+' '+str(self.guid)+' '+'TITLE:'+' '+str(self.title)+' '+'DESCRIPTION: '+str(self.description)+' '+'LINK: '+str(self.link)+' '+ 'PUBDATE: '+str(self.pubdate)
    def lower(self):
        self=str(self)
        return self.lower()
    def __append__(self, other):
#        return other.append(str(self))
        return other.append('x')
#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!

        raise NotImplementedError
a=NewsStory('', 'The purple cow is soft and cuddly.', '', '', datetime.now())
#print(a.get_title())
# PHRASE TRIGGERS
# Problem 2
class PhraseTriggers(Trigger):
    def __init__(self, phrase):
        self.phrase=phrase
    def is_phrase_in(self, text):
        self.phrase=(self.phrase).lower()
        if type(text)==NewsStory:
            text=text.get_title()
        text=text.lower()
        puntuations=string.punctuation
        for a in puntuations:
            if a in self.phrase:
                return 'not a valid phrase'
            if a in text:
                text=text.replace(a,' ')
        liste=(self.phrase).split()
        if self.phrase[0]==' ' and  self.phrase[-1]==' ':
            if len(liste)-1 != (self.phrase).count(' ')-2:
                return 'not a valid phrase'
        if self.phrase[0]==' ' and  self.phrase[-1]!=' ':
            if len(liste)-1 != (self.phrase).count(' ')-1:
                return 'not a valid phrase'         
        if self.phrase[0]!=' ' and self.phrase[-1]!=' ':
            if len(liste)-1 != (self.phrase).count(' '):
                return 'not a valid phrase'
        text=text.split()
        
        text=' '.join(text)
        liste=' '.join(liste)
        liste2=(liste).split()
        text2=text.split()
        if all(elem in text2 for elem in liste2):
            if liste in text:
                return True
        else:
            return False
        def evaluate(self, story):
            if self.is_phrase_in(story)==True:
                return True
            else:
                return False
#a=PhraseTriggers('The purple cow is soft and cuddly.')

#print(a.is_phrase_in('as'))

#
## Problem 3
## TODO: TitleTrigger
class TitleTrigger(PhraseTriggers):
    def __init__(self, phrase):
        PhraseTriggers.__init__(self, phrase)

    def evaluate(self, NewsStory):
        title=NewsStory.get_title()
        if self.is_phrase_in(title)==True:
                return True
        else:
            return False
#b=TitleTrigger('PURPLE COW')
#print(b.is_phrase_in(a))
#a=NewsStory('', 'The purple cow is soft and cuddly.', '', '', datetime.now())
#print(b.evaluate(a))
# Problem 4
## TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTriggers):
    def __init__(self, phrase):
        PhraseTriggers.__init__(self, phrase)
    def evaluate(self, NewsStory):
        description=NewsStory.get_description()
        if self.is_phrase_in(description)==True:
                return True
        else:
            return False
    
## TIME TRIGGERS
#
## Problem 5
## TODO: TimeTrigger
## Constructor:
##        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
##        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def __init__(self, string_time):
        self.string_time=string_time
        self.time=datetime.strptime(string_time, "%d %b %Y %H:%M:%S")
    def get_time(self):
        return self.time
#a=TimeTrigger( '03 Oct 2016 17:10:11')
#print(a.get_time())
        
## Problem 6
## TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def __init__(self, string_time):
        TimeTrigger.__init__(self,string_time)
    def evaluate(self, other):
        if type(other)==NewsStory:
            if type(other.get_pubdate())==datetime:
                time2=other.get_pubdate()
            else:
                time2=datetime.strptime(other.get_pubdate(), "%d %b %Y %H:%M:%S")
        time2=time2.replace(tzinfo=pytz.timezone('EST'))
        time3=self.time.replace(tzinfo=pytz.timezone('EST'))
        if time2<time3:
            return True
        else:
            return False    
class AfterTrigger(TimeTrigger):
    def __init__(self, string_time):
        TimeTrigger.__init__(self,string_time)
    def evaluate(self, other):
        if type(other)==NewsStory:
            if type(other.get_pubdate())==datetime:
                time2=other.get_pubdate()
            else:
                time2=datetime.strptime(other.get_pubdate(), "%d %b %Y %H:%M:%S")
        time2=time2.replace(tzinfo=pytz.timezone('EST'))
        time3=self.time.replace(tzinfo=pytz.timezone('EST'))
        if time2>time3:
            return True
        else:
            return False    


#
## COMPOSITE TRIGGERS
#
## Problem 7
## TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger=trigger
    def evaluate(self, other):
        return not self.trigger.evaluate(other)
        
## Problem 8
## TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1=trigger1
        self.trigger2=trigger2
    def evaluate(self, other):
        if (self.trigger1).evaluate(other)==True:  
            if (self.trigger2).evaluate(other)==True:
                return True
            else:
                return False
        else:
            
            return False
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1=trigger1
        self.trigger2=trigger2
    def evaluate(self, other):
        if self.trigger1.evaluate(other)==True:
            return True
        if self.trigger2.evaluate(other)==True:
            return True
        else:
            return False
## Problem 9
## TODO: OrTrigger
#
#
##======================
## Filtering
##======================
#
# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    new_stories=[]
    for s in triggerlist:
        for t in stories:
            if s.evaluate(t)==True:
                new_stories.append(t)
    return new_stories

#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    print(lines) # for now, print it so you see what it contains!



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("trump")
#        t2 = DescriptionTrigger("")
#        t3 = DescriptionTrigger()
#        t4 = AndTrigger(t2, t3)
        triggerlist = [t1]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        # triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
#        # Retrieves and filters the stories from the RSS feeds
#        frame = Frame(master)
#        frame.pack(side=BOTTOM)
#        scrollbar = Scrollbar(master)
#        scrollbar.pack(side=RIGHT,fill=Y)

#        t = "Google & Yahoo Top News"
#        title = StringVar()
#        title.set(t)
#        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
#        ttl.pack(side=TOP)
#        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
#        cont.pack(side=BOTTOM)
#        cont.tag_config("title", justify='center')
#        button = Button(frame, text="Exit", command=root.destroy)
#        button.pack(side=BOTTOM)
#        guidShown = []
#        def get_cont(newstory):1

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")
#            print('f')
            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))
            
            stories = filter_stories(stories, triggerlist)
            print(stories)
            list(map(get_cont, stories))
#            scrollbar.config(command=cont.yview)


#            print("Sleeping1...")
#            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

