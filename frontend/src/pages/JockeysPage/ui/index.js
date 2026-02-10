import { jockeyApi } from "../../../entities/jockey/index.js";
import { Spinner, Alert } from "../../../shared/ui/index.js";
import { createElement, clearElement } from "../../../shared/lib/utils.js";

export async function JockeysPage() {
  const container = createElement("div", "page jockeys-page");
  const header = createElement("div", "page-header");
  header.innerHTML = "<h1>Жокеи</h1>";
  container.appendChild(header);

  const contentDiv = createElement("div", "page-content");
  const loadingDiv = createElement("div");
  loadingDiv.appendChild(Spinner());
  contentDiv.appendChild(loadingDiv);
  container.appendChild(contentDiv);

  async function loadJockeys() {
    try {
      clearElement(contentDiv);
      const loadingDiv = createElement("div");
      loadingDiv.appendChild(Spinner());
      contentDiv.appendChild(loadingDiv);

      const jockeys = await jockeyApi.getJockeys();
      clearElement(contentDiv);

      if (jockeys.length === 0) {
        contentDiv.innerHTML = '<p class="empty-message">Нет жокеев</p>';
      } else {
        const jockeysList = createElement("div", "jockeys-grid");
        jockeys.forEach((jockey) => {
          const card = createElement(
            "a",
            "jockey-card card",
            `
            <h3>${jockey.name}</h3>
            <p><span class="label">Возраст:</span> ${jockey.age}</p>
            <p><span class="label">Рейтинг:</span> ${jockey.rating}</p>
            <p><span class="label">Адрес:</span> ${jockey.address}</p>
          `,
          );
          card.href = `#/jockeys/${jockey.id}`;
          jockeysList.appendChild(card);
        });
        contentDiv.appendChild(jockeysList);
      }
    } catch (error) {
      clearElement(contentDiv);
      contentDiv.appendChild(
        Alert("Ошибка загрузки: " + error.message, "error"),
      );
    }
  }

  await loadJockeys();

  return container;
}
