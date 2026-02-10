/**
 * Утилиты для работы с DOM и данными
 */

export function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString('ru-RU');
}

export function getElementById(id) {
  return document.getElementById(id);
}

export function querySelector(selector) {
  return document.querySelector(selector);
}

export function querySelectorAll(selector) {
  return document.querySelectorAll(selector);
}

export function createElement(tag, className = '', innerHTML = '') {
  const element = document.createElement(tag);
  if (className) element.className = className;
  if (innerHTML) element.innerHTML = innerHTML;
  return element;
}

export function addClass(element, className) {
  element.classList.add(className);
}

export function removeClass(element, className) {
  element.classList.remove(className);
}

export function toggleClass(element, className) {
  element.classList.toggle(className);
}

export function setAttributes(element, attrs) {
  Object.keys(attrs).forEach((key) => {
    element.setAttribute(key, attrs[key]);
  });
}

export function addEventListener(element, event, handler) {
  if (element) {
    element.addEventListener(event, handler);
  }
}

export function removeEventListener(element, event, handler) {
  if (element) {
    element.removeEventListener(event, handler);
  }
}

export function showElement(element) {
  if (element) element.style.display = '';
}

export function hideElement(element) {
  if (element) element.style.display = 'none';
}

export function setInnerHTML(element, html) {
  if (element) element.innerHTML = html;
}

export function setTextContent(element, text) {
  if (element) element.textContent = text;
}

export function clearElement(element) {
  if (element) element.innerHTML = '';
}

export function findParent(element, selector) {
  return element.closest(selector);
}

export function getFormData(formElement) {
  const formData = new FormData(formElement);
  const data = {};
  for (let [key, value] of formData.entries()) {
    data[key] = value;
  }
  return data;
}

export function debounce(func, delay) {
  let timeoutId;
  return function (...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func.apply(this, args), delay);
  };
}

export function escapeHtml(text) {
  const map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;',
  };
  return text.replace(/[&<>"']/g, (m) => map[m]);
}
