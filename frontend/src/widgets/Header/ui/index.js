import { createElement } from '../../../shared/lib/utils.js';

export function Header() {
  const header = createElement('header', 'header');
  header.innerHTML = `
    <div class="header-container">
      <div class="header-logo">
        <a href="#/" class="logo-link">RaceTracker</a>
      </div>
      <nav class="header-nav">
        <a href="#/" class="nav-link">Состязания</a>
        <a href="#/jockeys" class="nav-link">Жокеи</a>
        <a href="#/horses" class="nav-link">Лошади</a>
      </nav>
    </div>
  `;
  return header;
}
