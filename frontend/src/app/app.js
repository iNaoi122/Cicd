/**
 * App - инициализация приложения
 * App layer
 */

import { Header } from "../widgets/Header/index.js";
import { Router } from "./router.js";
import { createElement } from "../shared/lib/utils.js";

export function initApp() {
  const root = document.getElementById("app");

  // Очищаем старое содержимое
  root.innerHTML = "";

  // Создаем структуру приложения
  const appContainer = createElement("div", "app-container");

  const header = Header();
  appContainer.appendChild(header);

  const main = createElement("main", "main-content");
  main.id = "main";
  appContainer.appendChild(main);

  root.appendChild(appContainer);

  // Инициализируем роутер
  const router = new Router("main");
  router.init();
}
