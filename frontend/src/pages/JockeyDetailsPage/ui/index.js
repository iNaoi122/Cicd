import { jockeyApi } from '../../../entities/jockey/index.js';
import { Spinner, Alert } from '../../../shared/ui/index.js';
import { createElement, clearElement } from '../../../shared/lib/utils.js';
import { RaceCard } from '../../../widgets/RaceCard/index.js';

export async function JockeyDetailsPage(jockeyId) {
  const container = createElement('div', 'page jockey-details-page');
  const contentDiv = createElement('div');
  const loadingDiv = createElement('div');
  loadingDiv.appendChild(Spinner());
  contentDiv.appendChild(loadingDiv);
  container.appendChild(contentDiv);
  
  try {
    const [jockey, races] = await Promise.all([
      jockeyApi.getJockeyById(jockeyId),
      jockeyApi.getJockeyRaces(jockeyId),
    ]);
    
    clearElement(contentDiv);
    const backBtn = createElement('button', 'btn-back', '← Назад');
    backBtn.addEventListener('click', () => {
      window.location.hash = '#/jockeys';
    });
    contentDiv.appendChild(backBtn);
    
    contentDiv.innerHTML += `
      <h1>${jockey.name}</h1>
      <div class="info-block">
        <div class="info-item"><span class="label">Возраст:</span><span>${jockey.age}</span></div>
        <div class="info-item"><span class="label">Рейтинг:</span><span>${jockey.rating}</span></div>
        <div class="info-item"><span class="label">Адрес:</span><span>${jockey.address}</span></div>
      </div>
      <h2>История состязаний</h2>
    `;
    
    if (races.length === 0) {
      contentDiv.innerHTML += '<p class="empty-message">Нет состязаний</p>';
    } else {
      const racesList = createElement('div', 'races-list');
      races.forEach(race => {
        racesList.appendChild(RaceCard(race));
      });
      contentDiv.appendChild(racesList);
    }
  } catch (error) {
    clearElement(contentDiv);
    contentDiv.appendChild(Alert('Ошибка загрузки: ' + error.message, 'error'));
  }
  
  return container;
}
