// General JS utility functions

export const intcomma = value => {
  // inspired by django.contrib.humanize.intcomma
  // from https://gist.github.com/banterability/559757
  const origValue = String(value);
  const newValue = origValue.replace(/^(-?\d+)(\d{3})/, '$1,$2');
  return (origValue === newValue) ? newValue : intcomma(newValue);
};
