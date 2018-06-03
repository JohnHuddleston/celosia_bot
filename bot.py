#! /usr/bin/env python3

import telepot
import time
from telepot.loop import MessageLoop
import urllib.request
import urllib.parse
import sys
import json
import psutil
import os
import requests
import re
import logging
from random import randrange

# Use the built-in Telegram bot 'Bot Father' to obtain this if you don't have one already
API_KEY = 'Place your Telegram bot API key here'

def remove_dups(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list

def decode(tokens, msg):

	# Initialize output to an empty string
	output = ''

	thank_you = ["Thanks, " + msg['from']['username'] + " ☺", "You're the best, " + msg['from']['username'] +"!", "Aw, shucks", "+1 Ego Points!", "Hell yeah, thanks fam"]

	# if-elif-else statements to catch commands

	# '!time' returns the current time for the server the bot resides on
	if tokens[0] == '!time':
		output = "It is currently *" + time.strftime("%-I:%M:%S %p") + "* EST."
		
	elif tokens[0] == '!goodbot':
		output = thank_you[randrange(0, len(thank_you) - 1)]

	elif tokens[0] in ['!yt', '!ytlucky']:
		query_string = urllib.parse.urlencode({"search_query" : ' '.join(tokens[1:])})
		html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
		search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
		if tokens[0] == '!yt':
			search_results = remove_dups(search_results)
			output = "Here are the top 3 results:\n1. " + "http://www.youtube.com/watch?v=" + search_results[0] + "\n2. " + "http://www.youtube.com/watch?v=" + search_results[1] + "\n3. " + "http://www.youtube.com/watch?v=" + search_results[2]
		else:
			output = "Here's the top hit: http://www.youtube.com/watch?v=" + search_results[0]

	# '/start' means someone just initiated a chat
	elif tokens[0] == '/start':
		output = "Oh, hi there, " + msg["from"]["username"] + "!\nFor information on what commands I offer, message me \'!help\'"

	# geolocation via IP
	elif tokens[0] == '!whereyouat':
		my_ip = json.load(urllib.request.urlopen('http://jsonip.com'))['ip']
		api = "http://freegeoip.net/json/" + my_ip
		try:
			result = urllib.request.urlopen(api).read()
			result = str(result) 
			result = result[2:len(result)-3]
			result = json.loads(result)
			output = "This bot is currently chilling in *" + result['city'] + ", " + result['region_name'] + ", " + result['country_name'] + "*."
		except e:
			logging.info("Could not find location: " + e)
			output = "Sorry, I can't figure out where I am!"

	# super simple echo
	elif tokens[0] == '!echo':
		output = ' '.join(tokens[1:])

	# gives information about the server hardware usage
	elif tokens[0] == '!serverstats':
		cpu_loads = psutil.cpu_percent(interval=3, percpu=True)
		process = psutil.Process(os.getpid())
		output = '*CPU Load*: '
		for i in range(len(cpu_loads)):
			output += '_Core ' + str(i) + "_: " + str(cpu_loads[i])
			if i < (len(cpu_loads) - 1):
				output += ", "
		output += "\n"
		memory_usage = psutil.virtual_memory()
		total_mem = memory_usage[0]/1000000000
		available_mem = memory_usage[1]/1000000000
		used_mem = total_mem - available_mem
		current_ram = process.memory_info()[0]/1000000
		output += "*Total memory*: {0:.4} GB".format(str(total_mem)) + "\n"
		output += "*Used memory*: {0:.4} GB".format(str(used_mem)) + "\n"
		output += "*Available memory*: {0:.4} GB".format(str(available_mem))
		output += "\n_This bot is currently using {0:.4} MB_".format(current_ram)

	elif tokens[0] == '!help':
		output = "Here are the commands I can currently handle for you:\n"
		output += "*{}*: {}\n".format("!echo", "I'll repeat back whatever you say!")
		output += "*{}*: {}\n".format("!goodbot", "Give me a little ego boost!")
		output += "*{}*: {}\n".format("!newpoll", "I'll set up a strawpoll for you and send back the link!  (Usage: !new poll \"poll title\" \"option 1\" \"option 2\" ... )")
		output += "*{}*: {}\n".format("!serverstats", "Find out about RAM and processor usage on my server!")
		output += "*{}*: {}\n".format("!time", "I'll let you know what time it is, in case those timestamps don't help.")
		output += "*{}*: {}\n".format("!whereyouat", "I'll figure out where I'm currently running!")
		output += "*{}*: {}\n".format("!yt", "Follow this with a search query and I'll give you the top 3 results from YouTube.")
		output += "*{}*: {}".format("!ytlucky", "Just like !yt, but I'll only return the top result.")


	elif tokens[0] == '!newpoll':
		back_to_string = ' '.join(tokens)
		input_exp = re.compile(r'"([^"]*)"')
		args = re.findall(input_exp, back_to_string)

		query = {'title': args[0], 'options': args[1:]}
		query = json.dumps(query)
		header = {'Content-Type': 'application/json'}

		response = requests.post('https://www.strawpoll.me/api/v2/polls', data=query, headers=header)

		if len(args[0]) > 25:
			title = args[0][0:21] + '...'
		else:
			title = args[0]

		if response.ok == True:
			output = "Congrats!  Your poll *{}* has been posted and can be found here: https://www.strawpoll.me/{} !".format(title, str(response.content[6:14])[2:-1])
		else:
			output = "Sorry, something went wrong, please try again later!"
		

	# once the output is constructed, we return it
	return output


def handle(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	logging.info("New Message Profile: " + content_type + ", " + chat_type + ", " + str(chat_id))

	if content_type == 'text':
		inp = msg['text']
		try:
			logging.info("Received command " + inp + " from " + msg['from']['username'])
		except KeyError:
			logging.info("Received command " + inp + " from " + str(msg['from']['id']) + " [USERNAME_NOT_SET FALLBACK]")
		tokens = inp.split(' ')

		output = decode(tokens, msg)
		avoid_markup = 0

		if tokens[0] in ['!yt', '!ytlucky']:
			avoid_markup = 1


		if 'doot' in tokens:
			bot.sendMessage(chat_id, "*D O O T    D O O T !*", parse_mode='Markdown')

		if output is not "":
			if avoid_markup == 1:
				bot.sendMessage(chat_id, output)
			else:
				bot.sendMessage(chat_id, output, parse_mode='Markdown')
			logging.info("Message sent to chat " + str(chat_id))

			

logging.basicConfig(format='%(asctime)s  %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='celosia.log', level=logging.INFO)

bot = telepot.Bot(API_KEY)
MessageLoop(bot, handle).run_as_thread()
logging.info("Bot started at " + time.strftime("%-I:%M:%S %p"))
print("Bot started.")

while True:
	time.sleep(5)
