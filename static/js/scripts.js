function toggleSelection(checkbox, groupName) {
  // Select all checkboxes with the same name as the group
  const checkboxes = document.querySelectorAll(
    `input[type="checkbox"][name="${groupName}"]`
  );

  // Deselect other checkboxes in the group
  checkboxes.forEach((cb) => {
    if (cb !== checkbox) {
      cb.checked = false;
      cb.dataset.checked = "false";
    }
  });

  // Allow deselecting the same checkbox
  if (checkbox.dataset.checked === "true") {
    checkbox.checked = false;
    checkbox.dataset.checked = "false";
  } else {
    checkbox.dataset.checked = "true";
  }
}

document
  .getElementById("submitVoteButton")
  .addEventListener("click", function () {
    // Validate that both radio buttons are selected
    const headSelected = document.querySelector(
      'input[name="head_candidate"]:checked'
    );
    const chairmanSelected = document.querySelector(
      'input[name="chairman_candidate"]:checked'
    );

    if (!headSelected || !chairmanSelected) {
      // Show an alert if the user hasn't selected all required options
      alert("Please select a candidate from each position before submitting.");
    } else {
      // If both are selected, show the confirmation modal
      const confirmationModal = new bootstrap.Modal(
        document.getElementById("confirmationModal")
      );
      confirmationModal.show();
    }
  });

document.getElementById("confirmSubmit").addEventListener("click", function () {
  // Submit the form if the user confirms
  document.getElementById("voteForm").submit();
});

// Custom Alert
// function CustomAlert() {
//   this.alert = function (message, title) {
//     document.body.innerHTML =
//       document.body.innerHTML +
//       '<div id="dialogoverlay"></div><div id="dialogbox" class="slit-in-vertical"><div><div id="dialogboxhead"></div><div id="dialogboxbody"></div><div id="dialogboxfoot"></div></div></div>';

//     let dialogoverlay = document.getElementById("dialogoverlay");
//     let dialogbox = document.getElementById("dialogbox");

//     let winH = window.innerHeight;
//     dialogoverlay.style.height = winH + "px";

//     dialogbox.style.top = "100px";

//     dialogoverlay.style.display = "block";
//     dialogbox.style.display = "block";

//     document.getElementById("dialogboxhead").style.display = "block";

//     if (typeof title === "undefined") {
//       document.getElementById("dialogboxhead").style.display = "none";
//     } else {
//       document.getElementById("dialogboxhead").innerHTML =
//         '<i class="fa fa-exclamation-circle" aria-hidden="true"></i> ' + title;
//     }
//     document.getElementById("dialogboxbody").innerHTML = message;
//     document.getElementById("dialogboxfoot").innerHTML =
//       '<button class="pure-material-button-contained active" onclick="customAlert.ok()">OK</button>';
//   };

//   this.ok = function () {
//     document.getElementById("dialogbox").style.display = "none";
//     document.getElementById("dialogoverlay").style.display = "none";
//   };
// }

// let customAlert = new CustomAlert();
