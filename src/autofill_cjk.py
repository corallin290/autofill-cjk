import aqt
from aqt import mw
from aqt import gui_hooks
from aqt.utils import qconnect
from aqt.qt import *

from . import cjk_info
from . import jisho
from . import wiktionary

def autofill_cjk_card(addcards: aqt.addcards.AddCards):
    # TODO: check that it is a cjk card
    key = addcards.editor.note['Key']
    if key == "":
        return
    info = cjk_info.get_fields(key)

    wiktionary.open(info['Key'])
    if info['jisho-key'] != '':
        jisho.open(info['jisho-key'])
    if info['linedict-key'] != '':
        # TODO: open linedict
        pass

    for fld in info:
        if fld in addcards.editor.note.keys():
            addcards.editor.note[fld] = info[fld]


    addcards.editor.note.tags = list(set(addcards.editor.note.tags) | info['Tags'])

    addcards.editor.loadNoteKeepingFocus()

def setup_addcards_menu(addcards: aqt.addcards.AddCards) -> None:
    menubar = addcards.form.menubar
    menu = menubar.addMenu('Tools')
    action = menu.addAction('Autofill')
    action.setShortcut(QKeySequence('Ctrl+Shift+D'))
    qconnect(action.triggered, lambda: autofill_cjk_card(addcards))

gui_hooks.add_cards_did_init.append(setup_addcards_menu)
