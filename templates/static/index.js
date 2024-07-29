window.addEventListener('load', function () {
  const deleteBtns = document.querySelectorAll(".delete-button");

  deleteBtns.forEach((btn) => {
    btn.addEventListener("click", (event) => {
      const site = event.target.name;
      fetch(`/api/sites/${site}`, {
        method: "DELETE"
      }).then((response) => {
        if (response.ok) {
          window.location.reload();
        }
      });
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
      }
    });
  });
})
