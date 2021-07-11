# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
#from mtTkinter import *
from tkinter import *
import tkinter
from datetime import datetime
import pytz
import sys
#from django.utils import timezone
#now = timezone.now()

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
        raise NotImplementedError
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

#
## Problem 3
## TODO: TitleTrigger
class TitleTrigger(PhraseTriggers):
    def __init__(self, phrase):
        PhraseTriggers.__init__(self, phrase)

    def evaluate(self, NewsStory):
        if type(NewsStory)==NewsStory:
            title=NewsStory.get_title()
        else:
            title=NewsStory
            
        if self.is_phrase_in(title)==True:
                return True
        else:
            return False
    def __str__(self):
        return str(self.phrase)

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
    def __str__(self):
        return str(self.phrase)
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
        else:
            if type(other)==datetime:
                time2=other.get_pubdate()
            else:
                time2=datetime.strptime(other, "%d %b %Y %H:%M:%S")

        time2=time2.replace(tzinfo=pytz.timezone('EST'))
        time3=self.time.replace(tzinfo=pytz.timezone('EST'))
        if time2>time3:
            return True
            print('asd')
        else:
            return False    


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
    trigger_file = open(filename, 'r')
    lines = []
    trigger_list=[]
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)
    for k in lines:
        lines[lines.index(k)]=k.split(',')
    t_pieces=[]
    triggers=[]
    for t in lines:
        if 'ADD' not in t:
            if 'TITLE' in t:
                index=t.index('TITLE')
                t_pieces.append(t[index-1])
                triggers.append(TitleTrigger(t[index+1]))
            if 'DESCRIPTION' in t:
                index=t.index('DESCRIPTION')
                t_pieces.append(t[index-1])
                triggers.append(DescriptionTrigger(t[index+1]))
            if 'BEFORE' in t:
                t_pieces.append(t[index-1])
                triggers.append(BeforeTrigger(t[index+1]))
            if 'AFTER' in t:
                t_pieces.append(t[index-1])
                triggers.append(AfterTrigger(t[index+1]))

            if 'AND' in t:
                t_pieces.append(t[index-1])
                triggers.append(AndTrigger(t[index+1], t[index+2]))
            if 'OR' in t:
                t_pieces.append(t[index-1])
                triggers.append(OrTrigger(t[index+1],t[index+2]))
                print('asd')
            if 'NOT' in t:
                t_pieces.append(t[index-1])
                triggers.append(NotTrigger(t[index+1]))
        else:
            for k in t:
                if k!='ADD':
                    index=t_pieces.index(k)
                    trigger_list.append(triggers[index])
    return trigger_list

file='triggers.txt'
SLEEPTIME = 120 
def main_thread(master):
    
    try:


        triggerlist = read_trigger_config(file)

        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 14))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("TITLE", justify='center')
        button = Button(frame, text="CLICK TO EXIT", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())
        while True:
            print("Polling . . .", end=' ')
            stories = process("http://news.google.com/news?output=rss")
            stories.extend(process("   "))
            stories = filter_stories(stories, triggerlist)
            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)
            time.sleep(SLEEPTIME)
            print("Sleeping...")
    except Exception as e:
        print(e)
if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

