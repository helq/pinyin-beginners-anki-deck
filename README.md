Pinyin Beginners Anki Deck
==========================

This is the main repository for the [Pinyin Beginners Anki Deck][deckankiurl]. This deck
is targeted to those starting to learn Mandarin Chinese and want to know how are
"syllables" pronunced. All cards are accompanied with three (randomly selected) recordings
of natives pronuncing the syllable.

[deckankiurl]: https://ankiweb.net/shared/info/854183352

Download
--------

I recommend you download this deck from [the Ankiweb webpage][deckankiurl], or if you are
feeling adventurous you can keep reading ;)

"Compile" Deck
--------------

If you want to modify this deck to fit your needs, and you want to do it programatically,
i.e., you want to modify the Python script `generate-deck.py`, you will need to install
the python library `genanki`:

~~~
pip install genanki
~~~

The script is written in Python 3.6 or higher.

Once everything is ready, run the script `generate-deck.py`:

~~~
python3 generate-deck.py
~~~

The scripts generates an Anki deck with name `pinyin_deck.apkg` in the same folder the
script was run. You can install this deck as any other in Anki.

Notice that this repository doesn't contain any of the recordings that the deck uses. You
will need to download the audios independently from
<https://www.mediafire.com/?vpbv0m0me7b81zg>.

Acknoledgements
---------------

Special thanks to [anki-persistence][] which allows me to easily retrieve information
shown at the front of the card.

[anki-persistence]: https://github.com/SimonLammer/anki-persistence

I don't own any of the recordings. All credit for the recordings goes to:

1. <http://resources.allsetlearning.com/chinese/pronunciation/Pinyin_chart>
2. <https://chinese.yabla.com/chinese-pinyin-chart.php>
3. <http://www.yoyochinese.com/chinese-learning-tools/Mandarin-Chinese-pronunciation-lesson/pinyin-chart-table>
4. <http://www.archchinese.com/chinese_pinyin.html>
5. <http://pinpinchinese.com/pinyin-chart/>
6. <http://public.gettysburg.edu/~jli/PinYinChart/ChinesePinYinChartM.html>
7. <http://lost-theory.org/chinese/phonetics/>
8. <http://www.china-on-site.com/language/phonetic/phonetic.htm>
