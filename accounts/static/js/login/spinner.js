document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const submitButton = document.getElementById("submitButton");
    const spinner = document.getElementById("spinner");

    spinner.classList.remove("d-none");
    submitButton.setAttribute("disabled", "true");

    setTimeout(() => this.submit(), 1000);
});