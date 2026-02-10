import { createElement } from '../../../shared/lib/utils.js';

export function ParticipantsList(participants) {
  const container = createElement('div', 'participants-list');
  
  if (!participants || participants.length === 0) {
    container.innerHTML = '<p class="empty-message">Нет результатов</p>';
    return container;
  }
  
  let html = `
    <h3>Результаты состязания</h3>
    <div class="participants-table">
      <div class="table-header">
        <div class="table-cell">Место</div>
        <div class="table-cell">Жокей</div>
        <div class="table-cell">Лошадь</div>
        <div class="table-cell">Время</div>
      </div>
  `;
  
  participants.forEach(participant => {
    html += `
      <div class="table-row">
        <div class="table-cell">
          <span class="place-badge">${participant.place}</span>
        </div>
        <div class="table-cell">${participant.jockey_name}</div>
        <div class="table-cell">${participant.horse_name}</div>
        <div class="table-cell">${participant.time_result || '—'}</div>
      </div>
    `;
  });
  
  html += '</div>';
  container.innerHTML = html;
  return container;
}
