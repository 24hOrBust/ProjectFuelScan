function showMessages(messages) {
  console.log(messages);
  if(messages.length == 0){
    return;
  }
  document.onrea
  var snackbarContainer = document.querySelector("#demo-snackbar-example");
  console.log(snackbarContainer);
  var data = {
    message: messages,
    timeout: 2000,
  };

  snackbarContainer.MaterialSnackbar.showSnackbar(data);
}