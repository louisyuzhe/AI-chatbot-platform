# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 22:35:22 2020

@author: Yu Zhe
"""

#Importing modules
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer #train chatbot on a custom list of statements 
from chatterbot.trainers import ChatterBotCorpusTrainer


"""
Instantiating a ChatBot Instance
"""
#chatbot will be set to read_only to avoid learning after training
chatbot1 = ChatBot(name = 'chatbot1',
                  read_only = False,                  
                  logic_adapters = ["chatterbot.logic.BestMatch"],                 
                  storage_adapter = "chatterbot.storage.SQLStorageAdapter")


"""
Training on Corpus Data
"""
#instantiate a ChatterBotCorpusTrainer object with the chatbot as arg
corpus_trainer = ChatterBotCorpusTrainer(chatbot1)
#Train dataset (ChatterBot-Corpus)
corpus_trainer.train("train_data/chatterbot_corpus/data/english")

"""
Training on Custom List Data
Train the chatbot using custom conversations
Each statement in the list is a possible response to it’s predecessor in the list.
"""
greet_conversation = [
    "Hello",
    "Hi there!",
    "How are you doing?",
    "I'm doing great.",
    "That is good to hear",
    "Thank you.",
    "You're welcome."
]
 
open_timings_conversation = [
    "What time does the Bank open?",
    "The Bank opens at 9AM",
]
 
close_timings_conversation = [
    "What time does the Bank close?",
    "The Bank closes at 5PM",
]

#Initializing Trainer Object
trainer = ListTrainer(chatbot1)

#Training BankBot
trainer.train(greet_conversation)
trainer.train(open_timings_conversation)
trainer.train(close_timings_conversation)