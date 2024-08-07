#!/usr/bin/env python
# coding=utf-8
# author=XingLong Pan
# date=2016-12-06

import pymysql.cursors
import configparser
import warnings
warnings.filterwarnings("ignore")

class DbHelper:

    __connection = None

    def __init__(self):
        self.__connect_database()

    def __connect_database(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.__connection = pymysql.connect(
            host=config['mysql']['host'],
            user=config['mysql']['user'],
            port=int(config['mysql']['port']),
            password=config['mysql']['password'],
            db=config['mysql']['db_name'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)

    def insert_movie(self, movie):
        try:
            with self.__connection.cursor() as cursor:
                sql = "INSERT IGNORE INTO `movie` (`douban_id`, `title`, `directors`, " \
                      "`scriptwriters`, `actors`, `types`,`release_region`," \
                      "`release_date`,`alias`,`languages`,`duration`,`score`," \
                      "`description`,`tags`,`cover`) VALUES (%s," \
                      "%s, %s, %s, %s, %s, %s, %s," \
                      "%s, %s, %s, %s, %s, %s, %s);"
                #print(movie['cover'])
                cursor.execute(sql, (
                    movie['douban_id'],
                    movie['title'],
                    movie['directors'],
                    movie['scriptwriters'],
                    movie['actors'],
                    movie['types'],
                    movie['release_region'],
                    movie['release_date'],
                    movie['alias'],
                    movie['languages'],
                    movie['duration'],
                    movie['score'],
                    movie['description'],
                    movie['tags'],
                    movie['cover'],

                ))
                self.__connection.commit()
        except Exception as e:
               self.__connection.rollback()
        finally:
               pass

    def close_db(self):
        self.__connection.close()
