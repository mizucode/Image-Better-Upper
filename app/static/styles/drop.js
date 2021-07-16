mDropzone.options.dropzoneForm = {
    addRemoveLinks: true,
    removedfile: function (file) {
    var _ref;
    return (_ref = file.previewElement) != null ? ref.parentNode.removeChild(file.previewElement) : void 0;
    },
    dictDefaultMessage: "Drop File(s) Here or Click to Upload",

    }