window.setup_markdown_editor = (elem) ->
  elem = $(elem)
  new_elem = $("<div></div>")

  new_elem.insertBefore(elem)

  elem.hide()

  editor = new EpicEditor(
    container: new_elem[0]
    clientSideStorage: false
    textarea: elem[0]
    basePath: '/static/epiceditor/epiceditor'
    theme:
      base: '/themes/base/epiceditor.css'
      editor: '/themes/editor/epic-light.css'
      preview: '/themes/preview/github.css'
  )
  editor.load()

$ ->
  $('.edit_markdown').each ->
    setup_markdown_editor this