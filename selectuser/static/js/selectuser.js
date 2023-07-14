let buttonSelectUser = document.getElementById("select_User");
let buttonGetInfo = document.getElementById("infoButton")

buttonSelectUser.onclick = function () {
    BX24.selectUser(function (res) {
        buttonSelectUser.innerHTML = res['name'];
        buttonSelectUser.style.backgroundColor = 'red';
        buttonGetInfo.disabled = false;
        buttonGetInfo.value = res['id'];
    })
}