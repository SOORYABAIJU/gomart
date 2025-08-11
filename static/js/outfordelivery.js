const selectBox = document.getElementById("selectBox");
const optionsWrapper = document.getElementById("optionsWrapper");
const searchBox = document.getElementById("searchBox");
const optionsList = document.getElementById("optionsList");

selectBox.addEventListener("click", () => {
  optionsWrapper.classList.toggle("active");
  searchBox.value = "";
  filterOptions("");
});

searchBox.addEventListener("input", (e) => {
  filterOptions(e.target.value.toLowerCase());
});

optionsList.addEventListener("click", (e) => {
  if (e.target.tagName === "LI") {
    selectBox.textContent = e.target.textContent;
    optionsWrapper.classList.remove("active");
  }
});

function filterOptions(searchTerm) {
  const options = optionsList.querySelectorAll("li");
  options.forEach((opt) => {
    opt.style.display = opt.textContent.toLowerCase().includes(searchTerm)
      ? "block"
      : "none";
  });
}
