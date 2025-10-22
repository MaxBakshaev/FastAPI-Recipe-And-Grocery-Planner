let productsList = [];
let uploadedImageUrl = null;

// Функции для показа/скрытия сообщений
function showError(message) {
    const errorEl = document.getElementById('error-message');
    const errorText = document.getElementById('error-text');
    errorText.textContent = message;
    errorEl.style.display = 'block';
    document.getElementById('success-message').style.display = 'none';
    
    // Автоскрытие через 5 секунд
    setTimeout(() => {
        hideError();
    }, 5000);
}

function hideError() {
    document.getElementById('error-message').style.display = 'none';
}

function showSuccess(message) {
    const successEl = document.getElementById('success-message');
    const successText = document.getElementById('success-text');
    successText.textContent = message;
    successEl.style.display = 'block';
    document.getElementById('error-message').style.display = 'none';
}

function showLoading() {
    document.getElementById('btn-text').style.display = 'none';
    document.getElementById('loading-spinner').style.display = 'block';
    document.getElementById('submit-btn').disabled = true;
}

function hideLoading() {
    document.getElementById('btn-text').style.display = 'block';
    document.getElementById('loading-spinner').style.display = 'none';
    document.getElementById('submit-btn').disabled = false;
}

// Предпросмотр картинки
document.getElementById('recipe-image').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.getElementById('image-preview');
            const previewImg = document.getElementById('preview-img');
            previewImg.src = e.target.result;
            preview.style.display = 'block';
        }
        reader.readAsDataURL(file);
    }
});

window.addEventListener('DOMContentLoaded', async () => {
    try {
        const res = await fetch('/api/v1/products/');
        productsList = await res.json();
        productsList.sort((a, b) => a.name.localeCompare(b.name, 'ru', { sensitivity: 'base' }));
        populateAllProductSelects();
    } catch (err) {
        showError("Ошибка при загрузке списка продуктов");
        console.error(err);
    }
});

function populateProductSelect(selectElement) {
    selectElement.innerHTML = '<option value="">-- Выберите продукт --</option>';
    productsList.forEach(product => {
        const option = document.createElement('option');
        option.value = product.id;
        option.textContent = product.name;
        selectElement.appendChild(option);
    });
}

function populateAllProductSelects() {
    const selects = document.querySelectorAll('select[name="product_id"]');
    selects.forEach(select => populateProductSelect(select));
}

function addProduct() {
    const container = document.getElementById('products-container');
    const productBlock = document.createElement('div');
    productBlock.className = 'product-block';
    productBlock.style.cssText = 'display: flex; align-items: center; gap: 10px; width: 100%;';

    productBlock.innerHTML = ` 
        <div style="display: flex; align-items: center; gap: 10px; width: 100%;">
            <div style="flex: 3; display: flex; flex-direction: column;">
                <label style="font-weight: 700; margin-bottom: 8px;">Продукты:</label>
                <select name="product_id" required
                        style="font-size: 20px; padding: 12px; border: 1px solid #ccc; border-radius: 6px; min-height: 50px;">
                    <option value="">-- Выберите продукт --</option>
                </select>
            </div>
            <div style="flex: 1; display: flex; flex-direction: column;">
                <label style="font-weight: 700; margin-bottom: 8px;">Граммы:</label>
                <input type="number" name="quantity" min="0" required
                    style="font-size: 20px; padding: 12px; border: 1px solid #ccc; border-radius: 6px; min-height: 50px;">
            </div>
            <button type="button" onclick="removeProduct(this)"
                    style="height: 30px; width: 30px; font-size: 30px; color: white; background-color: red; border: none; 
                    display: flex; justify-content: center; align-items: center; margin-top: 30px; cursor: pointer;">×</button>
        </div>
    `;
    container.appendChild(productBlock);

    const newSelect = productBlock.querySelector('select[name="product_id"]');
    populateProductSelect(newSelect);
}

function removeProduct(button) {
    button.parentElement.remove();
}

document.getElementById('recipe-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    // Скрываем предыдущие сообщения
    hideError();
    document.getElementById('success-message').style.display = 'none';

    const form = e.target;
    const title = form.title.value.trim();
    const body = form.body.value.trim();
    const imageFile = form.image.files[0];

    // Валидация
    if (!title || !body) {
        showError('Пожалуйста, заполните название и описание рецепта');
        return;
    }

    const productBlocks = document.querySelectorAll('.product-block');
    if (productBlocks.length === 0) {
        showError('Добавьте хотя бы один продукт в рецепт');
        return;
    }

    const products_info = [];
    for (const block of productBlocks) {
        const product_id = parseInt(block.querySelector('select[name="product_id"]').value);
        const quantity = parseInt(block.querySelector('input[name="quantity"]').value);

        if (isNaN(product_id) || isNaN(quantity)) {
            showError('Пожалуйста, выберите продукт и укажите граммы для всех позиций');
            return;
        }

        products_info.push({ product_id, quantity });
    }

    // Показываем загрузку
    showLoading();

    try {
        // Загружаем картинку если она есть
        let imageUrl = null;
        if (imageFile) {
            try {
                const formData = new FormData();
                formData.append('file', imageFile);

                const uploadResponse = await fetch('/api/v1/recipes/upload/recipe-image', {
                    method: 'POST',
                    body: formData
                });

                if (uploadResponse.ok) {
                    const uploadResult = await uploadResponse.json();
                    imageUrl = uploadResult.image_url;
                } else {
                    const errorData = await uploadResponse.json();
                    showError(errorData.detail || 'Ошибка при загрузке изображения');
                    return;
                }
            } catch (error) {
                showError('Ошибка при загрузке изображения: ' + error.message);
                return;
            }
        }

        const payload = { 
            title, 
            body, 
            products_info,
            image_url: imageUrl
        };
        
        const token = localStorage.getItem('access_token');

        if (!token) {
            showError('Пожалуйста, войдите в систему');
            return;
        }

        const response = await fetch('/api/v1/recipes/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            showSuccess('Рецепт успешно создан!');
            // Редирект через 1 секунду
            setTimeout(() => {
                window.location.href = "/recipes";
            }, 1000);
        } else {
            const error = await response.json();
            showError(error.detail || "Ошибка при создании рецепта");
        }
    } catch (error) {
        showError("Ошибка при отправке: " + error.message);
    } finally {
        hideLoading();
    }
});

// Скрываем ошибку при клике на нее
document.getElementById('error-message').addEventListener('click', hideError);

// Скрываем ошибку при начале ввода в поля формы
const inputs = document.querySelectorAll('#recipe-form input, #recipe-form textarea, #recipe-form select');
inputs.forEach(input => {
    input.addEventListener('input', hideError);
});