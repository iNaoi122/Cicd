import { horseApi } from "../../../entities/horse/index.js";
import { Spinner, Alert } from "../../../shared/ui/index.js";
import { createElement, clearElement } from "../../../shared/lib/utils.js";

export async function HorsesPage() {
  const container = createElement("div", "page horses-page");
  const header = createElement("div", "page-header");
  header.innerHTML = "<h1>Лошади</h1>";
  container.appendChild(header);

  const contentDiv = createElement("div", "page-content");
  const loadingDiv = createElement("div");
  loadingDiv.appendChild(Spinner());
  contentDiv.appendChild(loadingDiv);
  container.appendChild(contentDiv);

  async function loadHorses() {
    try {
      clearElement(contentDiv);
      const loadingDiv = createElement("div");
      loadingDiv.appendChild(Spinner());
      contentDiv.appendChild(loadingDiv);

      const horses = await horseApi.getHorses();
      clearElement(contentDiv);

      if (horses.length === 0) {
        contentDiv.innerHTML = '<p class="empty-message">Нет лошадей</p>';
      } else {
        const horsesList = createElement("div", "horses-grid");
        horses.forEach((horse) => {
          const card = createElement(
            "a",
            "horse-card card",
            `
            <h3>${horse.nickname}</h3>
            <p><span class="label">Пол:</span> ${horse.gender}</p>
            <p><span class="label">Возраст:</span> ${horse.age}</p>
            <p><span class="label">ID владельца:</span> ${horse.owner_id}</p>
          `,
          );
          card.href = `#/horses/${horse.id}`;
          horsesList.appendChild(card);
        });
        contentDiv.appendChild(horsesList);
      }
    } catch (error) {
      clearElement(contentDiv);
      contentDiv.appendChild(
        Alert("Ошибка загрузки: " + error.message, "error"),
      );
    }
  }

  await loadHorses();

  return container;
}
