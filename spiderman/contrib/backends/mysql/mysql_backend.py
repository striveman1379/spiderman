from spiderman.contrib.backends.backend import BaseBackend
from scrapy.utils.misc import load_object

MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'database1'
MYSQL_USER = 'root'
MYSQL_PASSWD = '123456'
MYSQL_TBNAME = 'table1'

class MySqlBackend(BaseBackend):

    def create_database(self):
        pass

    pass





import scrapy
import pymysql

class MovieItem(scrapy.Item):
    # 电影名字
    name = scrapy.Field()
    # 电影信息
    info = scrapy.Field()
    # 评分
    rating = scrapy.Field()
    # 评论人数
    num = scrapy.Field()
    # 经典语句
    quote = scrapy.Field()
    # 电影图片
    img_url = scrapy.Field()



'''
create database douban DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
use douban;
CREATE TABLE doubanmovie (
    name VARCHAR(100) NOT NULL, # 电影名字
    info VARCHAR(150), # 电影信息
    rating VARCHAR(10), # 评分
    num VARCHAR(10), # 评论人数
    quote VARCHAR(100), # 经典语句
    img_url VARCHAR(100), # 电影图片
) 
'''

if __name__ == '__main__':
    connect = pymysql.connect(
        user='root',
        password='123456',
        host='127.0.01',
        port=3306,
        db='MYSQL',
        charset='utf8'
    )

    connect_cursor = connect.cursor()

    command = 'drop database if exists %s' % MYSQL_DATABASE_NAME
    connect_cursor.execute(command)

    item = MovieItem(name='name',info='info',rating=1,num=20,quote='quote',img_url='url')
    format = 'insert into'
    tabletitle = 'doubanmovie' + '('
    tablevalue = 'value ('
    for key in item.fields:
        tabletitle += (key + ',')
        tablevalue += (str(item[key]) + ',')

    tabletitle = tabletitle[:-1]+')'
    tablevalue = tablevalue[:-1]+')'

        # """insert into doubanmovie(name, info, rating, num ,quote, img_url)
        #                 value (%s, %s, %s, %s, %s, %s)""",
        # (item['name'],
        #  item['info'],
        #  item['rating'],
        #  item['num'],
        #  item['quote'],
        #  item['img_url']))
    print(format)
    print(tabletitle)
    print(tablevalue)
    pass