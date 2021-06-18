
function onStartedDownload(id) {
  console.log(`Started downloading: ${id}`);
}

function onFailed(error) {
  console.log(`Download failed: ${error}`);
}

var downloadUrl = "https://example.org/image.png";

var downloading = browser.downloads.download({
  url : downloadUrl,
  filename : 'my-image-again.png',
  conflictAction : 'uniquify'
});

downloading.then(onStartedDownload, onFailed);