function list_files(){
    let x = document.getElementById("file");
    let txt = "";
    if ('files' in x) {
    if (x.files.length === 0) {
      txt = "Select one or more files.";
    } else {
      for (let i = 0; i < x.files.length; i++) {
          let file = x.files[i];
          if ('name' in file) {
          txt += "file selected: " + file.name + "<br>";
        }
      }
    }
  }
  else {
    if (x.value === "") {
      txt += "Select one or more files.";
    } else {
      txt += "The files property is not supported by your browser!";
      txt  += "<br>The path of the selected file: " + x.value; // If the browser does not support the files property, it will return the path of the selected file instead.
    }
  }
  document.getElementById("upload_text").innerHTML = txt;
}