function toggleSelection(radio) {
  const radios = document.querySelectorAll(
    'input[type="radio"][name="candidate"]'
  );
  radios.forEach((r) => {
    if (r !== radio) r.checked = false;
  });
  // Allow deselecting the same radio
  if (radio.dataset.checked === "true") {
    radio.checked = false;
    radio.dataset.checked = "false";
  } else {
    radio.dataset.checked = "true";
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
      alert("Please select a candidate for both positions before submitting.");
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
