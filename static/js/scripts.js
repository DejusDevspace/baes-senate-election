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
