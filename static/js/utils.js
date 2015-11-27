// General JS utility functions

function intcomma(value) {
    // inspired by django.contrib.humanize.intcomma
    // from https://gist.github.com/banterability/559757
    var origValue = String(value);
    var newValue = origValue.replace(/^(-?\d+)(\d{3})/, '$1,$2');
    if (origValue == newValue){
        return newValue;
    } else {
        return intcomma(newValue);
    }
};