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

const fetchData = async () => {
  try {
    const accessToken = window.localStorage.getItem("token");
    const res = await fetch("/profile", {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    const data = await res.json(); // 응답 데이터를 JSON으로 변환
    const div = document.querySelector("#info");
    div.innerText = data.id;
  } catch (error) {
    console.error("데이터를 가져오는 데 오류가 발생했습니다:", error);
  }
};

fetchData();
