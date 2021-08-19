from peewee import *
import logging

from model import *

def file_exists(m, filepath):
    try:
        query = (m
                    .select()
                    .where(m.filepath == filepath)
                )
        return query.exists()
    except Exception as e:
        logging.error(e)
        return False