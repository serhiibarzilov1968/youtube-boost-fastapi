document.addEventListener('DOMContentLoaded', () => {
    const registrationForm = document.getElementById('registrationForm');
    const loginForm = document.getElementById('loginForm');
    const messageDiv = document.getElementById('message');

    // URL бэкенда, который мы используем (localhost для локального тестирования)
    const API_BASE_URL = 'http://localhost:8001';

    // --- Логика Регистрации ---
    if (registrationForm ) {
        registrationForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const REGISTER_URL = `${API_BASE_URL}/api/v1/users/register`;

            messageDiv.textContent = 'Регистрация...';
            messageDiv.style.color = 'blue';

            try {
                const response = await fetch(REGISTER_URL, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email, password }),
                });

                const data = await response.json();

                if (response.ok) {
                    messageDiv.textContent = 'Регистрация успешна! Перенаправление на страницу входа...';
                    messageDiv.style.color = 'green';
                    // Перенаправление на страницу входа после успешной регистрации
                    setTimeout(() => {
                        window.location.href = 'login.html';
                    }, 2000);
                } else {
                    messageDiv.textContent = `Ошибка регистрации: ${data.detail || 'Неизвестная ошибка'}`;
                    messageDiv.style.color = 'red';
                }
            } catch (error) {
                console.error('Сетевая ошибка при регистрации:', error);
                messageDiv.textContent = 'Не удалось подключиться к серверу. Проверьте, запущен ли бэкенд на 8001 порту.';
                messageDiv.style.color = 'red';
            }
        });
    }

    // --- Логика Входа ---
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const LOGIN_URL = `${API_BASE_URL}/api/v1/users/login`;

            messageDiv.textContent = 'Вход...';
            messageDiv.style.color = 'blue';

            try {
                const response = await fetch(LOGIN_URL, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email, password }),
                });

                const data = await response.json();

                if (response.ok) {
                    // Сохраняем токен и перенаправляем
                    localStorage.setItem('access_token', data.access_token);
                    localStorage.setItem('token_type', data.token_type);
                    messageDiv.textContent = 'Вход успешен! Перенаправление на панель управления...';
                    messageDiv.style.color = 'green';
                    setTimeout(() => {
                        window.location.href = 'dashboard.html';
                    }, 1500);
                } else {
                    messageDiv.textContent = `Ошибка входа: ${data.detail || 'Неизвестная ошибка'}`;
                    messageDiv.style.color = 'red';
                }
            } catch (error) {
                console.error('Сетевая ошибка при входе:', error);
                messageDiv.textContent = 'Не удалось подключиться к серверу. Проверьте, запущен ли бэкенд на 8001 порту.';
                messageDiv.style.color = 'red';
            }
        });
    }

    // --- Логика Проверки Аутентификации и Анализа на Dashboard ---
    if (window.location.pathname.includes('dashboard.html')) {
        const token = localStorage.getItem('access_token');
        if (!token) {
            // Если токена нет, перенаправляем на страницу входа
            window.location.href = 'login.html';
        }
        // В реальном приложении здесь должна быть проверка токена на бэкенде

        // --- Логика Анализа Канала ---
        const analyzeForm = document.getElementById('analyzeForm');
        const analysisResultDiv = document.getElementById('analysisResult');
        const analyzeButton = document.getElementById('analyzeButton');

        if (analyzeForm) {
            analyzeForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const channelId = document.getElementById('channelId').value;
                const ANALYZE_URL = `${API_BASE_URL}/api/v1/analyzer/analyze/${channelId}`;

                analysisResultDiv.innerHTML = '<p style="color: blue;">Анализируем канал...</p>';
                analyzeButton.disabled = true;

                try {
                    const response = await fetch(ANALYZE_URL, {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                            // В реальном приложении здесь нужно передавать токен
                            // 'Authorization': `Bearer ${token}` 
                        },
                    });

                    const data = await response.json();

                    if (response.ok) {
                        analysisResultDiv.innerHTML = `
                            <h3>Результат анализа: ${data.channel_title}</h3>
                            <p><strong>ID Канала:</strong> ${data.channel_id}</p>
                            <p><strong>Подписчики:</strong> ${data.subscriber_count.toLocaleString()}</p>
                            <p><strong>Видео:</strong> ${data.video_count.toLocaleString()}</p>
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
    }
});
