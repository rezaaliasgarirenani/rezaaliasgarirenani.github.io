(() => {
  'use strict';
  // Directory URLs are real static pages; normalize explicitly requested index files.
  const { pathname, search, hash } = window.location;
  if (pathname.endsWith('/index.html')) {
    history.replaceState(history.state, '', pathname.slice(0, -10) + search + hash);
  }
})();
