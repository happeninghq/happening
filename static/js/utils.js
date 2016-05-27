// General JS utility functions

export const intcomma = value => {
  // inspired by django.contrib.humanize.intcomma
  // from https://gist.github.com/banterability/559757
  const origValue = String(value);
  const newValue = origValue.replace(/^(-?\d+)(\d{3})/, '$1,$2');
  return (origValue === newValue) ? newValue : intcomma(newValue);
};

export const toCamelCase = value =>
  value.replace(/-([a-z])/g, function (g) { return g[1].toUpperCase(); });


let i = 0;
export const idGenerator = elem => {
  if (!elem.dataset.generatedId) {
  	elem.dataset.generatedId = 'id_' + i++;
  }
  return elem.dataset.generatedId
}