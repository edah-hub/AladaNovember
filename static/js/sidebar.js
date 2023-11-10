const sidebar = document.getElementById("sidebar");
const hamburgerIcon = document.getElementById("hamburgerIcon");


function handleBranchChange(selectElement) {
    var selectedValue = selectElement.value;
    if (selectedValue !== '') {
        window.location.href = selectedValue;
    }
}
hamburgerIcon.addEventListener("click", () => {
    sidebar.style.zIndex = "9999999"
    sidebar.classList.toggle("active")
});
const branchesDropdown = document.getElementById('branchesDropdown');
branchesDropdown.addEventListener('change', function() {
    const selectedValue = this.value;
    if (selectedValue !== '') {
        window.location.href = selectedValue;
    }
});
