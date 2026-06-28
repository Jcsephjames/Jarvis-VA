const VERSION = "v1.0.0";

function updateClock() {
  const now = new Date();
  const time = now.toLocaleTimeString("en-GB", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    timeZone: "Europe/London"
  });

  document.getElementById("clock").textContent = `${time} UK`;
}

async function loadState() {
  try {
    const response = await fetch("state.json?cache=" + Date.now());
    const data = await response.json();

    const state = data.state || "idle";

    document.getElementById("onlineStatus").textContent = "ONLINE";
    document.getElementById("stateValue").textContent = state;
    document.getElementById("stateLabel").textContent = state.toUpperCase();

    document.querySelector(".top-bar div:first-child").textContent = `JARVIS OS ${VERSION}`;

    document.getElementById("updatedValue").textContent =
      data.last_updated ? new Date(data.last_updated).toLocaleTimeString("en-GB") : "--";

    const face = document.getElementById("face");
    face.className = "face " + state;

    if (data.transcript) {
      document.getElementById("transcript").textContent = data.transcript;
    }

    if (data.response) {
      document.getElementById("response").textContent = data.response;
    }
  } catch (error) {
    document.getElementById("onlineStatus").textContent = "OFFLINE";
    document.getElementById("stateValue").textContent = "offline";
    document.getElementById("stateLabel").textContent = "OFFLINE";
    document.getElementById("face").className = "face error";
  }
}

setInterval(updateClock, 1000);
setInterval(loadState, 250);

updateClock();
loadState();
