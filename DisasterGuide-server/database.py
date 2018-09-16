#!/usr/bin/env python3

import psycopg2 as pg
import datetime
from dateutil.relativedelta import relativedelta
from uuid import uuid4 as uuid
import json

class Database:

    NULL_UUID = "00000000-0000-0000-0000-000000000000"

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

    def add_user(self, first_name, last_name, birthday, role, user_id=None):
        """
        Add user to database.
        :param first_name: a string representing the first name of the user
        :param last_name: a string representing the last name of the user
        :param birthday: a date object representing the birthday of the user (to compte the age, for medical purposes)
        :param user_id: a string representing a UUID for the user. Will be automatically generated if not provided
        :return: a string representing the UUID of the user
        """
        if user_id is None:
            user_id = str(uuid())
        self.cur.execute('INSERT INTO users (user_id, first_name, last_name, birthday, role) VALUES (%s, %s, %s, %s, %s)',
                         (user_id, first_name, last_name, birthday, role))
        return user_id

    def get_user_info(self, user_id):
        """
        Gets the age of the user specified by the user ID.
        :param user_id: a string representing the UUID of the user of interest.
        :return: a tuple of the form (first_name <str>, last_name <str>, age <int>, role <str>)
        """
        self.cur.execute('SELECT first_name, last_name, birthday, role FROM users WHERE user_id=%s', (user_id, ))
        result = self.cur.fetchall()
        first_name, last_name, birthday, role = result[0]
        return first_name, last_name, relativedelta(datetime.datetime.now().date(), birthday).years, role

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
        return self.cur.fetchone()

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

    def get_all_users(self):
        """
        Retrieve all of the recorded locations for a specified user in the location log.
        :param user_id: a string representing the UUID of the user of interest.
        :return: a list of all tuples of (latitude (float), longitude (float), date_created (datetime)), ordered from
        most to least recent
        """
        self.cur.execute(
            'SELECT DISTINCT ON (locations.user_id) locations.user_id, first_name, last_name, birthday, latitude, longitude FROM users, locations WHERE users.user_id = locations.user_id ORDER BY locations.user_id, locations.date_created DESC')
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
                         (help_entry_id, user_id, description, json.dumps(watson_context)))
        if distress_status is not None:
            self.cur.execute(
                'INSERT INTO distress_log (entry_id, user_id, help_log_id, distress_status) VALUES (%s, %s, %s, %s)',
                (distress_entry_id, user_id, help_entry_id, distress_status))
        return True

    def get_watson_context(self, user_id):
        """
        Retrieves latest Watson context from help_log based on user_id.
        :param user_id: a string representing the UUID of the user of interest.
        :return: dict of context if a prior Watson context was found, or otherwise None
        """
        # TODO: need to fix this to somehow capture that conversations can be broken up
        self.cur.execute('SELECT watson_context FROM help_log WHERE user_id=%s ORDER BY date_created DESC LIMIT 1', (user_id, ))
        response = self.cur.fetchone()
        return response[0] if response is not None else None

    def init_distress_status(self, user_id):
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
        distress_entry_id = str(uuid())
        self.cur.execute(
            'INSERT INTO distress_log (entry_id, user_id, help_log_id, distress_status) VALUES (%s, %s, %s, %s)',
            (distress_entry_id, user_id, Database.NULL_UUID, False))
        return True

    def get_distress_status(self, user_id):
        """
        Retrieve latest distress status of specified user based on distress log.
        :param user_id: a string representing the UUID of the user of interest.
        :return: a boolean representing whether the user currently has his distress beacon active or not
        """
        self.cur.execute('SELECT distress_status FROM distress_log WHERE user_id=%s ORDER BY date_created DESC LIMIT 1', (user_id,))
        return self.cur.fetchone()[0]

    def log_disaster(self, disaster_id, disaster_type, latitude, longitude, radius, severity):
        """
        Logs disaster in database.
        :param disaster_id: a UUID representing the disaster
        :param disaster_type: a string representing a brief description of the disaster
        :param latitude: a float representing the latitudinal position of the center of the disaster
        :param longitude: a float representing the longitudinal position of the center of the disaster
        :param radius: a float representing the radius around the center of the disaster
        :param severity: a ranking of how severe the disaster notification is
        :return: True if successful
        """
        self.cur.execute('SELECT disaster_id FROM disaster_log WHERE disaster_id = %s OR (center_latitude = %s AND center_longitude = %s)', (disaster_id, latitude, longitude))
        response = self.cur.fetchone()
        if response is None:
            self.cur.execute('INSERT INTO disasters (disaster_id, disaster_type) VALUES (%s, %s)', (disaster_id, disaster_type))
        else:
            disaster_id = response[0]
        entry_id = str(uuid())
        self.cur.execute('INSERT INTO disaster_log (entry_id, disaster_id, center_latitude, center_longitude, radius, severity) VALUES (%s, %s, %s, %s, %s, %s)', (entry_id, disaster_id, latitude, longitude, radius, severity))
        return True

    def get_severe_disasters(self, severity_threshold):
        """
        Retrieves all severe disasters.
        :return: list of dictionaries with data on severe disasters
        """
        self.cur.execute('SELECT DISTINCT ON (disaster_log.disaster_id) disaster_log.disaster_id, disaster_type, center_latitude, center_longitude, radius, severity FROM disasters, disaster_log WHERE disasters.disaster_id = disaster_log.disaster_id ORDER BY disaster_log.disaster_id, disaster_log.date_created DESC')
        response = self.cur.fetchall()
        return [
            {
                "type": r[1],
                "center_latitude": r[2],
                "center_longitude": r[3],
                "radius": r[4],
                "severity": r[5]
            }
            for r in response if severity_threshold(r[1], r[5])
        ]