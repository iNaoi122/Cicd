import { horseApi } from '../../../entities/horse/index.js';
import { Spinner, Alert } from '../../../shared/ui/index.js';
import { createElement, clearElement } from '../../../shared/lib/utils.js';
import { RaceCard } from '../../../widgets/RaceCard/index.js';

export async function HorseDetailsPage(horseId) {
  const container = createElement('div', 'page horse-details-page');
  const contentDiv = createElement('div');
  const loadingDiv = createElement('div');
  loadingDiv.appendChild(Spinner());
  contentDiv.appendChild(loadingDiv);
  container.appendChild(contentDiv);
  
  try {
    const [horse, races] = await Promise.all([
      horseApi.getHorseById(horseId),
      horseApi.getHorseRaces(horseId),
    ]);
    
    clearElement(contentDiv);
    const backBtn = createElement('button', 'btn-back', '← Назад');
    backBtn.addEventListener('click', () => {
      window.location.hash = '#/horses';
    });
    contentDiv.appendChild(backBtn);
    
    contentDiv.innerHTML += `
      <h1>${horse.nickname}</h1>
      <div class="info-block">
        <div class="info-item"><span class="label">Пол:</span><span>${horse.gender}</span></div>
        <div class="info-item"><span class="label">Возраст:</span><span>${horse.age}</span></div>
        <div class="info-item"><span class="label">ID владельца:</span><span>${horse.owner_id}</span></div>
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
