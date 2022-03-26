
function showNotifications() {
  const container = document.getElementById('notification-container');

  if (container.classList.contains('d-none')) {
    container.classList.remove('d-none');
  } else {
    container.classList.add('d-none');
  }
}


function removeNotification(removeNotificationURL, redirectURL) {
  const csrftoken = getCookie('csrftoken');
  let xmlhttp = new XMLHttpRequest();

  xmlhttp.onreadystatechange = function () {
    if (xmlhttp.readyState == XMLHttpRequest.DONE) {
      if (xmlhttp.status == 200) {
        window.location.replace(redirectURL);
      } else {
        alert('There was an error');
      }
    }
  };

  xmlhttp.open("DELETE", removeNotificationURL, true);
  xmlhttp.setRequestHeader("X-CSRFToken", csrftoken);
  xmlhttp.send();
}