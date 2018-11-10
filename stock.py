import requests
from bs4 import BeautifulSoup

import pandas as pd
import numpy as np
import pandas_datareader.data as web
from datetime import datetime

import pygal
from pygal.style import DarkStyle

import re

#import sent #other file

class stock:
	def __init__(self,name):
		self.name=name
		
	def getName(self):
		url=requests.get('http://quotes.wsj.com/'+self.name+'/financials/annual/income-statement')
		dom=BeautifulSoup(url.content, "html.parser")
		data=dom.find('h1')
		while True:
			try:
				tik=data.find('span',{'class':'tickerName'}).text
				co=data.find('span',{'class':'companyName'}).text
				ex=data.find('span',{'class':'exchangeName'}).text.replace('(','').replace(')','')
			except AttributeError:
				#print "Retrying..."
				#pass
				continue
			return tik+' '+co+' '+' '+ex
		#data=dom.find('div',{'class','cr_quotesHeader'})
		#print data
		#name=data.find('span').text
		#print name
		#name=re.sub('[()]','',name).#remove parentheses
		#return name
	
	def getPrices(self):
		url=requests.get('http://quotes.wsj.com/'+self.name+'/financials/annual/income-statement')
		page=BeautifulSoup(url.content, "html.parser")
		array=[]
		while True:
			try:
				array.append(float(page.find(id='quote_val').text.replace(',','')))
				array.append(page.find('li',{'class':'crinfo_diff'}).text)
				array.append(page.find_all('span',{'class':'data_data'})[5].text)
			except AttributeError:
				#print "...Retrying"
				continue
				#pass
			return array
		#array.append())#round it?
		#array.append()
		#array.append()
		#return [1,2,3]
		#return array
		
		#gathers financial data as of most recent quarter(s)
	def getFin(self):
		#income statement data
		url=requests.get('http://quotes.wsj.com/'+self.name+'/financials/quarter/income-statement')
		incPage=BeautifulSoup(url.content, "html.parser")
		#data=dom.find_all('tbody')[1].find_all('td')
		#data=dom.find('table',{'class':'cr_dataTable'}).find_all('td')
		data=incPage.find('td',string='EPS (Basic)').find_next_siblings("td")
		eps=0
		#check for negative values
		for k in data[:4]:
			if '(' in k.text:
				eps=eps+-1*float(re.sub('[\(\)]','',k.text))
			else:
				eps=eps+float(k.text)
		eps=round(eps,2)
		price=incPage.find_all('span',{'class':'data_data'})[5].text.replace(',','')
		shares=incPage.find('td',string='Basic Shares Outstanding').find_next_siblings("td")[0].text.replace(',','')
		format=incPage.find('th',{'class':'fiscalYr'}).text
		if "Thousands" in format:
			shares=float(shares)*1000
		else:
			shares=float(shares)*1000000
		
		mCap=float(price)*shares
		if mCap < 1000000000:
			CAP=str(int(mCap/1000000))+"M"
		else:
			CAP=str(int(mCap)/1000000000)+"B"
		pe=round((float(price)/float(eps)),2)
		if pe<0:
			pe='NEG'
		
		#balance sheet data
		url2=requests.get('http://quotes.wsj.com/'+self.name+'/financials/quarter/balance-sheet')
		balPage=BeautifulSoup(url2.content, "html.parser")	
		liab=balPage.find('td',string='Total Liabilities').find_next_sibling("td").text.replace(',','')
		equity=balPage.find('td',string='Total Equity').find_next_sibling("td").text.replace(',','')#negative equity .. remove parathenses ?
		form=balPage.find('th',{'class':'fiscalYr'}).text
		if "Thousands" in form:
			equity=float(equity)*1000
			liab=float(liab)*1000
		else:
			equity=float(equity)*1000000
			liab=float(liab)*1000000
		de=round(liab/equity,2)		
		pb=round((float(price)/(equity/shares)),2)
		array=[CAP,eps,pe,de,pb]
		#print array
		return array
		
	def getComp(self):
		url=requests.get('http://quotes.wsj.com/'+self.name)
		fPage=BeautifulSoup(url.content, "html.parser")
		tik=fPage.find(id='cr_competitors_table').find_all('h5')
		name=fPage.find(id='cr_competitors_table').find_all('h4')
		
		array=[]
		#test=[]
		for i in range(0,len(tik))[:3]:	#first 3 counts in range
			array.append([tik[i].text,name[i].text])	#append ( array+array ) = 2d array/list
		'''
		for i in tik[:3]:
			array.append(i.text)
		'''
		return array