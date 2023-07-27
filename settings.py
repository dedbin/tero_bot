import random
import openai
import telebot
from telebot import types
import datetime
import requests
from googletrans import Translator
import sqlite3

card_desc = ['шут', 'маг', 'жрица', 'императрица', 'император', 'верховный жрец', 'влюбленные', 'колесница',
             'правосудие', 'отшельник', 'колесо фортуны', 'сила', 'повешенный', 'смерть', 'умеренность', 'дьявол',
             'башня', 'звезда', 'луна', 'солнце', 'суд']

api_key = "***************************************************" # api key from openai

token = '**********************************************' # telegram bot token

path = r'cards\card' # path to cards images

colors_array = ['красный', 'оранжевый', 'желтый', 'зеленый', 'голубой', 'синий', 'фиолетовый', 'черный', 'белый',
                'розовый', 'мультицвет', 'коричневый', 'серый']