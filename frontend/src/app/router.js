/**
 * Simple Router - маршрутизатор приложения
 * App layer
 */

import { RacesPage } from "../pages/RacesPage/index.js";
import { RaceDetailsPage } from "../pages/RaceDetailsPage/index.js";
import { JockeysPage } from "../pages/JockeysPage/index.js";
import { JockeyDetailsPage } from "../pages/JockeyDetailsPage/index.js";
import { HorsesPage } from "../pages/HorsesPage/index.js";
import { HorseDetailsPage } from "../pages/HorseDetailsPage/index.js";
import { createElement, clearElement } from "../shared/lib/utils.js";

export class Router {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.currentPage = null;
    this.routes = {
      "/": { handler: RacesPage, params: null },
      "/races/:id": { handler: RaceDetailsPage, params: ["id"] },
      "/jockeys": { handler: JockeysPage, params: null },
      "/jockeys/:id": { handler: JockeyDetailsPage, params: ["id"] },
      "/horses": { handler: HorsesPage, params: null },
      "/horses/:id": { handler: HorseDetailsPage, params: ["id"] },
    };
  }

  async navigate(hash) {
    const path = this.hashToPath(hash);
    const route = this.matchRoute(path);

    if (!route) {
      this.notFound();
      return;
    }

    try {
      clearElement(this.container);

      let page;
      if (route.params && route.params.length > 0) {
        const params = this.extractParams(path, route.pattern);
        page = await route.handler(...Object.values(params));
      } else {
        page = await route.handler();
      }

      this.container.appendChild(page);
      this.currentPage = page;
    } catch (error) {
      console.error("Router error:", error);
      this.container.innerHTML = `<div class="error">Ошибка загрузки страницы: ${error.message}</div>`;
    }
  }

  hashToPath(hash) {
    return hash.replace("#/", "/");
  }

  matchRoute(path) {
    for (const [pattern, route] of Object.entries(this.routes)) {
      if (this.pathMatches(path, pattern)) {
        return { ...route, pattern };
      }
    }
    return null;
  }

  pathMatches(path, pattern) {
    const pathParts = path.split("/").filter(Boolean);
    const patternParts = pattern.split("/").filter(Boolean);

    if (pathParts.length !== patternParts.length) {
      return false;
    }

    return pathParts.every((part, index) => {
      const patternPart = patternParts[index];
      return patternPart.startsWith(":") || part === patternPart;
    });
  }

  extractParams(path, pattern) {
    const pathParts = path.split("/").filter(Boolean);
    const patternParts = pattern.split("/").filter(Boolean);
    const params = {};

    pathParts.forEach((part, index) => {
      const patternPart = patternParts[index];
      if (patternPart.startsWith(":")) {
        const paramName = patternPart.slice(1);
        params[paramName] = part;
      }
    });

    return params;
  }

  notFound() {
    clearElement(this.container);
    this.container.innerHTML =
      '<div class="error-page"><h1>404 - Страница не найдена</h1></div>';
  }

  init() {
    window.addEventListener("hashchange", () => {
      const hash = window.location.hash || "#/";
      this.navigate(hash);
    });

    const hash = window.location.hash || "#/";
    this.navigate(hash);
  }
}
