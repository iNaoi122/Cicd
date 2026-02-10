import { raceApi } from '../../../entities/race/index.js';
import { Spinner, Alert } from '../../../shared/ui/index.js';
import { createElement, clearElement, formatDate } from '../../../shared/lib/utils.js';
import { ParticipantsList } from '../../../widgets/ParticipantsList/index.js';

export async function RaceDetailsPage(raceId) {
  const container = createElement('div', 'page race-details-page');
  const contentDiv = createElement('div');
  const loadingDiv = createElement('div');
  loadingDiv.appendChild(Spinner());
  contentDiv.appendChild(loadingDiv);
  container.appendChild(contentDiv);
  
  try {
    const data = await raceApi.getRaceWithParticipants(raceId);
    const { race, participants } = data;
    clearElement(contentDiv);
    
    const backBtn = createElement('button', 'btn-back', '← Назад');
    backBtn.addEventListener('click', () => {
      window.location.hash = '#/';
    });
    contentDiv.appendChild(backBtn);
    
    contentDiv.innerHTML += `
      <h1>${race.name || 'Состязание'}</h1>
      <div class="info-block">
        <div class="info-item">
          <span class="label">Дата:</span>
          <span>${formatDate(race.date)}</span>
        </div>
        <div class="info-item">
          <span class="label">Время:</span>
          <span>${race.time}</span>
        </div>
        <div class="info-item">
          <span class="label">Ипподром:</span>
          <span>${race.hippodrome}</span>
        </div>
      </div>
    `;
    
    contentDiv.appendChild(ParticipantsList(participants));
  } catch (error) {
    clearElement(contentDiv);
    contentDiv.appendChild(Alert('Ошибка загрузки: ' + error.message, 'error'));
  }
  
  return container;
}
