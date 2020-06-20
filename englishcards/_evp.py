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

import requests


class EVPDeck(object):
    __URL = 'https://www.englishprofile.org/wordlists/evp'
    __LEVEL_CODES = {'A1': 1, 'A2': 2, 'B1': 3, 'B2': 4, 'C1': 5, 'C2': 6}

    def __init__(self, cache, log):
        self.__cache = cache
        self.__log = log
        self.__loaded_cards = []
        self.__levels_to_load = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']

    def __search_words(self, group, value):
        post_data = {
            'filter_search': '*',
            'filter_custom_Topic': '',
            'filter_custom_Parts': '',
            'filter_custom_Category': '',
            'filter_custom_Grammar': '',
            'filter_custom_Usage': '',
            'filter_custom_Prefix': '',
            'filter_custom_Suffix': '',
            'limit': '0',
            'directionTable': 'asc',
            'sortTable': 'base',
            'task': '',
            'boxchecked': '0',
            'filter_order': 'pos_rank',
            'filter_order_Dir': 'asc',
        }

        if group == 'level':
            post_data['filter_custom_Level[]'] = str(self.__LEVEL_CODES[value])
        else:
            assert 0, f'Unknown group {group!r}!'

        def retrieve():
            self.__log(f'Retrieve EVP word list: {group} {value}.')

            r = requests.post(self.__URL, post_data)
            r.raise_for_status()
            for chunk in r.iter_content(chunk_size=8192):
                yield chunk

        return self.__cache.get(('evp', f'{group}-{value}'), retrieve)

    def __load_cards(self):
        if not self.__levels_to_load:
            return

        level = self.__levels_to_load.pop(0)
        words = self.__search_words('level', level)
        assert 0, (level, words)

    def pick_card(self):
        if not self.__loaded_cards:
            self.__load_cards()

        if not self.__loaded_cards:
            return None

        return self.__loaded_cards.pop(0)
