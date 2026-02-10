# Frontend RaceTracker

Фронтенд приложение для управления информацией о скачках, реализованное на чистом HTML, CSS и JavaScript с архитектурой Feature-Sliced Design (FSD).

## Технологический стек

- **Vanilla JavaScript (ES6+)** - без фреймворков
- **HTML5** - семантическая разметка
- **CSS3** - современная стилизация
- **Fetch API** - HTTP клиент
- **Hash Router** - навигация на стороне клиента

## Архитектура: Feature-Sliced Design (FSD)

Проект организован по слоям FSD архитектуры (снизу вверх):

```
frontend/src/
├── shared/              # Переиспользуемый код
│   ├── api.js          # HTTP клиент и конфигурация API
│   ├── utils.js        # Утилиты для работы с DOM
│   ├── eventBus.js     # Event emitter для коммуникации
│   └── ui.js           # UI компоненты
│
├── entities/           # Бизнес-сущности
│   ├── raceApi.js
│   ├── jockeyApi.js
│   ├── horseApi.js
│   ├── ownerApi.js
│   └── participantApi.js
│
├── features/           # Функциональные модули
│   ├── createRaceForm.js
│   ├── addJockeyForm.js
│   ├── addHorseForm.js
│   └── addRaceResultForm.js
│
├── widgets/            # Композитные компоненты
│   ├── header.js
│   ├── raceCard.js
│   └── participantsList.js
│
├── pages/              # Страницы приложения
│   ├── racesPage.js
│   ├── raceDetailsPage.js
│   ├── jockeysPage.js
│   ├── jockeyDetailsPage.js
│   ├── horsesPage.js
│   └── horseDetailsPage.js
│
├── app/                # Инициализация приложения
│   ├── router.js       # Router
│   └── app.js          # Инициализация
│
├── styles/
│   └── styles.css      # Глобальные стили
│
└── main.js             # Точка входа
```

## Установка и запуск

### Локальная разработка

```bash
# Запустить встроенный веб-сервер Python
python3 -m http.server 5173
```

Приложение будет доступно на `http://localhost:5173`

### Конфигурация API

Отредактируйте файл `.env`:
```
API_BASE_URL=http://localhost:8000
```

## Функционал

### Состязания (Races)
- ✅ Просмотр списка состязаний
- ✅ Просмотр деталей состязания с результатами
- ✅ Добавление нового состязания

### Жокеи (Jockeys)
- ✅ Просмотр списка жокеев
- ✅ Просмотр деталей жокея и его состязаний
- ✅ Добавление нового жокея

### Лошади (Horses)
- ✅ Просмотр списка лошадей
- ✅ Просмотр деталей лошади и её состязаний
- ✅ Добавление новой лошади

### Результаты состязаний
- ✅ Добавление результатов состязания (место, жокей, лошадь, время)

## Docker

### Сборка образа
```bash
docker build -t racetracker-frontend .
```

### Запуск контейнера
```bash
docker run -p 80:80 racetracker-frontend
```

## Архитектурные решения

### Event Bus
Для коммуникации между компонентами используется простой Event Bus (`shared/eventBus.js`):
```javascript
// Emit
eventBus.emit('race:created', data);

// Subscribe
eventBus.on('race:created', (data) => {
  // handle event
});
```

### API Клиент
Простой HTTP клиент с кешированием GET запросов (`shared/api.js`):
```javascript
const response = await apiClient.get('/races');
const newRace = await apiClient.post('/races', data);
```

### Роутинг
Hash-based роутер (`app/router.js`) без зависимостей:
- `#/` - список состязаний
- `#/races/:id` - деталь состязания
- `#/jockeys` - список жокеев
- `#/jockeys/:id` - деталь жокея
- `#/horses` - список лошадей
- `#/horses/:id` - деталь лошади

### UI Компоненты
Функции для создания UI элементов в `shared/ui.js`:
- `Button()` - кнопка
- `Input()` - input поле
- `Select()` - select поле
- `Card()` - карточка
- `Modal()` - модальное окно
- `Alert()` - уведомление
- `Spinner()` - загрузчик

## Преимущества подхода

✅ **Нет зависимостей** - чистый JavaScript, легко развертывается
✅ **Быстрая загрузка** - минимум кода, быстрая инициализация
✅ **FSD архитектура** - чистый, масштабируемый код
✅ **Простота** - легко понять и модифицировать
✅ **Отсутствие bundler** - работает как есть в браузере

## Файлы конфигурации

- `.env` - переменные окружения
- `.gitignore` - исключения из git
- `package.json` - метаданные проекта
- `Dockerfile` - Docker конфигурация
- `nginx.conf` - конфигурация Nginx для production

## Заметки

- API базовый URL конфигурируется в `src/shared/api.js`
- Все HTTP запросы автоматически кешируются на уровне клиента
- Event Bus используется для оповещения компонентов об изменениях
- Роутер использует hash для навигации (подходит для SPA)

## Контакты

Для вопросов и проблем обратитесь к команде разработки.
