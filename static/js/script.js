document.addEventListener('DOMContentLoaded', function() {
    // Auto-focus the input field on the login page
    const usernameInput = document.getElementById('username');
    if (usernameInput) {
        usernameInput.focus();
    }
    
    // Auto-focus the item input field on the main page
    const itemInput = document.querySelector('input[name="item"]');
    if (itemInput) {
        itemInput.focus();
    }
    
    // Add smooth fade-in animation for list items
    const listItems = document.querySelectorAll('.list-item');
    listItems.forEach((item, index) => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(10px)';
        setTimeout(() => {
            item.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            item.style.opacity = '1';
            item.style.transform = 'translateY(0)';
        }, index * 50);
    });
    
    // Add confirmation for clear all buttons
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
