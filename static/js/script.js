document.addEventListener('DOMContentLoaded', function() {
    // 自動フォーカス
    const usernameInput = document.getElementById('username');
    if (usernameInput) {
        usernameInput.focus();
    }
    
    const itemInput = document.querySelector('input[name="item"]');
    if (itemInput) {
        itemInput.focus();
    }
    
    // レシピ追加ページでの材料入力欄の動的追加
    const addMainIngredientBtn = document.getElementById('add-main-ingredient');
    if (addMainIngredientBtn) {
        addMainIngredientBtn.addEventListener('click', function() {
            const mainIngredientsContainer = document.getElementById('main-ingredients-container');
            const ingredientRow = document.createElement('div');
            ingredientRow.className = 'ingredient-row';
            
            ingredientRow.innerHTML = `
                <input type="text" name="main_name[]" placeholder="材料名" required>
                <input type="text" name="main_amount[]" placeholder="分量">
                <button type="button" class="btn-remove" onclick="this.parentElement.remove()">
                    <i class="fas fa-minus"></i>
                </button>
            `;
            
            mainIngredientsContainer.appendChild(ingredientRow);
        });
    }
    
    // 調味料入力欄の動的追加
    const addSeasoningBtn = document.getElementById('add-seasoning');
    if (addSeasoningBtn) {
        addSeasoningBtn.addEventListener('click', function() {
            const seasoningsContainer = document.getElementById('seasonings-container');
            const seasoningRow = document.createElement('div');
            seasoningRow.className = 'ingredient-row';
            
            seasoningRow.innerHTML = `
                <input type="text" name="seasoning_name[]" placeholder="調味料名" required>
                <input type="text" name="seasoning_amount[]" placeholder="分量">
                <button type="button" class="btn-remove" onclick="this.parentElement.remove()">
                    <i class="fas fa-minus"></i>
                </button>
            `;
            
            seasoningsContainer.appendChild(seasoningRow);
        });
    }
    
    // 手順入力欄の動的追加
    const addStepBtn = document.getElementById('add-step');
    if (addStepBtn) {
        addStepBtn.addEventListener('click', function() {
            const stepsContainer = document.getElementById('steps-container');
            const stepCount = stepsContainer.childElementCount + 1;
            
            const stepRow = document.createElement('div');
            stepRow.className = 'step-row';
            
            stepRow.innerHTML = `
                <div class="step-number">${stepCount}</div>
                <textarea name="step[]" placeholder="手順の詳細" required></textarea>
                <button type="button" class="btn-remove" onclick="removeStep(this)">
                    <i class="fas fa-minus"></i>
                </button>
            `;
            
            stepsContainer.appendChild(stepRow);
        });
    }
    
    // 全削除ボタンの確認ダイアログ
    const clearButtons = document.querySelectorAll('.btn-clear');
    clearButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const category = this.closest('form').querySelector('input[name="category"]').value;
            if (!confirm(`${category}カテゴリのすべてのアイテムを削除してもよろしいですか？`)) {
                e.preventDefault();
            }
        });
    });
});

// 手順の削除と番号の振り直し
function removeStep(button) {
    const stepRow = button.parentElement;
    const stepsContainer = stepRow.parentElement;
    stepRow.remove();
    
    // 残りの手順の番号を振り直す
    const stepRows = stepsContainer.querySelectorAll('.step-row');
    stepRows.forEach((row, index) => {
        row.querySelector('.step-number').textContent = index + 1;
    });
}
