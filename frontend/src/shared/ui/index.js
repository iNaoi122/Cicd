/**
 * UI Components - базовые компоненты интерфейса
 */

import { createElement, setAttributes, addEventListener } from '../lib/utils.js';

export function Button(text, options = {}) {
  const button = createElement('button', 'btn ' + (options.className || ''));
  button.textContent = text;

  if (options.onClick) {
    addEventListener(button, 'click', options.onClick);
  }

  if (options.disabled) {
    button.disabled = true;
  }

  if (options.title) {
    button.title = options.title;
  }

  return button;
}

export function Input(options = {}) {
  const wrapper = createElement('div', 'input-wrapper');

  if (options.label) {
    const label = createElement('label', 'input-label');
    label.textContent = options.label;
    wrapper.appendChild(label);
  }

  const input = createElement('input');
  input.type = options.type || 'text';
  if (options.name) input.name = options.name;
  if (options.value) input.value = options.value;
  if (options.placeholder) input.placeholder = options.placeholder;
  if (options.required) input.required = true;
  if (options.className) input.className = 'input ' + options.className;
  else input.className = 'input';

  wrapper.appendChild(input);
  return { wrapper, input };
}

export function Select(options = {}) {
  const wrapper = createElement('div', 'select-wrapper');

  if (options.label) {
    const label = createElement('label', 'select-label');
    label.textContent = options.label;
    wrapper.appendChild(label);
  }

  const select = createElement('select');
  select.className = 'select';
  if (options.name) select.name = options.name;
  if (options.required) select.required = true;

  if (options.options) {
    options.options.forEach(({ value, text, selected }) => {
      const option = createElement('option');
      option.value = value;
      option.textContent = text;
      if (selected) option.selected = true;
      select.appendChild(option);
    });
  }

  wrapper.appendChild(select);
  return { wrapper, select };
}

export function Card(content = '', className = '') {
  const card = createElement('div', 'card ' + className);
  if (typeof content === 'string') {
    card.innerHTML = content;
  } else {
    card.appendChild(content);
  }
  return card;
}

export function Modal(title, content) {
  const overlay = createElement('div', 'modal-overlay');
  const modal = createElement('div', 'modal');

  const header = createElement('div', 'modal-header');
  const headerTitle = createElement('h2', 'modal-title');
  headerTitle.textContent = title;
  header.appendChild(headerTitle);

  const closeBtn = createElement('button', 'modal-close');
  closeBtn.innerHTML = '&times;';
  closeBtn.setAttribute('type', 'button');
  header.appendChild(closeBtn);

  const body = createElement('div', 'modal-body');
  if (typeof content === 'string') {
    body.innerHTML = content;
  } else {
    body.appendChild(content);
  }

  modal.appendChild(header);
  modal.appendChild(body);
  overlay.appendChild(modal);

  const show = () => {
    document.body.appendChild(overlay);
    document.body.style.overflow = 'hidden';
  };

  const hide = () => {
    overlay.remove();
    document.body.style.overflow = '';
  };

  addEventListener(closeBtn, 'click', hide);
  addEventListener(overlay, 'click', (e) => {
    if (e.target === overlay) hide();
  });

  return { overlay, modal, show, hide };
}

export function Spinner() {
  return createElement('div', 'spinner', '<div class="spinner-inner"></div>');
}

export function Alert(message, type = 'info') {
  const alert = createElement('div', `alert alert-${type}`);
  alert.textContent = message;
  return alert;
}

export function Form(fields, onSubmit) {
  const form = createElement('form', 'form');
  const fieldElements = {};

  fields.forEach(field => {
    const { wrapper, input } = Input({
      label: field.label,
      type: field.type || 'text',
      name: field.name,
      placeholder: field.placeholder,
      required: field.required,
    });
    fieldElements[field.name] = input;
    form.appendChild(wrapper);
  });

  const submitBtn = Button('Отправить', { className: 'btn-primary' });
  form.appendChild(submitBtn);

  addEventListener(form, 'submit', (e) => {
    e.preventDefault();
    const formData = {};
    Object.keys(fieldElements).forEach(name => {
      formData[name] = fieldElements[name].value;
    });
    if (onSubmit) onSubmit(formData);
  });

  return { form, fieldElements };
}
