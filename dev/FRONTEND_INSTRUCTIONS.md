# Frontend RaceTracker - Инструкции для Claude Code

## Обзор проекта

Реализация frontend части веб-приложения "RaceTracker" для управления информацией о скачках в клубе любителей скачек. Используется архитектура Feature-Sliced Design (FSD) и монорепозиторий.

## Структура монорепозитория

```
racetracker/
├── backend/
└── frontend/
    ├── src/
    │   ├── app/              # Инициализация приложения
    │   ├── pages/            # Страницы (роутинг)
    │   ├── widgets/          # Комплексные компоненты
    │   ├── features/         # Функциональные модули
    │   ├── entities/         # Бизнес-сущности
    │   ├── shared/           # Переиспользуемый код
    │   └── index.tsx
    ├── public/
    ├── Dockerfile
    ├── nginx.conf
    ├── package.json
    └── tsconfig.json
```

## Технологический стек

- **React**: 18+
- **TypeScript**: 5+
- **React Router**: маршрутизация
- **Axios**: HTTP-клиент
- **React Query (TanStack Query)**: управление серверным состоянием
- **CSS Modules** или **Tailwind CSS**: стилизация
- **Vite**: сборщик
- **Nginx**: веб-сервер для production

## Архитектура: Feature-Sliced Design (FSD)

### Слои FSD (снизу вверх)

1. **shared** - переиспользуемый код, UI-kit, утилиты, API конфигурация
2. **entities** - бизнес-сущности (Race, Jockey, Horse, Owner)
3. **features** - функциональные возможности (CreateRace, AddJockey, etc.)
4. **widgets** - композитные блоки (RaceCard, ParticipantsList)
5. **pages** - страницы приложения
6. **app** - настройки, провайдеры, роутинг

### Детальная структура

```
frontend/src/
├── app/
│   ├── providers/
│   │   ├── RouterProvider.tsx
│   │   └── QueryProvider.tsx
│   ├── styles/
│   │   └── global.css
│   ├── App.tsx
│   └── main.tsx
│
├── pages/
│   ├── RacesPage/
│   │   ├── ui/
│   │   │   └── RacesPage.tsx
│   │   └── index.ts
│   ├── RaceDetailsPage/
│   │   ├── ui/
│   │   │   └── RaceDetailsPage.tsx
│   │   └── index.ts
│   ├── JockeysPage/
│   ├── HorsesPage/
│   └── index.ts
│
├── widgets/
│   ├── RaceCard/
│   │   ├── ui/
│   │   │   ├── RaceCard.tsx
│   │   │   └── RaceCard.module.css
│   │   └── index.ts
│   ├── ParticipantsList/
│   │   ├── ui/
│   │   │   ├── ParticipantsList.tsx
│   │   │   └── ParticipantsList.module.css
│   │   └── index.ts
│   └── Header/
│
├── features/
│   ├── CreateRace/
│   │   ├── ui/
│   │   │   ├── CreateRaceForm.tsx
│   │   │   └── CreateRaceForm.module.css
│   │   ├── model/
│   │   │   └── useCreateRace.ts
│   │   └── index.ts
│   ├── AddJockey/
│   ├── AddHorse/
│   ├── AddRaceResult/
│   └── ViewRaceHistory/
│
├── entities/
│   ├── race/
│   │   ├── model/
│   │   │   └── types.ts
│   │   ├── api/
│   │   │   └── raceApi.ts
│   │   └── index.ts
│   ├── jockey/
│   │   ├── model/
│   │   │   └── types.ts
│   │   ├── api/
│   │   │   └── jockeyApi.ts
│   │   └── index.ts
│   ├── horse/
│   ├── owner/
│   └── participant/
│
└── shared/
    ├── api/
    │   ├── config.ts          # ⚠️ ВАЖНО: Конфигурация API
    │   └── client.ts
    ├── ui/
    │   ├── Button/
    │   ├── Input/
    │   ├── Card/
    │   └── Modal/
    ├── lib/
    │   ├── hooks/
    │   └── utils/
    └── config/
        └── routes.ts
```

---

## Shared Layer - Конфигурация API

### ⚠️ КРИТИЧЕСКИ ВАЖНО: Конфигурация доступа к Backend

**Файл: `src/shared/api/config.ts`**

```typescript
/**
 * КОНФИГУРАЦИЯ ПОДКЛЮЧЕНИЯ К BACKEND API
 * 
 * ⚠️ ВАЖНО: Все URL для доступа к backend должны быть вынесены сюда
 * Это единственное место, где указываются адреса backend-серверов
 */

// Базовый URL API (изменяется в зависимости от окружения)
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Версия API
export const API_VERSION = 'v1';

// Полный путь к API
export const API_URL = `${API_BASE_URL}/api/${API_VERSION}`;

// Endpoints
export const API_ENDPOINTS = {
  // Races (Состязания)
  RACES: '/races',
  RACE_BY_ID: (id: number) => `/races/${id}`,
  
  // Jockeys (Жокеи)
  JOCKEYS: '/jockeys',
  JOCKEY_BY_ID: (id: number) => `/jockeys/${id}`,
  JOCKEY_RACES: (id: number) => `/jockeys/${id}/races`,
  
  // Horses (Лошади)
  HORSES: '/horses',
  HORSE_BY_ID: (id: number) => `/horses/${id}`,
  HORSE_RACES: (id: number) => `/horses/${id}/races`,
  
  // Owners (Владельцы)
  OWNERS: '/owners',
  OWNER_BY_ID: (id: number) => `/owners/${id}`,
  
  // Participants (Участники)
  PARTICIPANTS: '/participants',
} as const;

// Таймауты
export const API_TIMEOUT = 10000; // 10 секунд

// Конфигурация для разных окружений
export const getApiConfig = () => {
  const env = import.meta.env.MODE;
  
  switch (env) {
    case 'production':
      return {
        baseURL: import.meta.env.VITE_API_BASE_URL || 'https://api.racetracker.com',
        timeout: API_TIMEOUT,
      };
    case 'development':
      return {
        baseURL: 'http://localhost:8000',
        timeout: API_TIMEOUT,
      };
    default:
      return {
        baseURL: 'http://localhost:8000',
        timeout: API_TIMEOUT,
      };
  }
};
```

**Файл: `src/shared/api/client.ts`**

```typescript
import axios, { AxiosInstance, AxiosError } from 'axios';
import { API_URL, API_TIMEOUT } from './config';

/**
 * Настроенный HTTP-клиент для работы с API
 */
export const apiClient: AxiosInstance = axios.create({
  baseURL: API_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor (для добавления токенов и т.д.)
apiClient.interceptors.request.use(
  (config) => {
    // Здесь можно добавить токен авторизации
    // const token = localStorage.getItem('token');
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor (для обработки ошибок)
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    // Обработка ошибок
    if (error.response) {
      // Сервер ответил с ошибкой
      console.error('API Error:', error.response.status, error.response.data);
    } else if (error.request) {
      // Запрос был отправлен, но ответа не было
      console.error('Network Error:', error.request);
    } else {
      // Что-то пошло не так при настройке запроса
      console.error('Error:', error.message);
    }
    return Promise.reject(error);
  }
);
```

**Файл: `.env.development`**

```env
VITE_API_BASE_URL=http://localhost:8000
```

**Файл: `.env.production`**

```env
VITE_API_BASE_URL=https://api.racetracker.com
```

---

## Entities Layer - Бизнес-сущности

### Race Entity

**Файл: `src/entities/race/model/types.ts`**

```typescript
export interface Race {
  id: number;
  date: string; // ISO date format
  time: string; // HH:MM format
  hippodrome: string;
  name?: string;
}

export interface ParticipantResult {
  jockey_name: string;
  horse_name: string;
  place: number;
  time_result?: string; // HH:MM:SS format
}

export interface RaceWithParticipants {
  race: Race;
  participants: ParticipantResult[];
}

export interface CreateRaceDTO {
  date: string;
  time: string;
  hippodrome: string;
  name?: string;
}
```

**Файл: `src/entities/race/api/raceApi.ts`**

```typescript
import { apiClient } from '@/shared/api/client';
import { API_ENDPOINTS } from '@/shared/api/config';
import { Race, RaceWithParticipants, CreateRaceDTO } from '../model/types';

export const raceApi = {
  // Получить все состязания
  async getRaces(): Promise<Race[]> {
    const response = await apiClient.get<Race[]>(API_ENDPOINTS.RACES);
    return response.data;
  },

  // Получить состязание с участниками (Функция 1 из ТЗ)
  async getRaceWithParticipants(raceId: number): Promise<RaceWithParticipants> {
    const response = await apiClient.get<RaceWithParticipants>(
      API_ENDPOINTS.RACE_BY_ID(raceId)
    );
    return response.data;
  },

  // Создать новое состязание (Функция 2 из ТЗ)
  async createRace(data: CreateRaceDTO): Promise<Race> {
    const response = await apiClient.post<Race>(API_ENDPOINTS.RACES, data);
    return response.data;
  },
};
```

### Jockey Entity

**Файл: `src/entities/jockey/model/types.ts`**

```typescript
export interface Jockey {
  id: number;
  name: string;
  address: string;
  age: number;
  rating: number;
}

export interface CreateJockeyDTO {
  name: string;
  address: string;
  age: number;
  rating: number;
}
```

**Файл: `src/entities/jockey/api/jockeyApi.ts`**

```typescript
import { apiClient } from '@/shared/api/client';
import { API_ENDPOINTS } from '@/shared/api/config';
import { Jockey, CreateJockeyDTO } from '../model/types';
import { Race } from '@/entities/race';

export const jockeyApi = {
  // Получить всех жокеев
  async getJockeys(): Promise<Jockey[]> {
    const response = await apiClient.get<Jockey[]>(API_ENDPOINTS.JOCKEYS);
    return response.data;
  },

  // Создать нового жокея (Функция 3 из ТЗ)
  async createJockey(data: CreateJockeyDTO): Promise<Jockey> {
    const response = await apiClient.post<Jockey>(API_ENDPOINTS.JOCKEYS, data);
    return response.data;
  },

  // Получить состязания жокея (Функция 6 из ТЗ)
  async getJockeyRaces(jockeyId: number): Promise<Race[]> {
    const response = await apiClient.get<Race[]>(
      API_ENDPOINTS.JOCKEY_RACES(jockeyId)
    );
    return response.data;
  },
};
```

### Horse Entity

**Файл: `src/entities/horse/model/types.ts`**

```typescript
export enum HorseGender {
  STALLION = 'жеребец',
  MARE = 'кобыла',
  GELDING = 'мерин',
}

export interface Horse {
  id: number;
  nickname: string;
  gender: HorseGender;
  age: number;
  owner_id: number;
}

export interface CreateHorseDTO {
  nickname: string;
  gender: HorseGender;
  age: number;
  owner_id: number;
}
```

**Файл: `src/entities/horse/api/horseApi.ts`**

```typescript
import { apiClient } from '@/shared/api/client';
import { API_ENDPOINTS } from '@/shared/api/config';
import { Horse, CreateHorseDTO } from '../model/types';
import { Race } from '@/entities/race';

export const horseApi = {
  // Получить всех лошадей
  async getHorses(): Promise<Horse[]> {
    const response = await apiClient.get<Horse[]>(API_ENDPOINTS.HORSES);
    return response.data;
  },

  // Создать новую лошадь (Функция 4 из ТЗ)
  async createHorse(data: CreateHorseDTO): Promise<Horse> {
    const response = await apiClient.post<Horse>(API_ENDPOINTS.HORSES, data);
    return response.data;
  },

  // Получить состязания лошади (Функция 7 из ТЗ)
  async getHorseRaces(horseId: number): Promise<Race[]> {
    const response = await apiClient.get<Race[]>(
      API_ENDPOINTS.HORSE_RACES(horseId)
    );
    return response.data;
  },
};
```

---

## Features Layer - Функциональные возможности

### Feature: CreateRace

**Файл: `src/features/CreateRace/model/useCreateRace.ts`**

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { raceApi } from '@/entities/race';
import { CreateRaceDTO } from '@/entities/race/model/types';

export const useCreateRace = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateRaceDTO) => raceApi.createRace(data),
    onSuccess: () => {
      // Инвалидируем кеш списка состязаний
      queryClient.invalidateQueries({ queryKey: ['races'] });
    },
  });
};
```

**Файл: `src/features/CreateRace/ui/CreateRaceForm.tsx`**

```tsx
import React, { useState } from 'react';
import { useCreateRace } from '../model/useCreateRace';
import { Button } from '@/shared/ui/Button';
import { Input } from '@/shared/ui/Input';
import styles from './CreateRaceForm.module.css';

export const CreateRaceForm: React.FC = () => {
  const [formData, setFormData] = useState({
    date: '',
    time: '',
    hippodrome: '',
    name: '',
  });

  const { mutate: createRace, isPending, isError, error } = useCreateRace();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    createRace(
      {
        date: formData.date,
        time: formData.time,
        hippodrome: formData.hippodrome,
        name: formData.name || undefined,
      },
      {
        onSuccess: () => {
          // Очистить форму
          setFormData({ date: '', time: '', hippodrome: '', name: '' });
          alert('Состязание успешно создано!');
        },
      }
    );
  };

  return (
    <form className={styles.form} onSubmit={handleSubmit}>
      <h2>Добавить новое состязание</h2>
      
      <Input
        type="date"
        label="Дата состязания"
        value={formData.date}
        onChange={(e) => setFormData({ ...formData, date: e.target.value })}
        required
      />
      
      <Input
        type="time"
        label="Время проведения"
        value={formData.time}
        onChange={(e) => setFormData({ ...formData, time: e.target.value })}
        required
      />
      
      <Input
        type="text"
        label="Ипподром"
        value={formData.hippodrome}
        onChange={(e) => setFormData({ ...formData, hippodrome: e.target.value })}
        required
      />
      
      <Input
        type="text"
        label="Название (необязательно)"
        value={formData.name}
        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
      />
      
      <Button type="submit" disabled={isPending}>
        {isPending ? 'Создание...' : 'Создать состязание'}
      </Button>
      
      {isError && (
        <div className={styles.error}>
          Ошибка: {error?.message || 'Не удалось создать состязание'}
        </div>
      )}
    </form>
  );
};
```

### Feature: AddRaceResult

**Файл: `src/features/AddRaceResult/ui/AddRaceResultForm.tsx`**

```tsx
import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { raceApi } from '@/entities/race';
import { jockeyApi } from '@/entities/jockey';
import { horseApi } from '@/entities/horse';
import { participantApi } from '@/entities/participant';
import { Button } from '@/shared/ui/Button';
import { Select } from '@/shared/ui/Select';
import { Input } from '@/shared/ui/Input';

/**
 * Форма добавления результата состязания (Функция 5 из ТЗ)
 */
export const AddRaceResultForm: React.FC = () => {
  const [formData, setFormData] = useState({
    raceId: '',
    jockeyId: '',
    horseId: '',
    place: '',
    timeResult: '',
  });

  // Загружаем данные для селектов
  const { data: races } = useQuery({
    queryKey: ['races'],
    queryFn: () => raceApi.getRaces(),
  });

  const { data: jockeys } = useQuery({
    queryKey: ['jockeys'],
    queryFn: () => jockeyApi.getJockeys(),
  });

  const { data: horses } = useQuery({
    queryKey: ['horses'],
    queryFn: () => horseApi.getHorses(),
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    await participantApi.addParticipant({
      race_id: Number(formData.raceId),
      jockey_id: Number(formData.jockeyId),
      horse_id: Number(formData.horseId),
      place: Number(formData.place),
      time_result: formData.timeResult || undefined,
    });
    
    alert('Результат добавлен!');
    setFormData({
      raceId: '',
      jockeyId: '',
      horseId: '',
      place: '',
      timeResult: '',
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Добавить результат состязания</h2>
      
      <Select
        label="Состязание"
        value={formData.raceId}
        onChange={(e) => setFormData({ ...formData, raceId: e.target.value })}
        required
      >
        <option value="">Выберите состязание</option>
        {races?.map((race) => (
          <option key={race.id} value={race.id}>
            {race.name || race.hippodrome} - {race.date}
          </option>
        ))}
      </Select>
      
      <Select
        label="Жокей"
        value={formData.jockeyId}
        onChange={(e) => setFormData({ ...formData, jockeyId: e.target.value })}
        required
      >
        <option value="">Выберите жокея</option>
        {jockeys?.map((jockey) => (
          <option key={jockey.id} value={jockey.id}>
            {jockey.name}
          </option>
        ))}
      </Select>
      
      <Select
        label="Лошадь"
        value={formData.horseId}
        onChange={(e) => setFormData({ ...formData, horseId: e.target.value })}
        required
      >
        <option value="">Выберите лошадь</option>
        {horses?.map((horse) => (
          <option key={horse.id} value={horse.id}>
            {horse.nickname}
          </option>
        ))}
      </Select>
      
      <Input
        type="number"
        label="Занятое место"
        min="1"
        value={formData.place}
        onChange={(e) => setFormData({ ...formData, place: e.target.value })}
        required
      />
      
      <Input
        type="time"
        label="Время прохождения (необязательно)"
        step="1"
        value={formData.timeResult}
        onChange={(e) => setFormData({ ...formData, timeResult: e.target.value })}
      />
      
      <Button type="submit">Добавить результат</Button>
    </form>
  );
};
```

---

## Widgets Layer - Композитные компоненты

### Widget: ParticipantsList

**Файл: `src/widgets/ParticipantsList/ui/ParticipantsList.tsx`**

```tsx
import React from 'react';
import { ParticipantResult } from '@/entities/race/model/types';
import { Card } from '@/shared/ui/Card';
import styles from './ParticipantsList.module.css';

interface Props {
  participants: ParticipantResult[];
}

/**
 * Список участников состязания с результатами
 * Функция 1 из ТЗ: показать жокеев и лошадей с местами
 */
export const ParticipantsList: React.FC<Props> = ({ participants }) => {
  return (
    <div className={styles.container}>
      <h3>Результаты состязания</h3>
      
      <div className={styles.table}>
        <div className={styles.header}>
          <div className={styles.cell}>Место</div>
          <div className={styles.cell}>Жокей</div>
          <div className={styles.cell}>Лошадь</div>
          <div className={styles.cell}>Время</div>
        </div>
        
        {participants.map((participant, index) => (
          <div key={index} className={styles.row}>
            <div className={styles.cell}>
              <span className={styles.place}>{participant.place}</span>
            </div>
            <div className={styles.cell}>{participant.jockey_name}</div>
            <div className={styles.cell}>{participant.horse_name}</div>
            <div className={styles.cell}>
              {participant.time_result || '—'}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
```

---

## Pages Layer - Страницы

### RaceDetailsPage

**Файл: `src/pages/RaceDetailsPage/ui/RaceDetailsPage.tsx`**

```tsx
import React from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { raceApi } from '@/entities/race';
import { ParticipantsList } from '@/widgets/ParticipantsList';
import styles from './RaceDetailsPage.module.css';

/**
 * Страница детальной информации о состязании
 * Функция 1 из ТЗ
 */
export const RaceDetailsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  
  const { data, isLoading, isError } = useQuery({
    queryKey: ['race', id],
    queryFn: () => raceApi.getRaceWithParticipants(Number(id)),
    enabled: !!id,
  });

  if (isLoading) return <div>Загрузка...</div>;
  if (isError || !data) return <div>Ошибка загрузки данных</div>;

  const { race, participants } = data;

  return (
    <div className={styles.page}>
      <h1>{race.name || 'Состязание'}</h1>
      
      <div className={styles.info}>
        <div>
          <strong>Дата:</strong> {new Date(race.date).toLocaleDateString('ru-RU')}
        </div>
        <div>
          <strong>Время:</strong> {race.time}
        </div>
        <div>
          <strong>Ипподром:</strong> {race.hippodrome}
        </div>
      </div>

      <ParticipantsList participants={participants} />
    </div>
  );
};
```

### JockeyDetailsPage

**Файл: `src/pages/JockeyDetailsPage/ui/JockeyDetailsPage.tsx`**

```tsx
import React from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { jockeyApi } from '@/entities/jockey';
import { RaceCard } from '@/widgets/RaceCard';
import styles from './JockeyDetailsPage.module.css';

/**
 * Страница с информацией о жокее
 * Функция 6 из ТЗ: показать список состязаний жокея
 */
export const JockeyDetailsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  
  const { data: jockey } = useQuery({
    queryKey: ['jockey', id],
    queryFn: () => jockeyApi.getJockeyById(Number(id)),
  });

  const { data: races, isLoading } = useQuery({
    queryKey: ['jockey-races', id],
    queryFn: () => jockeyApi.getJockeyRaces(Number(id)),
  });

  if (!jockey) return <div>Загрузка...</div>;

  return (
    <div className={styles.page}>
      <h1>{jockey.name}</h1>
      
      <div className={styles.info}>
        <div><strong>Возраст:</strong> {jockey.age}</div>
        <div><strong>Рейтинг:</strong> {jockey.rating}</div>
        <div><strong>Адрес:</strong> {jockey.address}</div>
      </div>

      <h2>История состязаний</h2>
      
      {isLoading ? (
        <div>Загрузка состязаний...</div>
      ) : (
        <div className={styles.racesList}>
          {races?.map((race) => (
            <RaceCard key={race.id} race={race} />
          ))}
        </div>
      )}
    </div>
  );
};
```

---

## App Layer - Инициализация приложения

**Файл: `src/app/providers/QueryProvider.tsx`**

```tsx
import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

export const QueryProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
};
```

**Файл: `src/app/App.tsx`**

```tsx
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryProvider } from './providers/QueryProvider';
import { Header } from '@/widgets/Header';
import { RacesPage } from '@/pages/RacesPage';
import { RaceDetailsPage } from '@/pages/RaceDetailsPage';
import { JockeysPage } from '@/pages/JockeysPage';
import { JockeyDetailsPage } from '@/pages/JockeyDetailsPage';
import { HorsesPage } from '@/pages/HorsesPage';
import { HorseDetailsPage } from '@/pages/HorseDetailsPage';
import './styles/global.css';

export const App: React.FC = () => {
  return (
    <QueryProvider>
      <BrowserRouter>
        <div className="app">
          <Header />
          <main className="container">
            <Routes>
              <Route path="/" element={<RacesPage />} />
              <Route path="/races/:id" element={<RaceDetailsPage />} />
              <Route path="/jockeys" element={<JockeysPage />} />
              <Route path="/jockeys/:id" element={<JockeyDetailsPage />} />
              <Route path="/horses" element={<HorsesPage />} />
              <Route path="/horses/:id" element={<HorseDetailsPage />} />
            </Routes>
          </main>
        </div>
      </BrowserRouter>
    </QueryProvider>
  );
};
```

---

## Dockerfile для Frontend

```dockerfile
# Build stage
FROM node:18-alpine as build

WORKDIR /app

# Копируем package.json и устанавливаем зависимости
COPY package*.json ./
RUN npm ci

# Копируем исходный код
COPY . .

# Сборка приложения
RUN npm run build

# Production stage
FROM nginx:alpine

# Копируем собранное приложение
COPY --from=build /app/dist /usr/share/nginx/html

# Копируем конфигурацию nginx
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

---

## Nginx конфигурация

**Файл: `nginx.conf`**

```nginx
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    server {
        listen 80;
        server_name localhost;
        root /usr/share/nginx/html;
        index index.html;

        # Gzip сжатие
        gzip on;
        gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

        # SPA routing - все запросы отправляем на index.html
        location / {
            try_files $uri $uri/ /index.html;
        }

        # Кеширование статики
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        # Проксирование API запросов к backend (опционально)
        location /api/ {
            proxy_pass http://backend:8000;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }
    }
}
```

---

## Package.json

```json
{
  "name": "racetracker-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.21.0",
    "@tanstack/react-query": "^5.17.0",
    "axios": "^1.6.5"
  },
  "devDependencies": {
    "@types/react": "^18.2.47",
    "@types/react-dom": "^18.2.18",
    "@vitejs/plugin-react": "^4.2.1",
    "typescript": "^5.3.3",
    "vite": "^5.0.11"
  }
}
```

---

## Функции из ТЗ - Mapping Frontend

1. **Показать список жокеев и лошадей с местами** → `RaceDetailsPage` + `ParticipantsList`
2. **Добавить новое состязание** → `CreateRaceForm` feature
3. **Добавить нового жокея** → `AddJockeyForm` feature
4. **Добавить новую лошадь** → `AddHorseForm` feature
5. **Добавить результаты состязания** → `AddRaceResultForm` feature
6. **Список состязаний жокея** → `JockeyDetailsPage`
7. **Список состязаний лошади** → `HorseDetailsPage`

---

## Важные замечания

1. **⚠️ ВСЕ URL к backend находятся в `shared/api/config.ts`** - единственное место!
2. **FSD архитектура**: строгое соблюдение слоев и зависимостей
3. **React Query**: управление серверным состоянием и кешированием
4. **TypeScript**: строгая типизация для надежности
5. **Простота**: минимум зависимостей, максимум читаемости
6. **Адаптивность**: работает на всех устройствах
