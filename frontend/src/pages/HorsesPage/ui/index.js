import { horseApi } from '../../../entities/horse/index.js';
import { Button, Modal, Spinner, Alert } from '../../../shared/ui/index.js';
import { createElement, clearElement } from '../../../shared/lib/utils.js';
import { addHorseForm } from '../../../features/AddHorse/index.js';
import { eventBus } from '../../../shared/lib/eventBus.js';

export async function HorsesPage() {
  const container = createElement('div', 'page horses-page');
  const header = createElement('div', 'page-header');
  header.innerHTML = '<h1>Лошади</h1>';
  const addBtn = Button('+ Добавить лошадь', {
    className: 'btn-primary',
    onClick: () => showAddModal(),
  });
  header.appendChild(addBtn);
  container.appendChild(header);
  
  const contentDiv = createElement('div', 'page-content');
  const loadingDiv = createElement('div');
  loadingDiv.appendChild(Spinner());
  contentDiv.appendChild(loadingDiv);
  container.appendChild(contentDiv);
  
  async function loadHorses() {
    try {
      clearElement(contentDiv);
      const loadingDiv = createElement('div');
      loadingDiv.appendChild(Spinner());
      contentDiv.appendChild(loadingDiv);
      
      const horses = await horseApi.getHorses();
      clearElement(contentDiv);
      
      if (horses.length === 0) {
        contentDiv.innerHTML = '<p class="empty-message">Нет лошадей</p>';
      } else {
        const horsesList = createElement('div', 'horses-grid');
        horses.forEach(horse => {
          const card = createElement('a', 'horse-card card', `
            <h3>${horse.nickname}</h3>
            <p><span class="label">Пол:</span> ${horse.gender}</p>
            <p><span class="label">Возраст:</span> ${horse.age}</p>
            <p><span class="label">ID владельца:</span> ${horse.owner_id}</p>
          `);
          card.href = `#/horses/${horse.id}`;
          horsesList.appendChild(card);
        });
        contentDiv.appendChild(horsesList);
      }
    } catch (error) {
      clearElement(contentDiv);
      contentDiv.appendChild(Alert('Ошибка загрузки: ' + error.message, 'error'));
    }
  }
  
  async function showAddModal() {
    const form = await addHorseForm();
    const modal = Modal('Добавить новую лошадь', form);
    const unsubscribe = eventBus.on('horse:created', () => {
      modal.hide();
      loadHorses();
      unsubscribe();
    });
    modal.show();
  }
  
  await loadHorses();
  eventBus.on('horse:created', () => {
    loadHorses();
  });
  
  return container;
}
