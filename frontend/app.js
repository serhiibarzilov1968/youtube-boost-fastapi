// API Base URL - измените это на URL вашего сервера
const API_BASE_URL = 'http://localhost:8001';

document.addEventListener('DOMContentLoaded', function() {
    // Обработка формы регистрации
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const messageDiv = document.getElementById('message');

            try {
                const response = await fetch(`${API_BASE_URL}/api/v1/users/register`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email, password })
                });

                const data = await response.json();

                if (response.ok) {
                    messageDiv.innerHTML = `<p style="color: green;">Регистрация успешна! Перенаправление на страницу входа...</p>`;
                    setTimeout(() => {
                        window.location.href = 'login.html';
                    }, 2000);
                } else {
                    messageDiv.innerHTML = `<p style="color: red;">Ошибка: ${data.detail || 'Неизвестная ошибка'}</p>`;
                }
            } catch (error) {
                console.error('Сетевая ошибка при регистрации:', error);
                messageDiv.innerHTML = '<p style="color: red;">Не удалось подключиться к серверу. Проверьте, запущен ли бэкенд.</p>';
            }
        });
    }

    // Обработка формы входа
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const messageDiv = document.getElementById('message');

            try {
                const response = await fetch(`${API_BASE_URL}/api/v1/users/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email, password })
                });

                const data = await response.json();

                if (response.ok) {
                    // Сохраняем токен в localStorage
                    localStorage.setItem('access_token', data.access_token);
                    messageDiv.innerHTML = `<p style="color: green;">Вход успешен! Перенаправление на панель управления...</p>`;
                    setTimeout(() => {
                        window.location.href = 'dashboard.html';
                    }, 2000);
                } else {
                    messageDiv.innerHTML = `<p style="color: red;">Ошибка входа: ${data.detail || 'Неизвестная ошибка'}</p>`;
                }
            } catch (error) {
                console.error('Сетевая ошибка при входе:', error);
                messageDiv.innerHTML = '<p style="color: red;">Не удалось подключиться к серверу. Проверьте, запущен ли бэкенд.</p>';
            }
        });
    }

    // Обработка формы анализа канала
    const analyzeForm = document.getElementById('analyzeForm');
    if (analyzeForm) {
        analyzeForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const channelId = document.getElementById('channelId').value;
            const analysisResultDiv = document.getElementById('analysisResult');
            const analyzeButton = document.getElementById('analyzeButton');

            analyzeButton.disabled = true;
            analysisResultDiv.innerHTML = '<p>Загрузка...</p>';

            try {
                const response = await fetch(`${API_BASE_URL}/api/v1/analyzer/analyze/${channelId}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });

                const data = await response.json();

                if (response.ok) {
                    analysisResultDiv.innerHTML = `
                        <h3>Результаты анализа канала</h3>
                        <p><strong>ID канала:</strong> ${data.channel_id}</p>
                        <p><strong>Название:</strong> ${data.channel_title}</p>
                        <p><strong>Подписчики:</strong> ${data.subscriber_count.toLocaleString()}</p>
                        <p><strong>Видео:</strong> ${data.video_count}</p>
                        <p><strong>Просмотры:</strong> ${data.view_count.toLocaleString()}</p>
                        <p style="color: green;">Статус: ${data.status}</p>
                    `;
                } else {
                    analysisResultDiv.innerHTML = `<p style="color: red;">Ошибка анализа: ${data.detail || 'Неизвестная ошибка'}</p>`;
                }
            } catch (error) {
                console.error('Сетевая ошибка при анализе:', error);
                analysisResultDiv.innerHTML = '<p style="color: red;">Не удалось подключиться к API. Проверьте, запущен ли бэкенд.</p>';
            } finally {
                analyzeButton.disabled = false;
            }
        });
    }
});

// Создание формы регистрации на главной странице
if (document.body.innerHTML.includes('YouTubeBoost - Главная')) {
    document.addEventListener('DOMContentLoaded', function() {
        const container = document.querySelector('.container');
        const registrationForm = document.createElement('div');
        registrationForm.innerHTML = `
            <h2>Регистрация</h2>
            <form id="registerForm">
                <label for="email">Email:</label>
                <input type="email" id="email" required>

                <label for="password">Пароль:</label>
                <input type="password" id="password" required>

                <button type="submit">Зарегистрироваться</button>
            </form>
            <div id="message"></div>
        `;
        container.appendChild(registrationForm);
    });
}

