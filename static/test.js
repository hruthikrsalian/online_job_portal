let QUESTIONS = [];
let current = 0;
let answers = {};
let time = 1500;

let isFullscreen = false;

function startTest() {
  document.documentElement.requestFullscreen();
  document.getElementById("fsOverlay").style.display = "none";
  isFullscreen = true;
}

// ---------- FORCE FULLSCREEN ON START ----------
window.onload = () => {
  alert("This test requires full-screen mode. Click OK to start.");
  document.documentElement.requestFullscreen();
};

// Detect fullscreen
document.addEventListener("fullscreenchange", () => {
  if (!document.fullscreenElement && isFullscreen) {
    alert("You exited full-screen. Test will be submitted.");
    document.getElementById("testForm").submit();
  }
});


// ---------- LOAD QUESTIONS ----------
fetch("/api/questions")
  .then(res => res.json())
  .then(data => {
    QUESTIONS = data;
    buildPalette();
    showQuestion();
  });

// ---------- QUESTION LOGIC ----------
function showQuestion() {
  const q = QUESTIONS[current];

  document.getElementById("questionNumber").innerText =
    `Question ${current + 1} of ${QUESTIONS.length}`;

  document.getElementById("questionText").innerText = q[2];
  document.getElementById("optA").innerText = q[3];
  document.getElementById("optB").innerText = q[4];
  document.getElementById("optC").innerText = q[5];
  document.getElementById("optD").innerText = q[6];

  document.querySelectorAll("input[name='answer']").forEach(r => {
    r.checked = (answers[q[0]] === r.value);
  });
}

function nextQuestion() {
  saveAnswer();
  if (current < QUESTIONS.length - 1) {
    current++;
    showQuestion();
  }
}

function prevQuestion() {
  saveAnswer();
  if (current > 0) {
    current--;
    showQuestion();
  }
}

function jumpTo(i) {
  saveAnswer();
  current = i;
  showQuestion();
}

function saveAnswer() {
  const qid = QUESTIONS[current][0];
  const selected = document.querySelector("input[name='answer']:checked");
  if (selected) {
    answers[qid] = selected.value;
  }
  updatePalette();
  renderHiddenInputs();
}

// ---------- PALETTE ----------
function buildPalette() {
  const boxDiv = document.getElementById("paletteBoxes");
  for (let i = 0; i < QUESTIONS.length; i++) {
    const box = document.createElement("div");
    box.className = "palette-box";
    box.innerText = i + 1;
    box.onclick = () => jumpTo(i);
    box.id = "box-" + i;
    boxDiv.appendChild(box);
  }
}

function updatePalette() {
  QUESTIONS.forEach((q, i) => {
    const box = document.getElementById("box-" + i);
    if (answers[q[0]]) {
      box.classList.add("answered");
    }
  });
}

// ---------- SUBMIT DATA ----------
function renderHiddenInputs() {
  const container = document.getElementById("hiddenAnswers");
  container.innerHTML = "";
  for (let qid in answers) {
    container.innerHTML +=
      `<input type="hidden" name="${qid}" value="${answers[qid]}">`;
  }
}

// ---------- TIMER ----------
setInterval(() => {
  let min = Math.floor(time / 60);
  let sec = time % 60;
  document.getElementById("timer").innerText =
    `Time Left: ${min}:${sec < 10 ? "0" + sec : sec}`;
  time--;
  if (time <= 0) {
    alert("Time over. Auto submitting.");
    document.getElementById("testForm").submit();
  }
}, 1000);

// ---------- HARD ANTI-CHEAT ----------
document.addEventListener("visibilitychange", () => {
  if (document.hidden) {
    alert("Tab switch detected. Submitting test.");
    document.getElementById("testForm").submit();
  }
});

document.addEventListener("contextmenu", e => e.preventDefault());
document.addEventListener("keydown", e => {
  if (e.key === "F12" || (e.ctrlKey && e.shiftKey && e.key === "I")) {
    e.preventDefault();
    alert("Developer tools disabled.");
  }
});
