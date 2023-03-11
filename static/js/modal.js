// モーダルを表示させる
const eventBtn = document.getElementById("confirmation-btn");
const eventModal = document.getElementById("confirmation-modal");
const eventCloseBtn = document.getElementById("modal-close-btn");

// モーダルを開く
function modalOpen(mode) {
  if (mode === "event") {
    eventModal.style.display = "block";
  }
}

eventBtn.addEventListener("click", () => {
  modalOpen("event");
});

// モーダルを閉じる
function modalClose(mode) {
  if (mode === "event") {
    eventModal.style.display = "none";
  }
}

// モーダル内のキャンセルがクリックされた時
eventCloseBtn.addEventListener("click", () => {
  modalClose("event");
});

// モーダルコンテンツ以外がクリックされた時
addEventListener("click", outsideClose);
function outsideClose(e) {
  if (e.target == eventModal) {
    eventModal.style.display = "none";
  }
}

