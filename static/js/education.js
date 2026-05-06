/* education.js — Form validation & submit */

const rules = {
  username:    { test: v => v.trim().length >= 1, msg: "Username chunao." },
  college_name:{ test: v => v.trim().length >= 2, msg: "College name likho." },
  degree:      { test: v => v.trim().length >= 1, msg: "Degree chunao." },
  year:        { test: v => v.trim().length >= 1, msg: "Year chunao." },
  city:        { test: v => v.trim().length >= 2, msg: "City likho." },
};

function setFieldError(id, msg) {
  const group = document.getElementById("group-" + id);
  if (!group) return;
  const errEl = group.querySelector(".field-error");
  if (msg) { group.classList.add("has-error"); if(errEl) errEl.textContent = msg; }
  else      { group.classList.remove("has-error"); if(errEl) errEl.textContent = ""; }
}

Object.keys(rules).forEach(id => {
  const el = document.getElementById(id);
  if (!el) return;
  el.addEventListener("blur",  () => { if (!rules[id].test(el.value)) setFieldError(id, rules[id].msg); });
  el.addEventListener("input", () => { if (rules[id].test(el.value))  setFieldError(id, ""); });
  el.addEventListener("change",() => { if (rules[id].test(el.value))  setFieldError(id, ""); });
});

const form    = document.getElementById("edu-form");
const formMsg = document.getElementById("form-msg");
const btn     = document.getElementById("btn-submit");

form.addEventListener("submit", async e => {
  e.preventDefault();
  formMsg.className = "form-msg";
  formMsg.textContent = "";

  let valid = true;
  Object.keys(rules).forEach(id => {
    const el = document.getElementById(id);
    if (!el) return;
    if (!rules[id].test(el.value)) { setFieldError(id, rules[id].msg); valid = false; }
  });
  if (!valid) return;

  btn.classList.add("loading"); btn.disabled = true;
  try {
    const res  = await fetch("/submit-education", { method:"POST", body: new FormData(form) });
    const json = await res.json();
    if (json.status === "success") {
      formMsg.className = "form-msg success";
      formMsg.textContent = json.message;
      form.reset();
      Object.keys(rules).forEach(id => setFieldError(id, ""));
    } else {
      formMsg.className = "form-msg error";
      formMsg.textContent = (json.messages||[json.message]).join(" ");
    }
  } catch {
    formMsg.className = "form-msg error";
    formMsg.textContent = "Network error. Try again.";
  } finally {
    btn.classList.remove("loading"); btn.disabled = false;
  }
});
