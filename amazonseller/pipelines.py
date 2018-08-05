

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AmazonsellerPipeline(object):
	
	def open_spider(self, spider):
		# open csv file
		self.fp = open("data.csv", "wb")

		# write header in csv file
		self.fp.write('"OrderID","Ship Name","Ship Street","Ship City","Ship State","Ship ZipCode","Ship OrderDate","SKU","Personalization","Repersonalization"\n')

	def close_spider(self, spider):
		self.fp.close()

	def process_item(self, item, spider):
		line = '"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s"\n' % (item['OrderID'], item['Shipping_Name'], item['Shipping_Street'], item['Shipping_City'], item['Shipping_State'], item['Shipping_ZipCode'], item['Shipping_OrderDate'], item['SKU'], item['Personalization'], item['Repersonalization'])

		# encode data string with utf8 and save it into file
		self.fp.write(line.encode("utf8"))

		return item

	def filter(self, raw_str):

		res = raw_str.replace(",", " ")
		res = res.replace("\"", " ")

		return res