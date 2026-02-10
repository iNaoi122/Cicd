/**
 * CreateRace Feature - форма создания состязания
 * Features layer
 */

import { raceApi } from '../../../entities/race/index.js';
import { Button, Alert } from '../../../shared/ui/index.js';
import { createElement, addEventListener, clearElement } from '../../../shared/lib/utils.js';
import { eventBus } from '../../../shared/lib/eventBus.js';

export function createRaceForm() {
  const container = createElement('div', 'create-race-form');

  const form = createElement('form', 'form');
  form.innerHTML = `
    <h2>Добавить новое состязание</h2>

    <div class="input-wrapper">
      <label class="input-label">Дата состязания</label>
      <input type="date" name="date" class="input" required>
    </div>

    <div class="input-wrapper">
      <label class="input-label">Время проведения</label>
      <input type="time" name="time" class="input" required>
    </div>

    <div class="input-wrapper">
      <label class="input-label">Ипподром</label>
      <input type="text" name="hippodrome" class="input" required>
    </div>

    <div class="input-wrapper">
      <label class="input-label">Название (необязательно)</label>
      <input type="text" name="name" class="input">
    </div>

    <button type="submit" class="btn btn-primary">Создать состязание</button>
  `;

  const statusDiv = createElement('div');

  addEventListener(form, 'submit', async (e) => {
    e.preventDefault();

    const submitBtn = form.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Создание...';

    clearElement(statusDiv);

    try {
      const formData = new FormData(form);
      const data = {
        date: formData.get('date'),
        time: formData.get('time'),
        hippodrome: formData.get('hippodrome'),
        name: formData.get('name') || undefined,
      };

      await raceApi.createRace(data);

      const alert = Alert('Состязание успешно создано!', 'success');
      statusDiv.appendChild(alert);

      form.reset();
      eventBus.emit('race:created');

      setTimeout(() => {
        clearElement(statusDiv);
      }, 3000);
    } catch (error) {
      const alert = Alert('Ошибка: ' + error.message, 'error');
      statusDiv.appendChild(alert);
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Создать состязание';
    }
  });

  container.appendChild(form);
  container.appendChild(statusDiv);

  return container;
}
