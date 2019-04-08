import requests
import json

OXFORD_API_KEY = "5a1e5ebe8231caa5394d6c2d6d4610ce"
OXFORD_APP_ID = "bf9c0e59"
OXFORD_URL = "https://od-api.oxforddictionaries.com/api/v1"


def process_word(word):
    """
    Pre-processes a word before requesting its defnition.

    :param word: Word to be pre-processed.
    :return: Processed word.
    """

    return word


def clean_entries(entries):
    """
    Cleans out excessive metadata for a Oxford entry.

    :param entries: List of entries to clean out.
    :return: Cleaned out entries.
    """

    new_entries = []

    for entry in entries:
        raw_senses = entry['senses']
        definitions = list(map(lambda s: s['definitions'][0], raw_senses))
        raw_examples = list(map(lambda s: s['examples'], raw_senses))
        
        examples = []
        for raw_example in raw_examples:
            processed_raw_examples = list(map(lambda e: e['text'], raw_example))
            for processed_raw_example in processed_raw_examples:
                examples.append(processed_raw_example)

        new_entry = {
            'definitions': definitions,
            'examples': examples
        }

        new_entries.append(new_entry)

    return new_entries


def process_raw_definition(raw_definition):
    """
    Cleans out a raw definition of a word from the Oxford 
    Dictionary JSON.

    :param raw_definition: Raw definition dictionary to process.
    :return: Cleaned out version of the raw definition.
    """

    entries = raw_definition['entries']
    entries = clean_entries(entries)

    definition = {
        'category': raw_definition['lexicalCategory'],
        'entries': entries
    }

    return definition


def get_definition(word):
    """
    Looks up the definiton of a word on Oxford Dictionary.

    :param word: word to be searched up.
    :return: complete definition of word, if possible.
    """

    processed_word = process_word(word)

    headers = {
        'app_id': OXFORD_APP_ID,
        'app_key': OXFORD_API_KEY
    }

    params = {
        'source_lang': 'en',
        'word_id': processed_word
    }

    response = requests.get("{}/entries/{}/{}".format(OXFORD_URL, params['source_lang'], params['word_id']), 
        headers=headers)

    if response.status_code != 200:
        return None, "Could not find definition of {}!".format(word)

    search_json = json.loads(response.content.decode('utf-8'))

    raw_definitions = search_json['results'][0]['lexicalEntries']
    definitions = list(map(lambda x: process_raw_definition(x), raw_definitions))

    return definitions
