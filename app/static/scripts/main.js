const signUpButton = document.getElementById("signUp");
const signInButton = document.getElementById("signIn");
const container = document.getElementById("container");
const main_signup = document.getElementById("main_signup");
const down = document.getElementById("down");
const body = document.querySelector("body");
const data_container = document.querySelector(".data-container");
const download_container = document.querySelector(".download-container");

signUpButton.addEventListener("click", () => {
  container.classList.add("right-panel-active");
  body.classList.add("right-panel-active");
  // showData.classList.add("active");
});

signInButton.addEventListener("click", () => {
  container.classList.remove("right-panel-active");
  body.classList.remove("right-panel-active");
});

main_signup.addEventListener("click", () => {
  data_container.classList.add("active");
});

down.addEventListener("click", () => {
  download_container.classList.add("active-download");
});

// add event listeners
document.querySelector("#dept").addEventListener("change", getSubjects);

document.querySelectorAll('input[name="sem"]').forEach(function (radio) {
  radio.addEventListener("change", getSubjects);
});

document.querySelectorAll('input[name="clgyear"]').forEach(function (radio) {
  radio.addEventListener("change", getSubjects);
});

async function getSubjects() {
  const dept = document.querySelector("#dept").value;
  const clgyear = document.querySelector('input[name="clgyear"]:checked').value;

  const sem = document.querySelector('input[name="sem"]:checked').value;

  const response = await fetch(`/subjects?dept=${dept}&year=${clgyear}&sem=${sem}`);
  const subjects = await response.json();
  updateSubjectOptions(subjects);
}

function updateSubjectOptions(subjects) {
  const select = document.querySelector("#subject");
  select.innerHTML = "";
  subjects.forEach(function (subject) {
    const option = document.createElement("option");
    option.value = subject;
    option.textContent = subject;
    select.appendChild(option);
  });
}

async function sendFiles() {
  const selectedFiles = Array.from(document.querySelectorAll('input[name="file"]:checked')).map(function (checkbox) {
    return checkbox.value;
  });

  const email_id = prompt("Please enter your college email ID.");
  if (!email_id || !email_id.endsWith("mail.jiit.ac.in")) {
    alert("Invalid Email.");
  } else {
    try {
      const response = await fetch(`/send-pdf`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email_id,
          files: selectedFiles,
        }),
      });

      alert("We have delivered the requested files to your Email. Have fun!");
      // Handle response here
    } catch (error) {
      console.error(error);
    }
  }
}

async function getFiles() {
  const dept = document.querySelector("#dept").value;
  const clgyear = document.querySelector('input[name="clgyear"]:checked').value;
  const sem = document.querySelector('input[name="sem"]:checked').value;
  const exam = document.querySelector('input[name="exam"]:checked').value;
  const subject = document.querySelector("#subject").value;

  const response = await fetch(`/get-files?dept=${dept}&year=${clgyear}&sem=${sem}&exam=${exam}&subject=${subject}`);

  const data = await response.json();

  const fileContainer = document.querySelector(".download-container");
  // convertToFlex(fileContainer);
  fileContainer.innerHTML = "";

  const break_line = document.createElement("br");
  if (data.length === 0) {
    fileContainer.textContent = "No results found.";
  } else {
    data.forEach(function (file) {
      const label = document.createElement("label");
      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.name = "file";
      checkbox.value = file;
      label.appendChild(checkbox);
      label.appendChild(document.createTextNode(file));
      fileContainer.appendChild(label);
      fileContainer.appendChild(document.createElement("br"));
    });

    const selectAllButton = document.createElement("button");
    selectAllButton.textContent = "Select All";
    selectAllButton.addEventListener("click", function () {
      document.querySelectorAll('input[name="file"]').forEach(function (checkbox) {
        checkbox.checked = true;
      });
    });
    fileContainer.appendChild(selectAllButton);

    const downloadButton = document.createElement("button");

    downloadButton.textContent = "Download Selected";
    downloadButton.addEventListener("click", function () {
      const selectedFiles = Array.from(document.querySelectorAll('input[name="file"]:checked')).map(function (checkbox) {
        return checkbox.value;
      });
      if (selectedFiles.length > 0) {
        // Make post request with selected files
        sendFiles();
      } else {
        alert("No files selected!");
      }
      download_container.classList.add("scroll-download");
    });
    fileContainer.appendChild(downloadButton);
  }

  // const container = document.querySelector(".form-container");
  // container.appendChild(fileContainer);
}

getSubjects();
