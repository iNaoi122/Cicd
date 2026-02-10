import { participantApi } from '../../../entities/participant/index.js';
import { raceApi } from '../../../entities/race/index.js';
import { jockeyApi } from '../../../entities/jockey/index.js';
import { horseApi } from '../../../entities/horse/index.js';
import { Alert, Spinner } from '../../../shared/ui/index.js';
import { createElement, addEventListener, clearElement } from '../../../shared/lib/utils.js';
import { eventBus } from '../../../shared/lib/eventBus.js';

export async function addRaceResultForm() {
  const container = createElement('div', 'add-race-result-form');
  const spinnerDiv = createElement('div');
  spinnerDiv.appendChild(Spinner());
  container.appendChild(spinnerDiv);
  
  try {
    const [races, jockeys, horses] = await Promise.all([
      raceApi.getRaces(),
      jockeyApi.getJockeys(),
      horseApi.getHorses(),
    ]);
    
    clearElement(container);
    
    const form = createElement('form', 'form');
    
    let racesOptions = '<option value="">Выберите состязание</option>';
    races.forEach(race => {
      const name = race.name || race.hippodrome;
      racesOptions += `<option value="${race.id}">${name} - ${race.date}</option>`;
    });
    
    let jockeysOptions = '<option value="">Выберите жокея</option>';
    jockeys.forEach(jockey => {
      jockeysOptions += `<option value="${jockey.id}">${jockey.name}</option>`;
    });
    
    let horsesOptions = '<option value="">Выберите лошадь</option>';
    horses.forEach(horse => {
      horsesOptions += `<option value="${horse.id}">${horse.nickname}</option>`;
    });
    
    form.innerHTML = `
      <h2>Добавить результат состязания</h2>
      <div class="input-wrapper">
        <label class="input-label">Состязание</label>
        <select name="race_id" class="select" required>
          ${racesOptions}
        </select>
      </div>
      <div class="input-wrapper">
        <label class="input-label">Жокей</label>
        <select name="jockey_id" class="select" required>
          ${jockeysOptions}
        </select>
      </div>
      <div class="input-wrapper">
        <label class="input-label">Лошадь</label>
        <select name="horse_id" class="select" required>
          ${horsesOptions}
        </select>
      </div>
      <div class="input-wrapper">
        <label class="input-label">Занятое место</label>
        <input type="number" name="place" class="input" min="1" required>
      </div>
      <div class="input-wrapper">
        <label class="input-label">Время прохождения (необязательно)</label>
        <input type="time" name="time_result" step="1" class="input">
      </div>
      <button type="submit" class="btn btn-primary">Добавить результат</button>
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
          race_id: parseInt(formData.get('race_id')),
          jockey_id: parseInt(formData.get('jockey_id')),
          horse_id: parseInt(formData.get('horse_id')),
          place: parseInt(formData.get('place')),
          time_result: formData.get('time_result') || undefined,
        };
        
        await participantApi.addParticipant(data);
        const alert = Alert('Результат успешно добавлен!', 'success');
        statusDiv.appendChild(alert);
        form.reset();
        eventBus.emit('participant:created');
        setTimeout(() => clearElement(statusDiv), 3000);
      } catch (error) {
        const alert = Alert('Ошибка: ' + error.message, 'error');
        statusDiv.appendChild(alert);
      } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Добавить результат';
      }
    });
    
    container.appendChild(form);
    container.appendChild(statusDiv);
  } catch (error) {
    clearElement(container);
    const alert = Alert('Ошибка загрузки данных: ' + error.message, 'error');
    container.appendChild(alert);
  }
  
  return container;
}
