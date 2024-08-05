async function showError(resp) {
  const contentType = resp.headers.get("content-type");
  if (contentType && contentType.indexOf("application/json") !== -1) {
    const data = await resp.json()
    window.alert("App exception: " + data["detail"]);
  } else {
    window.alert("App exception: " + resp.statusText);
  }
}

window.addEventListener('load', function () {
  const deleteBtns = document.querySelectorAll(".delete-button");

  deleteBtns.forEach((btn) => {
    btn.addEventListener("click", (event) => {
      if (confirm("Are you sure you want to delete this site?")) {
        const site = event.target.name;
        fetch(`/api/sites/${site}`, {
          method: "DELETE"
        }).then((response) => {
          if (response.ok) {
            window.location.reload();
          } else {
            showError(response)
          }
        });
      }
    });
  });

  const uploadForm = document.getElementById("upload-form");

  uploadForm.addEventListener("submit", (event) => {
    if (event.submitter.value === "cancel") {
      return;
    }

    event.preventDefault();
    const formData = new FormData(uploadForm);
    fetch(uploadForm.action, {
      method: uploadForm.method,
      body: formData
    }).then((response) => {
      if (response.ok) {
        window.location.reload();
      } else {
        showError(response)
      }
    });
  });

  const editButtons = document.querySelectorAll(".edit-button");
  const ENTER_KEY = 13;
  const editableKeyPressListener = (event) => {
    if (event.which === ENTER_KEY) {
      event.preventDefault();
      removeEditable(event.target);

      const oldName = event.target.oldText;
      const newName = event.target.innerText;

      fetch(`/api/sites/${oldName}`, {
        method: "PUT",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name: newName}),

      }).then((response) => {
          if (response.ok) {
            window.location.reload();
          } else {
            showError(response).then(() => {
              window.location.reload();
            });
          }
        }
      )
    }
  }

  const removeEditable = (el) => {
    el.style.outline = "";
    el.removeAttribute("contenteditable");
    el.removeEventListener('keypress', editableKeyPressListener);
  }

  for (const editButton of editButtons) {
    editButton.addEventListener("click", (event) => {
        const text = editButton.parentElement.firstElementChild;
        const style = "2px dotted #333";
        if (text.style.outline === "") {
          text.style.outline = style;
          text.contentEditable = "plaintext-only";
          text.addEventListener('keypress', editableKeyPressListener);
          text.oldText = text.innerText;
        } else {
          removeEditable(text);
        }
      }
    )
  }
})
;
