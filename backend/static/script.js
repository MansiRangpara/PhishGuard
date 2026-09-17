function checkURL() {
  const url = document.getElementById('url-input').value;
  const result = document.getElementById('result');
  if (!url) {
    result.textContent = "Please enter a URL";
    return;
  }

  fetch("/check", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url })
  })
  .then(res => res.json())
  .then(data => { result.textContent = `${url} -> ${data.status}`; })
  .catch(err => { result.textContent = "Error checking URL"; console.error(err); });
}
