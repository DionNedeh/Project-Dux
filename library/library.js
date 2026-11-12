(() => {
  const controls = document.querySelector('#controls');
  const input = document.querySelector('#filter');
  const kind = document.querySelector('#kind');
  const topic = document.querySelector('#topic');
  const reset = document.querySelector('#reset');
  const result = document.querySelector('#result');
  const items = [...document.querySelectorAll('#catalog li')];
  const search = new Map((window.DUX_SEARCH || []).map(record => [record.path, record.text]));
  if (!input || !result || !items.length || !search.size) return;
  const value = select => (select ? select.value : 'all');
  const apply = () => {
    const terms = input.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    const wantKind = value(kind);
    const wantTopic = value(topic);
    let shown = 0;
    for (const item of items) {
      const text = search.get(item.dataset.path) || '';
      const match = (wantKind === 'all' || wantKind === item.dataset.kind)
        && (wantTopic === 'all' || wantTopic === item.dataset.topic)
        && terms.every(term => text.includes(term));
      item.hidden = !match;
      if (match) shown++;
    }
    result.textContent = `${shown} research ${shown === 1 ? 'note' : 'notes'}`;
  };
  input.addEventListener('input', apply);
  if (kind) kind.addEventListener('change', apply);
  if (topic) topic.addEventListener('change', apply);
  if (reset) reset.addEventListener('click', () => {
    input.value = '';
    if (kind) kind.value = 'all';
    if (topic) topic.value = 'all';
    apply();
    input.focus();
  });
  if (controls) controls.hidden = false;
  if (input.value || value(kind) !== 'all' || value(topic) !== 'all') apply();
})();
