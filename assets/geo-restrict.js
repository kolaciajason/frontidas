/**
 * Geo-restriction disabled (all countries allowed).
 */
(function () {
  document.documentElement.style.visibility = '';
  document.documentElement.removeAttribute('data-geo-pending');
})();

