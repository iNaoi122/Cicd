/**
 * Main entry point - инициализация приложения
 */

console.log("📥 main.js: Начало загрузки...");

async function startApp() {
  console.log("✅ Начинаем инициализацию приложения...");

  try {
    console.log("📦 Импортируем app.js...");
    const { initApp } = await import("./app/app.js");
    console.log("✅ app.js загружен");

    if (typeof initApp !== "function") {
      throw new Error("initApp не является функцией!");
    }

    console.log("🚀 Запускаем initApp()...");
    initApp();
    console.log("✅ Приложение успешно инициализировано!");
  } catch (error) {
    console.error("❌ Ошибка:", error.message);
    console.error("❌ Stack:", error.stack);

    // Показываем ошибку пользователю
    const app = document.getElementById("app");
    if (app) {
      app.innerHTML = `
        <div style="background: white; padding: 40px; margin: 40px auto; max-width: 800px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
          <h2 style="color: #dc3545; margin-top: 0;">❌ Ошибка загрузки приложения</h2>
          <p><strong>Сообщение:</strong> ${error.message}</p>
          <details style="margin-top: 20px;">
            <summary style="cursor: pointer; padding: 10px; background: #f8f9fa; border-radius: 4px;">📋 Подробности</summary>
            <pre style="background: #f8f9fa; padding: 15px; overflow: auto; max-height: 300px; margin-top: 10px; border-radius: 4px;">${error.stack}</pre>
          </details>
        </div>
      `;
    }
  }
}

// Проверяем состояние DOM
if (document.readyState === "loading") {
  console.log("⏳ Ждем загрузки DOM...");
  document.addEventListener("DOMContentLoaded", startApp);
} else {
  console.log("✅ DOM готов");
  startApp();
}

console.log("📝 main.js: Загрузка завершена");
