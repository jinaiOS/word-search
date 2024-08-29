const form = document.querySelector("#login-form");
const signup = document.getElementById("signup");

let accessToken = null;

const handleSubmit = async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const sha256Password = sha256(formData.get("password"));
  formData.set("password", sha256Password);
  console.log(formData);

  const div = document.querySelector("#info");

  const res = await fetch("/login", {
    method: "POST",
    body: formData,
  });

  const data = await res.json();
  const accessToken = data.access_token;
  window.localStorage.setItem("token", accessToken);
  alert("로그인되었습니다!!");

  window.location.pathname = "/";
};

const moveToSignup = () => {
  window.location.pathname = "/signup.html";
};

form.addEventListener("submit", handleSubmit);

if (signup) {
  signup.addEventListener("click", moveToSignup);
}
