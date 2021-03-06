#!/bin/env python3

from functools import reduce


def argsFieldLessEqual(node_args, key, value):
    try:
        val = reduce(lambda m, k: m[k], key if isinstance(key, list) else [key], node_args)
        return val <= value
    except:
        return False
