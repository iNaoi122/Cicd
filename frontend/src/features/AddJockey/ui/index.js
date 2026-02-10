import { jockeyApi } from "../../../entities/jockey/index.js";
import { Alert } from "../../../shared/ui/index.js";
import {
  createElement,
  addEventListener,
  clearElement,
} from "../../../shared/lib/utils.js";
import { eventBus } from "../../../shared/lib/eventBus.js";

export function addJockeyForm() {
  const container = createElement("div", "add-jockey-form");

  const form = createElement("form", "form");
  form.innerHTML = `
    <h2>Добавить нового жокея</h2>
    <div class="input-wrapper">
      <label class="input-label">ФИО</label>
      <input type="text" name="name" class="input" required>
    </div>
    <div class="input-wrapper">
      <label class="input-label">Адрес</label>
      <input type="text" name="address" class="input" required>
    </div>
    <div class="input-wrapper">
      <label class="input-label">Возраст</label>
      <input type="number" name="age" class="input" required>
    </div>
    <div class="input-wrapper">
      <label class="input-label">Рейтинг</label>
      <input type="number" name="rating" min="0" class="input" required>
    </div>
    <button type="submit" class="btn btn-primary">Добавить жокея</button>
  `;

  const statusDiv = createElement("div");

  addEventListener(form, "submit", async (e) => {
    e.preventDefault();
    const submitBtn = form.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    submitBtn.textContent = "Добавление...";
    clearElement(statusDiv);

    try {
      const formData = new FormData(form);
      const data = {
        name: formData.get("name"),
        address: formData.get("address"),
        age: parseInt(formData.get("age")),
        rating: parseInt(formData.get("rating")),
      };

      await jockeyApi.createJockey(data);
      const alert = Alert("Жокей успешно добавлен!", "success");
      statusDiv.appendChild(alert);
      form.reset();
      eventBus.emit("jockey:created");
      setTimeout(() => clearElement(statusDiv), 3000);
    } catch (error) {
      const alert = Alert("Ошибка: " + error.message, "error");
      statusDiv.appendChild(alert);
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = "Добавить жокея";
    }
  });

  container.appendChild(form);
  container.appendChild(statusDiv);
  return container;
}
