
    const input = document.querySelector('input');
    const preview = document.querySelector('.preview');

    input.style.opacity = 0;

    input.addEventListener('change', updateImageDisplay);

    function updateImageDisplay() {
      while(preview.firstChild) {
        preview.removeChild(preview.firstChild);
      }

      const curFiles = input.files;

      if(curFiles.length === 0) {
        const para = document.createElement('p');
        para.textContent = 'No files currently selected for upload. Please make sure the file size total is under 2MB.';
        preview.appendChild(para);
      } else {
        const list = document.createElement('ol');
        preview.appendChild(list);

      for(const file of curFiles) {
         const listItem = document.createElement('li');
         const para = document.createElement('p');

      if(file) {
         para.textContent = `${file.name}, file size ${returnFileSize(file.size)}.`;
         const image = document.createElement('img');
         image.src = URL.createObjectURL(file);

         listItem.appendChild(image);
         listItem.appendChild(para);
         }

          list.appendChild(listItem);
        }
      }
    }

    function returnFileSize(number) {
      if(number < 1024) {
        return number + 'bytes';
      } else if(number > 1024 && number < 1048576) {
        return (number/1024).toFixed(1) + 'KB';
      } else if(number > 1048576 && number < 2097151) {
        return (number/1048576).toFixed(1) + 'MB';
      } else if(number > 2097151) {
        return 'is too large. Please select the Upload button to add a new file';
      }
    }
