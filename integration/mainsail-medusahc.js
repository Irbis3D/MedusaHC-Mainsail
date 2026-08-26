(() => {
  const linkId = 'medusahc-nav-link';
  const viewId = 'medusahc-main-view';

  function panelUrl() {
    return `${window.location.protocol}//${window.location.hostname}:8090/`;
  }

  function positionView(view) {
    const main = document.querySelector('.v-main');
    if (!main) return;
    const style = getComputedStyle(main);
    const left = Number.parseFloat(style.paddingLeft) || 0;
    const right = Number.parseFloat(style.paddingRight) || 0;
    const top = Number.parseFloat(style.paddingTop) || 0;
    const bottom = Number.parseFloat(style.paddingBottom) || 0;
    Object.assign(view.style, {
      left: `${left}px`,
      top: `${top}px`,
      width: `${Math.max(0, window.innerWidth - left - right)}px`,
      height: `${Math.max(0, window.innerHeight - top - bottom)}px`,
    });
  }

  function getView() {
    let view = document.getElementById(viewId);
    if (view) return view;
    view = document.createElement('section');
    view.id = viewId;
    view.hidden = true;
    view.style.cssText = 'position:fixed;z-index:5;background:#090d14;overflow:hidden';
    const frame = document.createElement('iframe');
    frame.src = panelUrl();
    frame.title = 'MedusaHC';
    frame.style.cssText = 'display:block;width:100%;height:100%;border:0;background:#090d14';
    view.appendChild(frame);
    document.body.appendChild(view);
    window.addEventListener('resize', () => positionView(view));
    return view;
  }

  function openPanel(event) {
    event.preventDefault();
    event.stopPropagation();
    const view = getView();
    positionView(view);
    view.hidden = false;
    document.querySelectorAll(
      '.v-navigation-drawer .active-nav-item, .v-navigation-drawer .v-list-item--active'
    ).forEach((item) => item.classList.remove('active-nav-item', 'v-list-item--active'));
    document.getElementById(linkId)?.classList.add('active-nav-item');
  }

  function closePanel() {
    const view = document.getElementById(viewId);
    if (view) view.hidden = true;
    document.getElementById(linkId)?.classList.remove('active-nav-item', 'v-list-item--active');
  }

  function installLink() {
    if (document.getElementById(linkId)) return true;
    const list = document.querySelector('.v-navigation-drawer .v-list');
    const template = list?.querySelector('.v-list-item');
    if (!list || !template) return false;
    const link = template.cloneNode(true);
    link.id = linkId;
    link.classList.remove('active-nav-item', 'v-list-item--active');
    link.removeAttribute('href');
    link.removeAttribute('aria-current');
    link.setAttribute('role', 'button');
    link.setAttribute('aria-label', 'MedusaHC');
    const title = link.querySelector('.v-list-item__title');
    if (title) title.textContent = 'MedusaHC';
    link.addEventListener('click', openPanel);
    list.appendChild(link);
    return true;
  }

  document.addEventListener('click', (event) => {
    const navItem = event.target.closest('.v-navigation-drawer .v-list-item');
    if (navItem && navItem.id !== linkId) closePanel();
  }, true);
  const observer = new MutationObserver(installLink);
  observer.observe(document.documentElement, { childList: true, subtree: true });
  installLink();
})();
