import { horseApi } from '../../../entities/horse/index.js';
import { ownerApi } from '../../../entities/owner/index.js';
import { Alert, Spinner } from '../../../shared/ui/index.js';
import { createElement, addEventListener, clearElement } from '../../../shared/lib/utils.js';
import { eventBus } from '../../../shared/lib/eventBus.js';

export async function addHorseForm() {
  const container = createElement('div', 'add-horse-form');
  const spinnerDiv = createElement('div');
  spinnerDiv.appendChild(Spinner());
  container.appendChild(spinnerDiv);
  
  try {
    const owners = await ownerApi.getOwners();
    clearElement(container);
    
    const form = createElement('form', 'form');
    let ownerOptions = '<option value="">Выберите владельца</option>';
    owners.forEach(owner => {
      ownerOptions += `<option value="${owner.id}">${owner.name}</option>`;
    });
    
    form.innerHTML = `
      <h2>Добавить новую лошадь</h2>
      <div class="input-wrapper">
        <label class="input-label">Кличка</label>
        <input type="text" name="nickname" class="input" required>
      </div>
      <div class="input-wrapper">
        <label class="input-label">Пол</label>
        <select name="gender" class="select" required>
          <option value="">Выберите пол</option>
          <option value="жеребец">Жеребец</option>
          <option value="кобыла">Кобыла</option>
          <option value="мерин">Мерин</option>
        </select>
      </div>
      <div class="input-wrapper">
        <label class="input-label">Возраст</label>
        <input type="number" name="age" class="input" required>
      </div>
      <div class="input-wrapper">
        <label class="input-label">Владелец</label>
        <select name="owner_id" class="select" required>
          ${ownerOptions}
        </select>
      </div>
      <button type="submit" class="btn btn-primary">Добавить лошадь</button>
    `;
    
    const statusDiv = createElement('div');
    
    addEventListener(form, 'submit', async (e) => {
      e.preventDefault();
      const submitBtn = form.querySelector('button[type="submit"]');
      submitBtn.disabled = true;
      submitBtn.textContent = 'Добавление...';
      clearElement(statusDiv);
      
      try {
        const formData = new FormData(form);
        const data = {
          nickname: formData.get('nickname'),
          gender: formData.get('gender'),
          age: parseInt(formData.get('age')),
          owner_id: parseInt(formData.get('owner_id')),
        };
        
        await horseApi.createHorse(data);
        const alert = Alert('Лошадь успешно добавлена!', 'success');
        statusDiv.appendChild(alert);
        form.reset();
        eventBus.emit('horse:created');
        setTimeout(() => clearElement(statusDiv), 3000);
      } catch (error) {
        const alert = Alert('Ошибка: ' + error.message, 'error');
        statusDiv.appendChild(alert);
      } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Добавить лошадь';
      }
    });
    
    container.appendChild(form);
    container.appendChild(statusDiv);
  } catch (error) {
    clearElement(container);
    const alert = Alert('Ошибка загрузки владельцев: ' + error.message, 'error');
    container.appendChild(alert);
  }
  
  return container;
}
