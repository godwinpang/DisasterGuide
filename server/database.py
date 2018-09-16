#!/usr/bin/env python3

import psycopg2 as pg
import datetime
from uuid import uuid4 as uuid

class Database:

    def __init__(self, host, port, db_name, username, password):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.username = username

        self.conn = pg.connect(host=self.host,
                               port=self.port,
                               dbname=self.db_name,
                               user=self.username,
                               password=password)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    def add_user(self, first_name, last_name, birthday, user_id=None):
        """
        Add user to database.
        :param first_name: a string representing the first name of the user
        :param last_name: a string representing the last name of the user
        :param birthday: a date object representing the birthday of the user (to compte the age, for medical purposes)
        :param user_id: a string representing a UUID for the user. Will be automatically generated if not provided
        :return: True if successful
        """
        if user_id is None:
            user_id = str(uuid())
        self.cur.execute('INSERT INTO users (user_id, first_name, last_name, birthday) VALUES (%s, %s, %s, %s)',
                         (user_id, first_name, last_name, birthday))
        return True

    def get_user_info(self, user_id):
        """
        Gets the age of the user specified by the user ID.
        :param user_id: a string representing the UUID of the user of interest.
        :return: a tuple of the form (first_name <str>, last_name <str>, age <int>, role <str>)
        """
        self.cur.execute('SELECT first_name, last_name, birthday, role FROM users WHERE user_id=%s', (user_id, ))
        first_name, last_name, birthday, role = self.cur.fetchall()[0][0]
        return first_name, last_name, (datetime.datetime.now() - birthday).years, role

    def log_location(self, user_id, latitude, longitude):
        """
        Insert a row into the locations table with the new location of the user.
        :param user_id: a string representing the UUID of the user of interest.
        :param latitude: the latitudinal coordinate of the user
        :param longitude: the longitudinal coordinate of the user
        :return: True if successful
        """
        location_id = str(uuid())
        self.cur.execute('INSERT INTO locations (location_id, user_id, latitude, longitude) VALUES (%s, %s, %s, %s)',
                         (location_id, user_id, latitude, longitude))
        return True

    def get_last_location(self, user_id):
        """
        Retrieve the last recorded location for a specified user in the location log.
        :param user_id: a string representing the UUID of the user of interest.
        :return: a tuple given as (latitude (float), longitude (float), date_created (datetime))
        """
        self.cur.execute(
            'SELECT latitude, longitude, date_created FROM locations WHERE user_id=%s ORDER BY date_created DESC LIMIT 1', (user_id,))
        return self.cur.fetchall()[0]

    def get_past_locations(self, user_id):
        """
        Retrieve all of the recorded locations for a specified user in the location log.
        :param user_id: a string representing the UUID of the user of interest.
        :return: a list of all tuples of (latitude (float), longitude (float), date_created (datetime)), ordered from
        most to least recent
        """
        self.cur.execute(
            'SELECT latitude, longitude, date_created FROM locations WHERE user_id=%s ORDER BY date_created DESC', (user_id,))
        return self.cur.fetchall()

    def log_help_call(self, user_id, description, watson_context, distress_status=None):
        """
        Adds a new entry to the help_log representing a message from the user. Additionally, this function adds a log
        entry to distress_log if distress_status can be inferred from the message, as set in the parameters.
        :param user_id: a string representing the UUID of the user of interest.
        :param description: a string representing a free-text description of the log entry, typically including the
        message that the user gave to the service
        :param watson_context: a JSON object representing the context information of Watson IBM
        :param distress_status: a boolean representing whether the message provided by the user invoked a setting of
        the current distress status.
        :return: True if successful
        """
        help_entry_id = str(uuid())
        distress_entry_id = str(uuid())
        self.cur.execute('INSERT INTO help_log (entry_id, user_id, description, watson_context) VALUES (%s, %s, %s, %s)',
                         (help_entry_id, user_id, description, watson_context))
        if distress_status is not None:
            self.cur.execute(
                'INSERT INTO distress_log (entry_id, user_id, help_log_id, distress_status) VALUES (%s, %s, %s, %s)',
                (distress_entry_id, user_id, help_entry_id, distress_status))
        return True

    def get_distress_status(self, user_id):
        """
        Retrieve latest distress status of specified user based on distress log.
        :param user_id: a string representing the UUID of the user of interest.
        :return: a boolean representing whether the user currently has his distress beacon active or not
        """
        self.cur.execute(
            'SELECT distress_status FROM distress_log WHERE user_id=%s ORDER BY date_created DESC LIMIT 1', (user_id,))
        return self.cur.fetchone()[0][0]