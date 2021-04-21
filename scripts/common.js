function checkPersistence(callback) {
  if (Persistence.isAvailable()) {
    callback();
  } else {
    document.getElementById("the-card").innerHTML =
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

function getElems(fun) {
  var chunks = fun.toString();
  chunks = chunks.replace(/<div>/g, "\n").replace(/<\/div>/g, "\n").replace(/<\/?br ?\/?>/g, "\n"); //Strip HTML.
  //chunks = chunks.replace(/\s*</g, "<").replace(/>\s*/g, ">"); //Cleaning
  chunks = chunks.split('EOL');
  chunks = chunks.slice(2, chunks.length - 1);
  var elems = [];
  chunks.forEach(function (chunk) {
    var bits = chunk.split("MOS");
    elems.push({
      'sound': bits[0],
      'pinyin': bits[1],
      'zhuyin': bits[2],
      'ipa': bits[3]
    });
  });
  return elems;
}

function playAudio(id) {
  try {
    var link = document.querySelector(id);
    if (!(link instanceof HTMLAnchorElement))
      link = document.querySelector(id + " > .replay-button");
    if (!(link instanceof HTMLAnchorElement))
      link = document.querySelector(id + " > [title=Replay]");
    if (!(link instanceof HTMLAnchorElement))
      link = document.querySelector(id + " > a");

    if (link instanceof HTMLAnchorElement) {
      link.click();
    }
  } catch (e) {
  }
}