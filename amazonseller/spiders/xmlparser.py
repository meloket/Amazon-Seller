# -*- coding: utf-8 -*-
import scrapy
import requests
import time
import json
import os
import multiprocessing
import random
import sys
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from lxml import html
from w3lib.html import remove_tags
import unicodedata
from scrapy.http import HtmlResponse
from scrapy.http import TextResponse
from datetime import datetime

from amazonseller.items import AmazonsellerItem
import Tkinter
import tkMessageBox
 



class XmlparserSpider(scrapy.Spider):
    name = 'xmlparser'
    domain = ''
    hflag = 'no'
    items = []
    # allowed_urls = ['https://www.sellercentral.amazon.com']
	# start_urls = ['https://www.amazon.com/products/dress']

    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["OrderID", "Ship Name", "Ship Street", "Ship City", "Ship State", "Ship ZipCode", "Ship OrderDate", "SKU", "Personalization", "Repersonalization"],
    }

    current_orderID = ''
    current_address_ship_name = ''
    current_address_ship_street = ''
    current_address_ship_city = ''
    current_address_ship_state = ''
    current_address_ship_zipcode = ''
    current_orderDate = ''
    current_sku = ''
    current_personalization = ''
    current_repersonalization = ''




    def __init__(self):

        # script_dir = os.path.dirname(__file__)
        # chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--window-size=1920x1080")
        # self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
        # self.driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
        with open('C:\CSV\APP\data.csv', 'wb') as csvfile:
            fieldnames = ["PCAOrder", "CustName", "CustRef1", "CustRef2", "CustStreet", "CustCity", "CustState", "CustZip", "ShipName", "ShipRef1", "ShipRef2", "ShipStreet", "ShipCity", "ShipState", "ShipZip", "Item", "Qty", "ItemDescription", "Name", "Item1", "Qty1", "ItemDescription1", "Name1", "Item2", "Qty2", "ItemDescription2", "Name2", "Item3", "Qty3" ,"ItemDescription3", "Name3", "Item4", "Qty4", "ItemDescription4", "Name4", "Item5", "Qty5", "ItemDescription5", "Name5", "Item6", "Qty6", "ItemDescription6", "Name6", "Item7", "Qty7", "ItemDescription7", "Name7", "Date", "POBox", "PCItemNo", "Place", "Phone"]
            # fieldnames = ["OrderID", "Shipping_Name", "Shipping_Street", "Shipping_City", "Shipping_State", "Shipping_ZipCode", "Shipping_OrderDate", "SKU", "Personalization", "Repersonalization"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
            writer.writeheader()
            csvfile.close()

        chrome_driver = "amazonseller/chromedriver/chromedriver.exe"
        self.driver = webdriver.Chrome(chrome_driver)


    def start_requests(self):
        init_url = 'http://sellercentral.amazon.com'
        # init_url = 'http://localhost/emulatedurl/manage.html'
        self.driver.get(init_url)
        response0 = HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
        self.parse(response0)
        # yield scrapy.Request(url=self.driver.current_url, callback=self.body)


    def parse(self, response):
        
        self.driver.find_element_by_id('sign-in-button').click()
        
        # # # # *************** Log in ********************************
        
        self.driver.find_element_by_id('ap_email').send_keys('xx@xx.com')
        self.driver.find_element_by_id("ap_password").send_keys('asdfe')
        form = self.driver.find_element_by_name("signIn")
        form.submit()
        time.sleep(90)

        # # *************** Goto Manage Order Page  ***************
        self.driver.get("https://sellercentral.amazon.com/gp/orders-v2/list/ref=ag_myo_dnav_xx_")
        # self.driver.get('http://localhost/emulatedurl/manage.html')


        # # ***************** Last 3 Days Select and Click Search Button ******************
        # select_3dy = Select(self.driver.find_element_by_id('_myoLO_preSelectedRangeSelect'))
        # select_3dy.select_by_visible_text('Last 3 days')
        # self.driver.find_element_by_id('SearchID').click()
        time.sleep(5)

        # # ***************** Set 50 Show and Click Go Button ******************
        # select_50go = Select(self.driver.find_element_by_xpath('//div[@id="myo-table"]/table/tbody/tr/td/form/table/tbody/tr/td[2]/select'))
        # select_50go.select_by_visible_text('50')
        # form_show = self.driver.find_element_by_xpath("//form[contains(@class, 'myo_list_orders_search_form')]")
        # form_show.submit()
        # time.sleep(5)


        # source = self.driver.page_source.encode("utf8")
        # maintree = etree.HTML(source)
        # print(str(maintree))

        response2 = HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')



        # # ***************** Get Printing Page Request URL *******************/orders/packing-slip?orderIds=
        printing_url = "https://sellercentral.amazon.com/orders/packing-slip?orderIds="
        # orderIDs = response2.xpath('//div[@id="myo-table"]/table/tbody/tr/td/a/strong/text()').extract()

        orderIDs = response2.xpath("//tr/td[3]/div[contains(@class, 'cell-body')]/div[contains(@class, 'cell-body-title')]/a/text()").extract()

        for orderID in orderIDs:
            printing_url += orderID +";"
            print("\n " + orderID)
        
        print("\n SSSSSSSSSSSSSS:   " + printing_url + "\n")

        # #***************** Get Printing Page ******************************
        # printing_url = "http://localhost/emulatedurl/Amazon_fix.html"




        self.driver.get(printing_url)

        response1 = HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')

        self.get_page_block(response1)
        # yield scrapy.Request(url=printing_url, callback=self.get_page_block)




        # # # ***************** Select Print packing slip item and CheckBox then Click Go Button ******************
        # select_print_slip = Select(self.driver.find_element_by_xpath('//div[@id="myo-table"]/table/tbody/tr[2]/td/select'))
        # select_print_slip.select_by_visible_text('Print packing slips for selected orders')
        # self.driver.find_element_by_xpath('//div[@id="myo-table"]/table/tbody/tr[3]/td[1]/input[contains(@class, "checkall")]').click()
        # self.driver.find_element_by_xpath('//div[@id="myo-table"]/table/tbody/tr[2]/td/span[contains(@class, "action-go")]').click()
        # time.sleep(1)

        # source = self.driver.page_source.encode("utf8")
        # tree = etree.HTML(source)

        # print(str(source))

        # blocks = tree.xpath('//table/tbody//tr')


        # source = self.driver.page_source.encode("utf8")
        # tree = etree.HTML(source)
        # store_list = tree.xpath('//section//div[contains(@class, "stores")]//a[2]/@href')
        # for store in store_list:
        #     yield scrapy.Request(url=store, callback=self.parse_page)

    
    def get_page_block(self, response1):
        page_blocks = response1.xpath('//div[@id="myo-packing-slips"]/div').extract()
        for page_block in page_blocks:
            self.get_product_block(html.fromstring(page_block))
        # self.get_product_block(html.fromstring(page_blocks[0]))
        tkMessageBox.showinfo("Result", "End!")
        self.driver.close()
        os._exit

    def get_product_block(self, pageblock):
# #ORDER ID 
        string_orderID = pageblock.xpath("//div[contains(@class, 'a-section myo-orderId')]/text()")[0].strip().split(":")[1].strip()
        global current_orderID
        current_orderID = string_orderID
        # print("\n AAAAAAAA: " + string_orderID)
# #SHIPPING INFORMATION
    #ADDRESS
        shipAddress_name = pageblock.xpath("//div[contains(@class, 'a-section a-spacing-none a-spacing-top-micro a-padding-none')]//span[@id='myo-order-details-buyer-address']/text()")[0].strip()
        shipAddress_street = pageblock.xpath("//div[contains(@class, 'a-section a-spacing-none a-spacing-top-micro a-padding-none')]//span[@id='myo-order-details-buyer-address']/text()")[1].strip()
        shipAddress_city = pageblock.xpath("//div[contains(@class, 'a-section a-spacing-none a-spacing-top-micro a-padding-none')]//span[@id='myo-order-details-buyer-address']/text()")[2].strip().split(',')[0]
        shipAddress_state = pageblock.xpath("//div[contains(@class, 'a-section a-spacing-none a-spacing-top-micro a-padding-none')]//span[@id='myo-order-details-buyer-address']/text()")[3].strip()
        shipAddress_zipcode = pageblock.xpath("//div[contains(@class, 'a-section a-spacing-none a-spacing-top-micro a-padding-none')]//span[@id='myo-order-details-buyer-address']/text()")[4].strip()
        
        global current_address_ship_name, current_address_ship_street, current_address_ship_city, current_address_ship_state, current_address_ship_zipcode
        current_address_ship_name = shipAddress_name
        current_address_ship_street = shipAddress_street
        current_address_ship_city = shipAddress_city
        current_address_ship_state = shipAddress_state
        current_address_ship_zipcode = shipAddress_zipcode
        # print("\n BBBBBBBBB: " + shipAddress_name + " : " + shipAddress_street + " : " + shipAddress_city + " : " + shipAddress_state + " : " + shipAddress_zipcode)
    # #ORDER DATE
        string_orderDate = pageblock.xpath("//div[contains(@class, 'a-column a-span8 a-span-last')]/div[contains(@class, 'a-section a-spacing-none a-spacing-top-micro a-padding-none')][1]/span/text()")[0].strip()
        cstrdate = datetime.strptime(string_orderDate, '%a, %b %d, %Y')
        outdate = datetime.strftime(cstrdate, '%m/%d/%Y')
        global current_orderDate
        current_orderDate = outdate
        # print("\n CCCCCCCCC: " + string_orderDate)
    # #INFO BLOCK
        info_blocks = pageblock.xpath("//table[contains(@class, 'a-normal a-spacing-none a-spacing-top-small table-border')]/tbody/tr")
        item_count = 2
        print("KSSSSSSSSSSSSSSSSSSSSSSSSSSSS:   " + str(len(info_blocks)))

        len_b = len(info_blocks)
        if len_b == 0:
            # info_block = pageblock.xpath("//table[contains(@class, 'a-normal a-spacing-none a-spacing-top-small table-border')]/tbody/tr")
            self.get_item_block(pageblock, item_count)
        else:
            del info_blocks[0]
            for info_block in info_blocks:
                self.get_item_block(info_block, item_count)
                item_count +=1

#PRODUCT DETAIL (*******  NEEDS LOOPING COURSE  ********)


    def get_item_block(self, infoblock, itemcount):
    #QTY
        string_qty = infoblock.xpath("//tr["+str(itemcount)+"]/td[contains(@class, 'a-text-center table-border')][1]/text()")[0].strip()
        # print("QQQQQQQQQQQQTTTTTTTTYYYYYYYYYYY:  " + string_qty)
    #SKU
        string_sku = infoblock.xpath("//tr["+str(itemcount)+"]/td[contains(@class, 'a-text-left table-border')]/div[contains(@class, 'a-row')][1]/span[2]/text()")[0].strip()
        global current_sku
        current_sku = string_sku
        # print("BBBBBBBBBBBBBBB: "+string_sku)
    #Personalization
        string_personalization = infoblock.xpath("//tr["+str(itemcount)+"]/td[contains(@class, 'a-text-left table-border')]/div[contains(@class, 'a-section a-spacing-none a-padding-none')]/ul[contains(@class, 'a-unordered-list a-nostyle a-vertical')]/li[1]/span[contains(@class, 'a-list-item')]/span[2]/text()")[0]
        global current_personalization
        current_personalization = string_personalization
        # print("BBBBBBBBBBBBBBB: "+string_personalization)//li[2]/span[contains(@class, 'a-list-item')]/span[2]
        

        try:
            string_personalization = infoblock.xpath("//tr["+str(itemcount)+"]/td[contains(@class, 'a-text-left table-border')]/div[contains(@class, 'a-section a-spacing-none a-padding-none')]/ul[contains(@class, 'a-unordered-list a-nostyle a-vertical')]/li[1]/span[contains(@class, 'a-list-item')]/span[2]/text()")[0]
            global current_personalization
            current_personalization = string_personalization
            # print("BBBBBBBBBBBBBBB: "+string_personalization)//li[2]/span[contains(@class, 'a-list-item')]/span[2]
            pass
        except Exception as e:
            string_personalization = infoblock.xpath("//tr["+str(itemcount)+"]/td[contains(@class, 'a-text-left table-border')]/div[contains(@class, 'a-section a-spacing-none a-padding-none')]/ul[contains(@class, 'a-unordered-list a-nostyle a-vertical')]/li/text()")[0]
            global current_personalization
            current_personalization = string_personalization
            # print("BBBBBBBBBBBBBBB: "+string_personalization)//li[2]/span[contains(@class, 'a-list-item')]/span[2]
            pass

    # #RePersonalization
    #     string_repersonalization = infoblock.xpath("//tr["+str(itemcount)+"]/td[contains(@class, 'a-text-left table-border')]/div[contains(@class, 'a-section a-spacing-none a-padding-none')]/ul[contains(@class, 'a-unordered-list a-nostyle a-vertical')]/li[2]/span[contains(@class, 'a-list-item')]/span[2]/text()")[0]
    #     global current_repersonalization
    #     current_repersonalization = string_repersonalization
    #     # print("BBBBBBBBBBBBBBB: "+string_repersonalization)
    #     # global all_item_count = all_item_count + 1

        print("\n  CURRENT: "+ current_orderID + " : "+current_address_ship_name + " : " + current_address_ship_street + " : " + current_address_ship_city + " : " + current_address_ship_state + " : " + current_address_ship_zipcode + " : " + current_sku + " : " + current_orderDate + " : " + current_personalization + " : " + "current_repersonalization")

        time.sleep(1)
        item = AmazonsellerItem()
        item['PCAOrder'] = current_orderID
        item['CustName'] = current_address_ship_name
        item['CustRef1'] = current_address_ship_street
        item['CustRef2'] = ""
        item['CustStreet'] = ""
        item['CustCity'] = current_address_ship_city
        item['CustState'] = current_address_ship_state
        item['CustZip'] = current_address_ship_zipcode
        item['ShipName'] = current_address_ship_name
        item['ShipRef1'] = ""
        item['ShipRef2'] = ""
        item['ShipStreet'] = current_address_ship_street
        item['ShipCity'] = current_address_ship_city
        item['ShipState'] = current_address_ship_state
        item['ShipZip'] = current_address_ship_zipcode
        item['Item'] = current_sku
        item['Qty'] = string_qty
        item['ItemDescription'] = ""
        item['Name'] = current_personalization
        item['Item1'] = ""
        item['Qty1'] = ""
        item['ItemDescription1'] = ""
        item['Name1'] = ""
        item['Item2'] = ""
        item['Qty2'] = ""
        item['ItemDescription2'] = ""
        item['Name2'] = ""
        item['Item3'] = ""
        item['Qty3'] = ""
        item['ItemDescription3'] = ""
        item['Name3'] = ""
        item['Item4'] = ""
        item['Qty4'] = ""
        item['ItemDescription4'] = ""
        item['Name4'] = ""
        item['Item5'] = ""
        item['Qty5'] = ""
        item['ItemDescription5'] = ""
        item['Name5'] = ""
        item['Item6'] = ""
        item['Qty6'] = ""
        item['ItemDescription6'] = ""
        item['Name6'] = ""
        item['Item7'] = ""
        item['Qty7'] = ""
        item['ItemDescription7'] = ""
        item['Name7'] = ""
        item['Date'] = current_orderDate
        item['POBox'] = ""
        item['PCItemNo'] = ""
        item['Place'] = ""
        item['Phone'] = ""

        # item['Shipping_OrderDate'] = current_orderDate
        # # item['SKU'] = current_sku
        # item['Personalization'] = current_personalization
        # item['Repersonalization'] = current_repersonalization

        # yield item
        # global items
        # items.append(item)
        

        with open('C:\CSV\APP\data.csv', 'a') as csvfile:
            # fieldnames = ["OrderID", "Shipping_Name", "Shipping_Street", "Shipping_City", "Shipping_State", "Shipping_ZipCode", "Shipping_OrderDate", "SKU", "Personalization", "Repersonalization"]
            fieldnames = ["PCAOrder", "CustName", "CustRef1", "CustRef2", "CustStreet", "CustCity", "CustState", "CustZip", "ShipName", "ShipRef1", "ShipRef2", "ShipStreet", "ShipCity", "ShipState", "ShipZip", "Item", "Qty", "ItemDescription", "Name", "Item1", "Qty1", "ItemDescription1", "Name1", "Item2", "Qty2", "ItemDescription2", "Name2", "Item3", "Qty3" ,"ItemDescription3", "Name3", "Item4", "Qty4", "ItemDescription4", "Name4", "Item5", "Qty5", "ItemDescription5", "Name5", "Item6", "Qty6", "ItemDescription6", "Name6", "Item7", "Qty7", "ItemDescription7", "Name7", "Date", "POBox", "PCItemNo", "Place", "Phone"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
            writer.writerow(item)
            csvfile.close()
        # global hflag
        # if hflag == 'no':
        #     writer.writeheader()
        # else:
        #     writer.writerow(item)
            # writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
            # writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})

        # print(str(item))
        
        pass

        # fields = ["OrderID", "Shipping_Name", "Shipping_Street", "Shipping_City", "Shipping_State", "Shipping_ZipCode", "Shipping_OrderDate", "SKU", "Personalization", "Repersonalization"] # define fields to use
        # with open('hi.csv','a+') as f: # handle the source file
        #     # f.write("{}\n".format('\t'.join(str(field) 
        #     #                         for field in fields))) # write header 
        #     # for item in items:
        #     f.write("{}\n".format('\t'.join(str(item[field]) 
        #                             for field in fields))) # write items
        # file = open('%s_%s.csv' % (spider.name, datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d')), 'w+b')

#     def parse(self, response):

#         # start_urls = ['http://localhost/emulatedurl/amazon.html']

#         # headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
#         # page = requests.get("http://localhost/emulatedurl/amazon.html")
#         page = requests.get("http://localhost/emulatedurl/index.htm")
#         # print(page)
#         #main_title = response.css('attr(title)')
#         #main_price = response.css('.main-price::text').extract()

#         # main_image = response.css("img::attr(data-img)").extract()



#         sitems1 = response.xpath('//table/tbody//td[1]/text()').extract()
#         sitems2 = response.xpath('//table/tbody//td[2]/text()').extract()
#         sitems3 = response.xpath('//table/tbody//td[3]/text()').extract()
#         sitems4 = response.xpath('//table/tbody//td[4]/text()').extract()
        
#         # print(self.format(items[0].strip()))


#         for sitem1 in sitems1:
#             item = AmazonsellerItem()
#             item['num'] = sitem1

#             # print(my_item)
#             yield item

#         for sitem2 in sitems2:
#             item = AmazonsellerItem()
#             item['type_'] = sitem2

#             # print(my_item)
#             yield item
#         # print(items)





# #ORDER ID 
#         string_orderID = response.xpath('//div[@class="a-section myo-orderId"]/text()').extract()
#         # print(test_block)

# #BUYER INFORMATION
#     #ADDRESS
#         buyerAddress_block = response.xpath('//span[@id="myo-order-details-buyer-address"]').extract()
#         buyerAddress_1 = remove_tags(self.format(buyerAddress_block[0]))
#         buyerAddress = buyerAddress_1.replace('\n','').strip().replace('  ',' ').strip()
#         # print(buyerAddress)
#     # ORDER DATE
#         string_orderDate = response.xpath('//div[@id="myo-packing-slip-0"]/div[4]/div/div[2]/div/div[2]/div[1]/span/text()').extract()
#         # print(string_orderDate[0])

# #PRODUCT DETAIL (*******  NEEDS LOOPING COURSE  ********)
#     #SKU
#         pre_sku = response.xpath('//div[@id="myo-packing-slip-0"]/table/tbody/tr[2]/td[2]/div[1]/span[2]/text()').extract()
#         string_SKU = pre_sku[0].replace('\n','').strip()
#         # print(string_SKU)
#     #Personalization
#         pre_personalization = response.xpath('//div[@id="myo-packing-slip-0"]/table/tbody/tr[2]/td[2]/div[6]/ul/li[1]/span/span[2]/text()').extract()
#         string_personalization = pre_personalization[0].replace('\n','').strip()
#         # print(string_personalization)

#     #RePersonalization
#         pre_repersonalization = response.xpath('//div[@id="myo-packing-slip-0"]/table/tbody/tr[2]/td[2]/div[6]/ul/li[2]/span/span[2]/text()').extract()
#         string_repersonalization = pre_repersonalization[0].replace('\n','').strip()
#         # print(string_repersonalization)

#         # test_string = response.selector.xpath("//span").extract()
#         # print(test_string)

#         # #Give the extracted content row wise
#         # for item in zip(main_image):
#         #     #create a dictionary to store the scraped info
#         #     scraped_info = {
#         #         'MainImage' : item[0],
#         #     }

#         #     #yield or give the scraped info to scrapy
#         #     yield scraped_info

#         pass

    
#     def format(self, item):
#             try:
#                 return unicodedata.normalize('NFKD', item).encode('ascii','ignore').strip()
#             except:
#                 return ''











# from __future__ import unicode_literals
# import scrapy
# import json
# import os
# from scrapy.spiders import Spider
# from scrapy.http import FormRequest
# from scrapy.http import Request
# from chainxy.items import ChainItem
# from lxml import etree
# from selenium import webdriver
# from lxml import html
# # import usaddress
# import pdb

# class todo2(scrapy.Spider):
# 	name = 'todo2'
# 	domain = ''
# 	history = []

# 	def __init__(self):
# 		self.driver = webdriver.Chrome("./chromedriver")
# 		script_dir = os.path.dirname(__file__)
# 		file_path = script_dir + '/geo/US_States.json'
# 		with open(file_path) as data_file:    
# 			self.location_list = json.load(data_file)

# 	def start_requests(self):
# 		init_url = ''
# 		yield scrapy.Request(url=init_url, callback=self.body)
	
# 	def body(self, response):
# 		self.driver.get("http://www.factory-connection.com/find-a-store")
# 		self.driver.find_element_by_id('state').send_keys('state')
# 		self.driver.find_element_by_xpath('//button').click()
# 		source = self.driver.page_source.encode("utf8")
# 		tree = etree.HTML(source)
# 		store_list = tree.xpath('//section//div[contains(@class, "stores")]//a[2]/@href')
# 		for store in store_list:
# 			yield scrapy.Request(url=store, callback=self.parse_page)

# 	def parse_page(self, response):
# 		try:
# 			item = ChainItem()
# 			detail = self.eliminate_space(response.xpath('//div[contains(@class, "address")]//text()').extract())
# 			item['store_name'] = ''
# 			item['store_number'] = ''
# 			item['address'] = self.validate(detail[0])
# 			addr = detail[1].split(',')
# 			item['city'] = self.validate(addr[0].strip())
# 			sz = addr[1].strip().split(' ')
# 			item['state'] = ''
# 			item['zip_code'] = self.validate(sz[len(sz)-1])
# 			for temp in sz[:-1]:
# 				item['state'] += self.validate(temp) + ' '
# 			item['phone_number'] = detail[2]
# 			item['country'] = 'United States'
# 			h_temp = ''
# 			hour_list = self.eliminate_space(response.xpath('//div[contains(@class, "hours")]//text()').extract())
# 			cnt = 1
# 			for hour in hour_list:
# 				h_temp += hour
# 				if cnt % 2 == 0:
# 					h_temp += ', '
# 				else:
# 					h_temp += ' '
# 				cnt += 1
# 			item['store_hours'] = h_temp[:-2]
# 			yield item	
# 		except:
# 			pdb.set_trace()		

# 	def validate(self, item):
# 		try:
# 			return item.strip()
# 		except:
# 			return ''

# 	def eliminate_space(self, items):
# 		tmp = []
# 		for item in items:
# 			if self.validate(item) != '' and 'STORE HOURS:' not in self.validate(item):
# 				tmp.append(self.validate(item))
# 		return tmp
