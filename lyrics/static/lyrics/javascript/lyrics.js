window.addEventListener('load', function() {
  const container = document.getElementById('lyric');
  applyMagneticSelectionOnMouseUp(container);
  overrideCopyBehaviour(container);
  loadLyricAttributes();
  loadLyricNotations();
  LyricNotationCard.initializeAll();
  loadPhoneticNotations();
})

const loadLyricAttributes = () => {
  const lyricContainer = document.getElementById('lyric');

  let lineCharOffset = 0;

  for (let lyricLine of lyricContainer.children) {
    lyricLine.setAttribute('data-char-offset', lineCharOffset)

    let wordCharOffset = 0;

    for (let word of Array.from(lyricLine.children).filter(child => child.dataset.wordId)) {
      word.setAttribute('data-char-offset', wordCharOffset)
      wordCharOffset += word.textContent.length;
    }
    lineCharOffset += wordCharOffset;
  }
}

const loadLyricNotations = () => {
  for (let notation of lyricNotations) {
    const position = {
      startLine: notation['start_line'],
      startOffset: notation['start_offset'],
      endLine: notation['end_line'],
      endOffset: notation['end_offset']
    }
    const lyricNotation = new LyricNotation(notation['id'], notation['lyric_id'], notation['selected_text'], notation['content'], position);
    lyricNotation.highlight();
  }
}

const loadPhoneticNotations = () => {
  for (let notation of phoneticNotations) {
    const position = {
      line: notation['line'],
      offset: notation['offset']
    }
    const phoneticNotation = new PhoneticNotation(notation['id'], notation['lyric_id'], notation['selected_text'], notation['content'], position);
    phoneticNotation.annotate();
  }
}
