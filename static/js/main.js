/* ============================================================
   main.js  —  Form Submission, Validation & UX
   ============================================================ */

// ── Password visibility toggle ──────────────────────────────
const toggleBtn = document.querySelector('.toggle-pw');
const pwInput   = document.getElementById('password');

if (toggleBtn && pwInput) {
  toggleBtn.addEventListener('click', () => {
    const isHidden = pwInput.type === 'password';
    pwInput.type = isHidden ? 'text' : 'password';
    toggleBtn.querySelector('.eye-open').style.display  = isHidden ? 'none'  : 'block';
    toggleBtn.querySelector('.eye-closed').style.display = isHidden ? 'block' : 'none';
  });
}

// ── Inline field validation ─────────────────────────────────
const rules = {
  phone:    { test: v => v.trim().length >= 7,
              msg:  'Please enter a valid phone number.' },
  username: { test: v => v.trim().length >= 3,
              msg:  'Username must be at least 3 characters.' },
  email:    { test: v => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()),
              msg:  'Please enter a valid email address.' },
  password: { test: v => v.length >= 6,
              msg:  'Password must be at least 6 characters.' },
};

function setFieldError(id, msg) {
  const group = document.getElementById('group-' + id);
  if (!group) return;
  const errEl = group.querySelector('.field-error');
  if (msg) {
    group.classList.add('has-error');
    if (errEl) errEl.textContent = msg;
  } else {
    group.classList.remove('has-error');
    if (errEl) errEl.textContent = '';
  }
}

// Validate on blur for each field
Object.keys(rules).forEach(id => {
  const el = document.getElementById(id);
  if (!el) return;
  el.addEventListener('blur', () => {
    if (!rules[id].test(el.value)) {
      setFieldError(id, rules[id].msg);
    }
  });
  el.addEventListener('input', () => {
    if (rules[id].test(el.value)) setFieldError(id, '');
  });
});

// ── Form submit ─────────────────────────────────────────────
const form    = document.getElementById('signup-form');
const formMsg = document.getElementById('form-msg');
const btnSubmit = document.getElementById('btn-submit');

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  // Clear previous messages
  formMsg.className = 'form-msg';
  formMsg.textContent = '';

  // Validate all fields before sending
  let valid = true;
  Object.keys(rules).forEach(id => {
    const el = document.getElementById(id);
    if (!el) return;
    if (!rules[id].test(el.value)) {
      setFieldError(id, rules[id].msg);
      valid = false;
    }
  });
  if (!valid) return;

  // Loading state
  btnSubmit.classList.add('loading');
  btnSubmit.disabled = true;

  try {
    const formData = new FormData(form);
    const res = await fetch('/submit', { method: 'POST', body: formData });
    const json = await res.json();

    if (json.status === 'success') {
      // Show success message
      formMsg.className = 'form-msg success';
      formMsg.textContent = json.message;

      // Reset form fields
      form.reset();
      Object.keys(rules).forEach(id => setFieldError(id, ''));

    } else {
      // Show server-side errors
      const msgs = Array.isArray(json.messages) ? json.messages : [json.messages];
      formMsg.className = 'form-msg error';
      formMsg.textContent = msgs.join(' ');
    }
  } catch (err) {
    formMsg.className = 'form-msg error';
    formMsg.textContent = 'Network error. Please try again.';
  } finally {
    btnSubmit.classList.remove('loading');
    btnSubmit.disabled = false;
  }
});

// ── Subtle card tilt on mouse move ──────────────────────────
const card = document.querySelector('.glass-card');
document.addEventListener('mousemove', (e) => {
  if (!card || window.innerWidth < 768) return;
  const rect = card.getBoundingClientRect();
  const cx   = rect.left + rect.width  / 2;
  const cy   = rect.top  + rect.height / 2;
  const dx   = (e.clientX - cx) / (window.innerWidth  / 2);
  const dy   = (e.clientY - cy) / (window.innerHeight / 2);
  card.style.transform = `perspective(900px) rotateY(${dx * 3}deg) rotateX(${-dy * 3}deg)`;
});
document.addEventListener('mouseleave', () => {
  if (card) card.style.transform = '';
});
