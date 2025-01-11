# Taha Rashid
# Monday May 27, 2024
# Anki Extension

# other
import os
import sys

# Add the path to your module's directory
module_dir = os.path.dirname(__file__)
sys.path.insert(0, module_dir)

# import the main window object (mw) from aqt
from aqt import mw, gui_hooks
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all the Qt GUI library
from aqt.qt import *

# util import
from .util import add_pitch, remove_pitch, get_accent_dict, get_note_type_ids, \
    get_note_ids, get_user_accent_dict, select_deck_id, \
    select_note_type_id, select_note_fields_add, \
    select_note_fields_del, get_plugin_dir_path, \
    get_acc_patt, clean_japanese_from_note_field

# scraper import
from .local_dict import run
# regular expression import
import re
# async import
import asyncio
# time import


# make my own cleaner func... courtesy of ChatGPT so far
def keep_hiragana_katakana_only(line):
    # Regular expression to match characters that are not Hiragana or Katakana
    non_hiragana_katakana_pattern = re.compile(r'[^\u3040-\u309F\u30A0-\u30FF]+')

    # Replace non-Hiragana/Katakana characters with an empty string
    cleaned_line = re.sub(non_hiragana_katakana_pattern, '', line)

    return cleaned_line


# this function will be where all of the proper logic goes in the future.., currently in bulk scrape
def scraper(deck_id, note_type_id):
    # gets all note ids in the selected note type
    note_ids = get_note_ids(deck_id, note_type_id)

    # FINDING SPECIFIC FIELDS OF DATA, WE CAN SPLIT INTO A FUNCTION FROM HERE!!!!
    # exp is kanji, reading is hiragana, output is where you want to save!
    expr_idx, reading_idx, output_idx = select_note_fields_add(note_type_id)
    note_key = list(mw.col.get_note(note_ids[0]).keys())

    # GOING THROUGH EVERY CARD
    # get all kanji, kana and write and put them into a tuple called pairs
    kanji = [(str(mw.col.get_note(note_id)[note_key[expr_idx]])) for note_id in note_ids]
    kana = [str(keep_hiragana_katakana_only(mw.col.get_note(note_id)[note_key[reading_idx]])) for note_id in
            note_ids]
    write = [(str(mw.col.get_note(note_id)[note_key[output_idx]])) for note_id in note_ids]
    pairs = list(zip(kanji, kana, write))

    # DEBUG
    # showInfo(str(pairs[0]) + " {NEXT} " + str(pairs[1]) + " {NEXT} " + str(pairs[300]))
    # showInfo(str(write[0]) + " {NEXT} " + str(write[1]) + " {NEXT} " + str(write[300]))

    # run the local_dict function to fetch information
    results = asyncio.run(run(pairs))  # Note: returned as a tuple...

    # start_time = time.time()  # timing code...
    # end_time = time.time()
    # execution_time = end_time - start_time

    # DEBUG
    # showInfo("Time -> " + str(execution_time))
    # showInfo("Length -> " + str(len(results)))
    # showInfo("MIN ->" + str(results[0]) + "<--->" + str(results[1]) + "<--->" + str(results[300]))
    # showInfo("End!")

    # checking intrans/trans... ALL TESTING!!
    move_idxs = []
    results = list(results)
    for count, result in enumerate(results):
        fun = str(result)
        if (fun.find("Self-Move") != -1) or (fun.find("Other-Move") != -1):
            move_idxs.append(count)

    # debug
    showInfo("Num of trans/intrans -> " + str(len(move_idxs)))

    # showInfo("MIN ->" + str(pairs[move_idxs[0]][2]) + "<--->" + str(pairs[move_idxs[1]][2]) + "<--->" + str(
    #     pairs[move_idxs[60]][2]))

    # note = mw.col.get_note(note_ids[move_idxs[0]])[note_key[output_idx]]
    # showInfo(str(note))
    # hello = results[move_idxs[0]]
    # showInfo(str(hello))

    for move_idx in move_idxs:
        #pairs[move_idx][2]
        note = mw.col.get_note(note_ids[move_idx])
        note[note_key[output_idx]] += (", " + str(results[move_idx]))
        #showInfo(str(note[note_key[output_idx]]))   #debug, IT WORKS
        #flush it and save below
        #HERE

    # note = mw.col.get_note(note_ids[move_idxs[0]])[note_key[output_idx]]
    # showInfo(note)
    # showInfo("INDEXES ->" + str(move_idxs[0]) + "<--->" + str(move_idxs[1]) + "<--->" + str(move_idxs[60]))


# add button in the main window toolbar
def bulk_scrape() -> None:
    try:
        # NARROWING DOWN OUR SELECTION
        # select which deck
        deck_id = select_deck_id('Which deck would you like to extend?')

        # gets all note TYPES
        note_type_ids = get_note_type_ids(deck_id)

        # select which note TYPES
        note_type_id = select_note_type_id(note_type_ids)

        # scraper function
        scraper(deck_id, note_type_id)

    except:
        showInfo("An error/exit occured...")


# add button in the editor toolbar (as an icon)
def manual_scrape(buttons, editor):
    icon_path_m = os.path.join(get_plugin_dir_path(), 'movement.png')
    select_edit_btn = editor.addButton(
        icon_path_m,
        'manual_scrape',
        lambda obj: showInfo("RUNS! -> " + str(obj)),
        tip='manually scrape the dictionary for self/other-move'
    )
    buttons.append(select_edit_btn)


# QT INTERFACE
# create a new menu item, "jisho_scraper"
action = QAction("Self/Other-Move Scraper", mw)
# set it to call jisho_modify when it's clicked
qconnect(action.triggered, bulk_scrape)
# and add it to the tools menu
mw.form.menuTools.addAction(action)

# add editor button
gui_hooks.editor_did_init_buttons.append(manual_scrape)
