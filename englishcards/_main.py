#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#   English Cards
#   Flash cards for learning English.
#
#   https://github.com/kosarev/englishcards
#
#   Copyright (C) 2020 Ivan Kosarev.
#   ivan@kosarev.info
#
#   Published under the MIT license.

import appdirs
import os
from ._evp import EVPDeck


class Logger(object):
    def __call__(self, message):
        print(message)


class Cache(object):
    def __init__(self, config):
        self.__config = config

    def get(self, id, retrieve):
        # Return a cached copy, if available.
        dir = os.path.join(self.__config['cache_dir'], *id[:-1])
        path = os.path.join(dir, id[-1])
        try:
            return open(path, 'rb')
        except FileNotFoundError:
            pass

        # Otherwise, retrieve and cache.
        os.makedirs(dir, exist_ok=True)
        temp_path = path + '.part'
        with open(temp_path, 'wb') as f:
            for chunk in retrieve():
                f.write(chunk)

        os.rename(temp_path, path)

        return open(path, 'rb')


def main(args=None):
    dirs = appdirs.AppDirs('englishcards')
    config_dir = dirs.user_data_dir

    config = {
        'cache_dir': os.path.join(config_dir, 'cache'),
    }

    cache = Cache(config)
    log = Logger()
    deck = EVPDeck(cache, log)
    deck.pick_card()


if __name__ == "__main__":
    main()
