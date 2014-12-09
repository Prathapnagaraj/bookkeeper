# encoding: utf-8
""" Small database wrapper allowing install management.

This allows bookkeeper to keep track of which is installed (and where).
"""
import sqlite


class DB(object):

    """ Manages the sqlite connection. """

    _instance = None

    @classmethod
    def get_instance(cls):
        """ Singleton instance. """
        if DB._instance is None:
            DB._instance = cls()
        return DB._instance

    def __init__(self):
        """ Create sqlite connection. """
        self.connection = sqlite.connect('$HOME/.bookkeeper_db')

    def exc(self, command, *args):
        """ Wrapper for sqlite exec. """
        cursor = self.connection.cursor()
        cursor.execute(command, *args)
        cursor.commit()

    def add_item(self, app, item, item_type):
        """ Simple wrapper for inserting item. """
        self.exc(
            """ INSERT OR IGNORE INTO inner (app, object, type)
            VALUES (?, ?, ?) """,
            app, item, item_type
        )

    def add_app(self, app, source, target):
        """ Simple wrapper for inserting app. """
        self.exc(
            """ INSERT OR IGNORE INTO app (app, source_path, target_path)
            VALUES (?, ?, ?) """,
            app, source, target
        )


def install():
    """ Create basic db. """
    db = DB.get_instance()

    db.exc("""CREATE TABLE apps
    (app text, source_path text, target_path text)
    UNIQUE (app, source_path, target_path)
    """)
    db.exc("""CREATE TABLE inner
    (app text, object text, type text)
    UNIQUE (app, object, type)
    """)
