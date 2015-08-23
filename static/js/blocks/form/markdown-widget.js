function setup_markdown_editor(elem) {
    var elem = $(elem);
    var new_elem = $("<div></div>");

    new_elem.insertBefore(elem);

    elem.hide();

    var editor = new EpicEditor({
        container: new_elem[0],
        clientSideStorage: false,
        textarea: elem[0],
        basePath: '/static/epiceditor/epiceditor',
        theme: {
            base: '../../../lib/epiceditor/themes/base/epiceditor.css',
            editor: '../../../lib/epiceditor/themes/editor/epic-light.css',
            preview: '../../../lib/epiceditor/themes/preview/github.css'
        }
    });
    editor.load();
}

$(function() {
    $('.markdown-widget').each(function() {
        setup_markdown_editor(this);
    });
});