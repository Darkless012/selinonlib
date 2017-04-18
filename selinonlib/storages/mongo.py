#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ######################################################################
# Copyright (C) 2016-2017  Fridolin Pokorny, fridolin.pokorny@gmail.com
# This file is part of Selinon project.
# ######################################################################
"""
MongoDB database adapter
"""

try:
    from pymongo import MongoClient
except ImportError:
    raise ImportError("Please install pymongo using `pip3 install pymongo` in order to use MongoStorage")
from selinon import DataStorage


class MongoStorage(DataStorage):
    """
    MongoDB database adapter
    """

    def __init__(self, db_name, collection_name, host="localhost", port=27017):
        super(MongoStorage, self).__init__()
        self.client = None
        self.collection = None
        self.db = None  # pylint: disable=invalid-name
        self.host = host
        self.port = port
        self.db_name = db_name
        self.collection_name = collection_name

    def is_connected(self):
        return self.client is not None

    def connect(self):
        self.client = MongoClient(self.host, self.port)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    def disconnect(self):
        if self.is_connected():
            self.client.close()
            self.client = None
            self.db = None
            self.collection = None

    def retrieve(self, flow_name, task_name, task_id):
        assert self.is_connected()  # nosec

        filtering = {'_id': 0}
        cursor = self.collection.find({'task_id': task_id}, filtering)

        if len(cursor) > 1:
            raise ValueError("Multiple records with same task_id found")
        elif not cursor:
            raise FileNotFoundError("Record not found in database")

        record = cursor[0]

        assert task_name == record['task_name']  # nosec
        return record.get('result')

    def store(self, node_args, flow_name, task_name, task_id, result):
        assert self.is_connected()  # nosec

        record = {
            'flow_name': flow_name,
            'node_args': node_args,
            'task_name': task_name,
            'task_id': task_id,
            'result': result

        }

        self.collection.insert(record)

        # task_id is unique here
        return task_id

    def store_error(self, node_args, flow_name, task_name, task_id, exc_info):
        # just to make pylint happy
        raise NotImplementedError()
