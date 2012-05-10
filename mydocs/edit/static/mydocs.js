function initEditor(isReadOnly) {
    if(isReadOnly) {
        CKEDITOR.config.toolbarStartupExpanded = false;

        /* Hide the save button. This isn't probably a terribly good way... */
        CKEDITOR.config.toolbar_Full[0].items.splice(2, 1);

        CKEDITOR.on('instanceReady', function(ev) {
            ev.editor.setReadOnly(true);
        });
    }
    window.addEventListener('load', function() {
        CKEDITOR.replace('content');
    });
}
