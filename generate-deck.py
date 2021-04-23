import json
import re
import subprocess
from pathlib import Path
from typing import List, Any, Tuple, Dict

import genanki
from bs4 import BeautifulSoup
from os import sep


def init_notes() -> Dict[str, Dict[str, str]]:
    scripts_path = Path('scripts')

    def init_npm():
        args = ['npm', 'install']
        print(f"Running npm install from '{scripts_path}'")
        p = subprocess.run(args, capture_output=False, shell=True, cwd=scripts_path)
        if p.returncode:
            raise Exception(p.stderr.decode())

    init_npm()

    def inject(path: Path):
        here = path.parent
        with open(path, 'r') as html:
            soup = BeautifulSoup(html, features='html.parser')

        for script in soup.find_all('script', src=True):
            src_path = here / script.attrs.pop('src')
            data = open(src_path.resolve(), 'r').read()
            script.insert(0, data)

        for script in soup.find_all('script', src=False):
            print(f"Transpiling '{path.parent.name}{sep}{path.name}'")
            rollup_config = scripts_path / 'rollup.config.js'
            args = ['npx', 'rollup', '--config', rollup_config.resolve(), '--stdin=js']
            p = subprocess.run(args, input=bytes(script.string, encoding=html.encoding),
                               capture_output=True, shell=True, cwd=here.resolve())
            if p.returncode:
                raise Exception(p.stderr.decode())
            script.string = p.stdout.decode(html.encoding)

        return soup.prettify(formatter='html')

    notes_path = Path('notes')
    spell_path = notes_path / 'Spellings and Sounds'
    pairs_path = notes_path / 'Pair Sounds'
    tones_path = notes_path / 'Chinese Tones'
    css = open(Path('scripts/style.css'), 'r').read()

    return {
        'spellings': {
          'front1': inject(spell_path / 'front-01.html'),
          'back1': inject(spell_path / 'back-01.html'),
          'front2': inject(spell_path / 'front-02.html'),
          'back2': inject(spell_path / 'back-02.html'),
          'style': css,
        },
        'pairs': {
          'front': inject(pairs_path / 'front-01.html'),
          'back': inject(pairs_path / 'back-01.html'),
          'style': css,
        },
        'tones': {
          'front': inject(tones_path / 'front-01.html'),
          'back': inject(tones_path / 'back-01.html'),
          'style': css,
        }
    }


notes = init_notes()

spellings_model = genanki.Model(
  1890075746,
  'Spellings and sounds',
  fields=[
    {'name': 'Pinyin'},
    {'name': 'Zhuyin'},
    {'name': 'IPA'},
    {'name': 'Extra Info'},
    {'name': 'Audio 1'},
    {'name': 'Type of Sound'},
  ],
  templates=[
    {
      'name': 'What is the spelling of',
      'qfmt': notes['spellings']['front1'],
      'afmt': notes['spellings']['back1'],
    },
    {
      'name': 'Which sound does this represents',
      'qfmt': notes['spellings']['front2'],
      'afmt': notes['spellings']['back2'],
    },
  ],
  css=notes['spellings']['style']
)


def format_card(card_template: str, val1: int, val2: int, opt: bool = False) -> str:
    card_template = card_template \
        .replace('||SOUND NUMBER 1||', str(val1)) \
        .replace('||SOUND NUMBER 2||', str(val2))
    if val1 == 3 or val2 == 3:
        card_template = (
            "{{#Pinyin 3}}\n" + card_template + "\n{{/Pinyin 3}}"
        )
        if opt:
            card_template = (
                '{{#Compare with "Pinyin 3"'
                ' multiple times (or once)? (create 3 cards or 1) [y=3cards]}}\n'
                + card_template
                + '\n{{/Compare with "Pinyin 3"'
                ' multiple times (or once)? (create 3 cards or 1) [y=3cards]}}'
            )
    return card_template


pairs_model = genanki.Model(
  556950176,
  'Minimal pair sounds',
  fields=[
    {'name': 'Pair Sounds'},
    {'name': 'Pinyin 1'},
    {'name': 'Zhuyin 1'},
    {'name': 'IPA 1'},
    {'name': 'Pinyin 2'},
    {'name': 'Zhuyin 2'},
    {'name': 'IPA 2'},
    {'name': 'Pinyin 3'},
    {'name': 'Zhuyin 3'},
    {'name': 'IPA 3'},
    {'name': 'Audio 1'},
    {'name': 'Audio 2'},
    {'name': 'Audio 3'},
    {'name': 'Extra Info'},
    {'name': 'Compare with "Pinyin 3"'
             ' multiple times (or once)? (create 3 cards or 1) [y=3cards]'},
  ],
  templates=[
    {
      'name': 'Which (1-2)? - 1',
      'qfmt': format_card(notes['pairs']['front'], 1, 2),
      'afmt': format_card(notes['pairs']['back'],  1, 2),
    },
    {
      'name': 'Which (1-2)? - 2',
      'qfmt': format_card(notes['pairs']['front'], 1, 2),
      'afmt': format_card(notes['pairs']['back'],  1, 2),
    },
    {
      'name': 'Which (1-2)? - 3',
      'qfmt': format_card(notes['pairs']['front'], 1, 2),
      'afmt': format_card(notes['pairs']['back'],  1, 2),
    },
    {
      'name': 'Which (1-3)? - 1',
      'qfmt': format_card(notes['pairs']['front'], 1, 3),
      'afmt': format_card(notes['pairs']['back'],  1, 3),
    },
    {
      'name': 'Which (1-3)? - 2',
      'qfmt': format_card(notes['pairs']['front'], 1, 3, opt=True),
      'afmt': format_card(notes['pairs']['back'],  1, 3, opt=True),
    },
    {
      'name': 'Which (1-3)? - 3',
      'qfmt': format_card(notes['pairs']['front'], 1, 3, opt=True),
      'afmt': format_card(notes['pairs']['back'],  1, 3, opt=True),
    },
    {
      'name': 'Which (2-3)? - 1',
      'qfmt': format_card(notes['pairs']['front'], 2, 3),
      'afmt': format_card(notes['pairs']['back'],  2, 3),
    },
    {
      'name': 'Which (2-3)? - 2',
      'qfmt': format_card(notes['pairs']['front'], 2, 3, opt=True),
      'afmt': format_card(notes['pairs']['back'],  2, 3, opt=True),
    },
    {
      'name': 'Which (2-3)? - 3',
      'qfmt': format_card(notes['pairs']['front'], 2, 3, opt=True),
      'afmt': format_card(notes['pairs']['back'],  2, 3, opt=True),
    },
  ],
  css=notes['pairs']['style']
)

tones_model = genanki.Model(
  1923816429,
  'Chinese Tones',
  fields=[
    {'name': 'Card Name'},
    {'name': 'tone1'},
    {'name': 'tone2'},
    {'name': 'tone3'},
    {'name': 'tone3-trad'},
    {'name': 'tone4'},
  ],
  templates=[
    {
      'name': 'Which tone?',
      'qfmt': notes['tones']['front'],
      'afmt': notes['tones']['back'],
    },
  ],
  css=notes['tones']['style']
)


class PinyinNote(genanki.Note):  # type: ignore
    @property
    def guid(self) -> Any:
        return genanki.guid_for(self.fields[0])


all_recordings: Dict[str, Any] = json.load(open("recordings/recordings.json"))
all_zhuyin: Dict[str, str] = json.load(open("recordings/zhuyin.json"))


def lookup_zhuyin(pinyin: str) -> str:
    pinyin = pinyin.replace('ü', 'u')

    if pinyin not in all_zhuyin:
        raise Exception(f"'{pinyin}' isn't zhuyin")
    return all_zhuyin[pinyin]


zy_re = re.compile(r'(-?[üa-uw-z]+)([1-4]?)')


def get_zhuyin_syllable(pinyin: str) -> str:
    match_zy = zy_re.match(pinyin)
    if not match_zy:
        raise Exception(f"'{pinyin}' isn't a syllable")
    return lookup_zhuyin(match_zy[1]) + all_zhuyin[match_zy[2]]


def gen_decks_initials_finals() -> Tuple[Any, Any]:
    initials_deck = genanki.Deck(
        481218247,
        'Chinese::Pinyin::A. Initials'
    )

    finals_deck = genanki.Deck(
        231241779,
        'Chinese::Pinyin::B. Finals'
    )

    with open("recordings/initials.json") as f:
        initials = json.load(f)

    with open("recordings/finals.json") as f:
        finals = json.load(f)

    for parts, name, deck in [
            (initials, 'initial', initials_deck),
            (finals, 'final', finals_deck)
    ]:
        for part, data in parts.items():
            part_audios = data['recordings']

            if part+'1' in all_recordings:
                part_audios.extend(all_recordings[part+'1']['recordings'])

            fields = [
                part,
                all_zhuyin[part],
                data['ipa'],
                data['notes'],
                ' EOL <br/> '.join([f"[sound:{s}]" for s in part_audios]),
                name
            ]
            deck.add_note(PinyinNote(model=spellings_model, fields=fields))

    return initials_deck, finals_deck


def find_audios(pinyins: List[str]) -> str:
    audios: List[str] = []

    for pinyin in pinyins:
        recording = all_recordings[pinyin]
        ipa = recording['ipa']
        for rec in recording['recordings']:
            audios.append(f'[sound:{rec}] MOS {pinyin} MOS {get_zhuyin_syllable(pinyin)} MOS {ipa}')

    return ' EOL </br> '.join(audios)


def gen_deck_pairs() -> Any:
    pairs_deck = genanki.Deck(
        1169464332,
        'Chinese::Pinyin::C. (Minimal Pairs)'
    )

    with open("recordings/pairs.json") as f:
        pairs = json.load(f)

    for pair, data in pairs.items():
        pinyin: List[str] = [data[f'written-{i}'] for i in range(1, 4)]

        def get_zhuyin(i):
            w = pinyin[i]
            return lookup_zhuyin(w) if w else ''

        fields = [
            pair,
            pinyin[0],
            get_zhuyin(0),
            data['ipa-1'],
            pinyin[1],
            get_zhuyin(1),
            data['ipa-2'],
            pinyin[2],
            get_zhuyin(2),
            data['ipa-3'],
            find_audios(data['sounds-1']),
            find_audios(data['sounds-2']),
            find_audios(data['sounds-3']),
            data['notes'],
            data['compare'],
        ]
        # print("New card:", fields)
        pairs_deck.add_note(PinyinNote(model=pairs_model, fields=fields))
    return pairs_deck


py_re = re.compile(r"[^_]*")


def mix_audios(audios: List[str]) -> str:
    row: List[str] = []

    for audio in audios:
        match_py = py_re.match(audio)
        if match_py:
            pinyin = match_py[0]
        else:
            raise Exception(f"No pinyin reading can be found for audio `{audio}`")

        ipa = all_recordings[pinyin]['ipa']
        row.append(f'[sound:{audio}] MOS {pinyin} MOS {get_zhuyin_syllable(pinyin)} MOS {ipa}')

    return ' EOL </br> '.join(row)


def gen_deck_tones() -> Any:
    tones_deck = genanki.Deck(
        1856348667,
        'Chinese::Pinyin::D. Tones'
    )

    with open("recordings/tones.json") as f:
        tones = json.load(f)

    for tone_title, data in tones.items():
        fields = [
            tone_title,
            mix_audios(data['tone-1']),
            mix_audios(data['tone-2']),
            mix_audios(data['tone-3']),
            mix_audios(data['tone-3-trad']),
            mix_audios(data['tone-4']),
        ]
        # print("New card:", fields)
        tones_deck.add_note(PinyinNote(model=tones_model, fields=fields))

    return tones_deck


def gen_deck_readme() -> Any:
    # TODO: Add the inline markup to notes and postprocess it instead
    readme_deck = genanki.Deck(
        1838790718,
        'Chinese::Pinyin::.. Readme first ..'
    )

    basic_model = genanki.Model(
      2122906168,
      'Basic',
      fields=[
        {'name': 'Front'},
        {'name': 'Back'},
      ],
      templates=[
        {
          'name': 'Card',
          'qfmt': '{{Front}}',
          'afmt': '{{FrontSide}}\n\n<hr id=answer>\n\n{{Back}}',
        },
      ],
      css="""
          .card {
           font-family: arial;
           font-size: 20px;
           text-align: center;
           color: black;
           background-color: white;
          }
          """
    )

    fields = [
        '\n'.join([
         '<div style="font-family: Arial; font-size: 15px;">',
         "Hi dear learner. Thank you for for trying out this deck. This couldn't be a thing",
         'without the hard work of many people who recorded audio and who built the',
         'software you are using. I am grateful for their hard work.',
         '<br><br>',
         'If you are using a recent version of Anki (Anki Desktop 2.1.25, AnkiDroid 2.14.3, or',
         'Anki for iOS), the deck should work for you without any further configuration.',
         '<br><br><br>',
         'Please read carefully the paragraphs below if you encounter any problems with the',
         'deck or if you are using a slightly older version of Anki.',
         '<br><br><br>',
         'If you are using an <strong>old version of Anki Desktop</strong>, you need to:',
         '<ul>',
         '  <li>',
         '    install the Anki addon "Replay buttons on card" (Id:',
         '    <a href="https://ankiweb.net/shared/info/498789867">498789867</a>)',
         '    so that audio can be played properly, and',
         '  </li>',
         '  <li>',
         '    disable Anki automatically playing audio:',
         '    <br>',
         '    Deck -&gt; Options -&gt; General -&gt; Automatically play audio',
         '  </li>',
         '</ul>',
         '<br>',
         'This Deck has been tested in Anki Desktop 2.1.25 and AnkiDroid 2.14.3. It has been',
         'reported to work in Anki for iOS (Thanks to',
         '<a href="https://github.com/helq/pinyin-beginners-anki-deck/pull/4">mikelambert</a>',
         'for the patches required to make it work).',
         '<br><br>',
         'Developed by: helq<br>',
         'Main page:',
         '<a href="https://github.com/helq/pinyin-beginners-anki-deck">github webpage</a>',
         '<br><br>',
         '2016 - 2021<br></div>']),
        '\n'.join([
         '<div style="font-family: Arial; font-size: 15px;">',
         'You can now suspend this card, ignore it or delete it. But I suggest you keep it',
         'around in case you need it in the future ;)<br>',
         '<br>',
         "That's all! Enjoy!",
         '<br>',
         '</div>'])
    ]

    readme_deck.add_note(genanki.Note(model=basic_model, fields=fields))

    return readme_deck


package = genanki.Package(
    list(gen_decks_initials_finals()) + [gen_deck_pairs(), gen_deck_tones(), gen_deck_readme()]
)

package.write_to_file('pinyin_deck.apkg')
