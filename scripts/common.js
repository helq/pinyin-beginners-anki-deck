function checkPersistence(callback) {
  if (typeof (window.Persistence) !== 'undefined' && Persistence.isAvailable()) {
    callback();
  } else {
    document.getElementById('root').innerHTML =
      '<div class="big-red">Sorry but this card cannot be ' +
      "displayed on this Anki client.</div>" +
      "<br/>" +
      "<div>This card cannot be previsualized in some platforms. " +
      "Make sure it actually works at study time.</div>" +
      "<br/>" +
      "<div>Please, contact the developer of the deck to let " +
      "them know something went wrong :)</div>";
  }
}

function getChunks(fun, clean = true) {

  var chunks = fun.toString()
    //Strip HTML
    .replace(/<div>/g, "\n")
    .replace(/<\/div>/g, "\n")
    .replace(/<\/?br ?\/?>/g, "\n");

  if (clean) {
    chunks = chunks
      .replace(/\s*</g, "<")
      .replace(/>\s*/g, ">")
  }

  chunks = chunks.split('EOL');
  chunks = chunks.slice(2, chunks.length - 1);
  return chunks;
}

function getElemsFromChunks(fun) {
  return getChunks(fun).map(chunk => {
    var bits = chunk.split("MOS");
    return {
      'sound': bits[0],
      'pinyin': bits[1],
      'zhuyin': bits[2],
      'ipa': bits[3]
    };
  });
}

function shuffle(array) {
  var i = array.length, tmpVal, rnd;
  // While there remain elements to shuffle...
  while (0 !== i) {
    // Pick a remaining element...
    rnd = Math.floor(Math.random() * i);
    i -= 1;
    // And swap it with the current element.
    tmpVal = array[i];
    array[i] = array[rnd];
    array[rnd] = tmpVal;
  }
  return array;
}

function playAudio(id) {
  var query = ['', ' > .replaybutton', ' > [title="Replay"]', ' > a']
    .map(q => '#' + id.toString() + q)
    .join(', ');
  var links = document.querySelectorAll(query);
  for (var link of links) {
    if (link instanceof HTMLAnchorElement) {
      link.click();
      break;
    }
  }
}

function playAudioAndPersistPossibilities(possibilities, max_sounds_shown = 3, playId = 'to-play') {
  shuffle(possibilities);
  possibilities = possibilities.slice(0, max_sounds_shown);

  // Common to front and back cards
  possibilities.forEach(function (elem) {
    var sound = elem['sound'] || elem;

    var toPlay = document.getElementById(playId);
    if (!toPlay) {
      console.error(playId + ' not found')
    } else {
      toPlay.innerHTML += sound;
    }
  });

  // playing first audio
  playAudio(playId);

  // Saving data
  Persistence.setItem('possibilities', JSON.stringify(possibilities));

  return possibilities;
}