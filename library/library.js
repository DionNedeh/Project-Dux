const input = document.querySelector('#filter');
const items = [...document.querySelectorAll('#catalog li')];
const result = document.querySelector('#result');
const search = new Map((window.DUX_SEARCH || []).map(record => [record.path, record.text]));
if (input && result && search.size) input.addEventListener('input', () => {
  const terms = input.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
  let shown = 0;
  for (const item of items) {
    const text = search.get(item.dataset.path) || '';
    const match = terms.every(term => text.includes(term));
    item.hidden = !match;
    if (match) shown++;
  }
  result.textContent = terms.length ? `${shown} chapter${shown === 1 ? '' : 's'} found.` : '';
});
