import { createElement } from '../../../shared/lib/utils.js';
import { formatDate } from '../../../shared/lib/utils.js';

export function RaceCard(race) {
  const card = createElement('a', 'race-card', `
    <div class="card">
      <h3>${race.name || 'Состязание'}</h3>
      <p><span class="label">Дата:</span> ${formatDate(race.date)}</p>
      <p><span class="label">Время:</span> ${race.time}</p>
      <p><span class="label">Ипподром:</span> ${race.hippodrome}</p>
    </div>
  `);
  card.href = `#/races/${race.id}`;
  return card;
}
