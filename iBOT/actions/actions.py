# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

#system-dependencies
import os
import pandas as pd
from datetime import datetime,timedelta
import time

#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class ActionOpenedApp(Action):

    def name(self) -> Text:
        return "action_opened_app"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        top=5
        output = os.popen('wmic process get name, creationdate /format:csv')
        df=pd.read_csv(output).drop(['Node'],axis=1)
        df['CreationDate']=df['CreationDate'].str.split('.').str[0]
        df['CreationDate'] = pd.to_datetime(df['CreationDate'], format='%Y%m%d%H%M%S')
        today=datetime.now()
        today=datetime.strptime(today.strftime("%Y-%m-%d 00:00:00"),'%Y-%m-%d %H:%M:%S')
        df=df[df['CreationDate'] >= today]
        df=df.groupby('Name').agg('count')
        df=df.sort_values(['CreationDate'],ascending=False)[:top]
        df.rename(columns={'CreationDate':'No.of.times.opened'},inplace=True)
        fig = df.plot(kind='bar',figsize=(5, 5)).get_figure()
        fig.savefig('./actions/test.jpg')
#         time.sleep(0.5)
        img='http://localhost:7000/img/test.jpg'
        dispatcher.utter_message(text=df.index[0],image=img)
        

        return []

class ActionMoreRam(Action):

    def name(self) -> Text:
        return "action_more_ram"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        top=5
        output = os.popen('wmic process get name, workingsetsize /format:csv')
        df=pd.read_csv(output).drop(['Node'],axis=1)
        df.rename(columns={'WorkingSetSize':'WorkingSetSize(MB)'},inplace=True)
        df['WorkingSetSize(MB)']=round(df['WorkingSetSize(MB)']/10**6,3)
        df=df.drop_duplicates(subset ="Name",keep ='first')
        df=df.sort_values(['WorkingSetSize(MB)'],ascending=False)[:top]
        df.set_index('Name',inplace=True)
        df.rename(columns={'WorkingSetSize(MB)':'occupied iN (MB)'},inplace=True)
        fig=df.plot(kind='bar',figsize=(5, 5)).get_figure()
        fig.savefig('./actions/test1.jpg')
#         time.sleep(0.5)
        img='http://localhost:7000/img/test1.jpg'
        dispatcher.utter_message(text=df.index[0],image=img)

        return []    
    
class ActionMoreCpu(Action):

    def name(self) -> Text:
        return "action_more_cpu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        top=5
        output = os.popen('wmic path win32_perfformatteddata_perfproc_process where (PercentProcessorTime ^> 10) get Name, PercentProcessorTime /format:csv')
        df=pd.read_csv(output).drop(['Node'],axis=1)
        df=df.sort_values(['PercentProcessorTime'],ascending=False)[:top]
        df.set_index('Name',inplace=True)
        df.rename(columns={'Name':'Process_Name','PercentProcessorTime':'Ram Utilised iN (MB)'},inplace=True)
        fig=df.plot(kind='bar',figsize=(5, 5)).get_figure()
        fig.savefig('./actions/test2.jpg')
#         time.sleep(0.5)
        img='http://localhost:7000/img/test2.jpg'
        dispatcher.utter_message(text='here ! ',image=img)

        return []    
    
    
    
    
class ActionScheduledTask(Action):

    def name(self) -> Text:
        return "action_scheduled_task"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        output=os.popen('schtasks /FO CSV')
        df=pd.read_csv(output)
        df.dropna(subset=['Next Run Time'],inplace=True)
        df=df[df['Next Run Time'].str.contains('\d{2}:\d{2}:\d{2}')].sort_values('Next Run Time')[:1]
#         time.sleep(0.5)
        dispatcher.utter_message(text=df.iloc[0]['TaskName'].split('\\')[-1]+' '+df.iloc[0]['Next Run Time'])
  

        return []    
    
    
class ActionCriticalEvent(Action):

    def name(self) -> Text:
        return "action_critical_event"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        output = os.popen('WMIC NTEVENT WHERE "EventType={}" GET SourceName,Type /format:csv'.format("'1'"))
        df=pd.read_csv(output).drop(['Node'],axis=1)
        df=df.groupby('SourceName').agg('count')
        fig=df.plot(kind='bar',figsize=(5, 5)).get_figure()
        fig.savefig('./actions/test3.jpg')
#         time.sleep(0.5)
        img='http://localhost:7000/img/test3.jpg'
        dispatcher.utter_message(text="These Apps created many critical events",image=img)

        return []    
    
    
# class ActionListen(Action):

#     def name(self) -> Text:
#         return "action_listen"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="collecting Data..")

#         return []    
    
    
    
    
    
