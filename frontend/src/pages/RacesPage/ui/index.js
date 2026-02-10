import { raceApi } from '../../../entities/race/index.js';
import { Button, Modal, Spinner, Alert } from '../../../shared/ui/index.js';
import { createElement, clearElement } from '../../../shared/lib/utils.js';
import { RaceCard } from '../../../widgets/RaceCard/index.js';
import { createRaceForm } from '../../../features/CreateRace/index.js';
import { eventBus } from '../../../shared/lib/eventBus.js';

export async function RacesPage() {
  const container = createElement('div', 'page races-page');
  
  const header = createElement('div', 'page-header');
  header.innerHTML = '<h1>Состязания</h1>';
  const addBtn = Button('+ Добавить состязание', {
    className: 'btn-primary',
    onClick: () => showCreateModal(),
  });
  header.appendChild(addBtn);
  container.appendChild(header);
  
  const contentDiv = createElement('div', 'page-content');
  const loadingDiv = createElement('div');
  loadingDiv.appendChild(Spinner());
  contentDiv.appendChild(loadingDiv);
  container.appendChild(contentDiv);
  
  async function loadRaces() {
    try {
      clearElement(contentDiv);
      const loadingDiv = createElement('div');
      loadingDiv.appendChild(Spinner());
      contentDiv.appendChild(loadingDiv);
      
      const races = await raceApi.getRaces();
      clearElement(contentDiv);
      
      if (races.length === 0) {
        contentDiv.innerHTML = '<p class="empty-message">Нет состязаний</p>';
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
  }
  
  function showCreateModal() {
    const form = createRaceForm();
    const modal = Modal('Добавить новое состязание', form);
    const unsubscribe = eventBus.on('race:created', () => {
      modal.hide();
      loadRaces();
      unsubscribe();
    });
    modal.show();
  }
  
  await loadRaces();
  eventBus.on('race:created', () => {
    loadRaces();
  });
  
  return container;
}
