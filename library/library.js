const input = document.querySelector('#filter');
const kind = document.querySelector('#kind');
const topic = document.querySelector('#topic');
const reset = document.querySelector('#reset');
const controls = document.querySelector('#controls');
const items = [...document.querySelectorAll('#catalog li')];
const result = document.querySelector('#result');
const search = new Map((window.DUX_SEARCH || []).map(record => [record.path, record.text]));
if (input && kind && topic && reset && controls && result && search.size) {
  const apply = () => {
    const terms = input.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    let shown = 0;
    for (const item of items) {
      const text = search.get(item.dataset.path) || '';
      const match = terms.every(term => text.includes(term)) && (kind.value === 'all' || kind.value === item.dataset.kind) && (topic.value === 'all' || topic.value === item.dataset.topic);
      item.hidden = !match;
      if (match) shown++;
    }
    result.textContent = `${shown} research ${shown === 1 ? 'note' : 'notes'}`;
  };
  input.addEventListener('input', apply);
  kind.addEventListener('change', apply);
  topic.addEventListener('change', apply);
  reset.addEventListener('click', () => { input.value = ''; kind.value = 'all'; topic.value = 'all'; apply(); input.focus(); });
  controls.hidden = false;
}
