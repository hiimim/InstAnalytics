#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from datetime import datetime
import json, time, os, re



# List of users
users = ['yotta_life']



# ----------------------------------------
#  InstAnalytics function
# ----------------------------------------

def InstAnalytics():

	# Launch browser
	browser = webdriver.PhantomJS(desired_capabilities=dcap)

	for user in users:

		# Load JSON
		with open('data/InstAnalytics.json') as iaFile:
			iaDictionary = json.load(iaFile)

		# Backup JSON
		with open('data/InstAnalytics_backup.json', 'w') as iaFile:
			json.dump(iaDictionary, iaFile, indent=4)

		# User's profile
		browser.get('https://instagram.com/' + user)
		time.sleep(0.5)

		# Soup
		soup = BeautifulSoup(browser.page_source, 'html.parser')

		# User's statistics
		postsT     = soup.find('span', {'class': re.compile(r'.*PostsStatistic__count.*')}).contents[0]
		followersT = soup.find('span', {'class': re.compile(r'.*FollowedByStatistic__count.*')}).contents[0]
		followingT = soup.find('span', {'class': re.compile(r'.*FollowsStatistic__count.*')}).contents[0]

		# Remove all non-numeric characters
		posts     = int(re.sub('[^0-9]', '', postsT))
		followers = int(re.sub('[^0-9]', '', followersT))
		following = int(re.sub('[^0-9]', '', followingT))

		# Convert k to thousands and m to millions
		if 'k' in postsT: 	  posts     = posts     * 1000
		if 'k' in followersT: followers = followers * 1000
		if 'k' in followingT: following = following * 1000
		if 'm' in postsT: 	  posts     = posts     * 1000000
		if 'm' in followersT: followers = followers * 1000000
		if 'm' in followingT: following = following * 1000000

		if posts > 12:
			# Click the 'Load more' button
			browser.find_element_by_xpath('//a[contains(@href, "max")]').click()

		if posts > 24:
			# Load more by scrolling to the bottom of the page
			for i in range (0, (posts-24)//12):
				browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
				time.sleep(0.1)
				browser.execute_script('window.scrollTo(0, 0)')
				time.sleep(0.5)

		browser.execute_script('window.scrollTo(0, 0)')

		# Soup
		soup = BeautifulSoup(browser.page_source, 'html.parser')

		# User's photos statistics
		photosDic = []
		pLikesT = 0
		for link in soup.find('div', attrs={'data-reactid': re.compile(r'.*\bmostRecentSection\b.*')}).div.findAll('a'):
			# Photo Id
			pId = link['href'].split("/")[2]
			# Hover over a photo reveals Likes & Comments
			time.sleep(0.2)
			photo = browser.find_element_by_xpath('//a[contains(@href, "' + pId + '")]')
			time.sleep(0.2)
			ActionChains(browser).move_to_element(photo).perform()
			# Soup
			soup = BeautifulSoup(browser.page_source, 'html.parser')
			# Likes
			pLikes = int(re.sub('[^0-9]', '', soup.find('li', {'class': re.compile(r'.*__statsLikes.*')}).findAll('span')[1].contents[0]))
			# Comments
			pComments = int(re.sub('[^0-9]', '', soup.find('li', {'class': re.compile(r'.*__statsComments.*')}).findAll('span')[1].contents[0]))
			# Photo dictionary
			photoDic = {
				'pId': pId,
				'pLikes': pLikes,
				'pComments': pComments
			}
			photosDic.append(photoDic)
			# Total likes
			pLikesT += pLikes

		# Dictionary
		userDic = {
			'username': user,
			'date': datetime.now().strftime(timeFormat),
			'data': {
				'posts': posts,
				'followers': followers,
				'following': following,
				'pLikesT': pLikesT,
				'photos': photosDic
			}
		}

		# Add data to JSON
		iaDictionary.append(userDic)
		with open('data/InstAnalytics.json', 'w') as iaFile:
			json.dump(iaDictionary, iaFile, indent=4)

		print '|', user

	# Quit browser
	browser.quit()

	# Remove ghostdriver.log
	os.remove('ghostdriver.log')


