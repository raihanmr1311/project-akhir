const navLinks = document.querySelectorAll(".nav-link");
const navBar = document.querySelector(".navbar-nav");

navBar.addEventListener("click", function (e) {
  navLinks.forEach((i) => {
    i.classList.remove("active");
    if (i.className === e.target.className) {
      e.target.classList.add("active");
    }
  });
});