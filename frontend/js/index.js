document.addEventListener("DOMContentLoaded", () => {
  const loginBtn = document.getElementById("menu-bar__login");

  // 로그인 버튼이 존재할 때만 이벤트 추가
  if (loginBtn) {
    const moveToLogin = () => {
      window.location.pathname = "/login.html";
    };

    loginBtn.addEventListener("click", moveToLogin);
  }
});
