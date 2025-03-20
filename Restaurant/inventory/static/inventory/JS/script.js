// filepath: c:\Users\artiu\Desktop\Py_DEV\django\Restaurant\inventory\static\inventory\JS\script.js
document.addEventListener('DOMContentLoaded', function() {
    const dropdownItems = document.querySelectorAll('.dropdown-item');
    const selectedIngredientsContainer = document.getElementById('selected-ingredients-container');
    const selectedIngredientsInput = document.getElementById('selected-ingredients');

    dropdownItems.forEach(item => {
        item.addEventListener('click', function(event) {
            event.preventDefault();
            const ingredientId = this.getAttribute('data-id');
            const ingredientName = this.getAttribute('data-name');
            const ingredientUnit = this.getAttribute('data-unit');
            // Check if the ingredient is already selected
            if (!selectedIngredientsInput.value.includes(ingredientId)) {
                // Add the selected ingredient to the container
                const ingredientElement = document.createElement('div');
                ingredientElement.className = 'selected-ingredient d-flex align-items-center mb-2 p-2 border rounded';
                ingredientElement.innerHTML = `
                    <div class="me-2">${ingredientName}</div>
                    <input type="number" class="form-control d-inline-block w-auto mx-2 amount-input" placeholder="${ingredientUnit}" name="amount_${ingredientId}" required>
                    <button type="button" class="btn btn-sm btn-danger remove-ingredient" data-id="${ingredientId}"><i class="fa-regular fa-circle-xmark" style="font-size: 16px;"></i></button>
                `;
                selectedIngredientsContainer.appendChild(ingredientElement);

                // Add event listener to the remove button
                ingredientElement.querySelector('.remove-ingredient').addEventListener('click', function() {
                    // Remove the ingredient element from the container
                    selectedIngredientsContainer.removeChild(ingredientElement);
                    // Update the hidden input field
                    updateSelectedIngredientsInput();
                });

                // Add event listener to the amount input field to update the hidden input field
                const amountInput = ingredientElement.querySelector('.amount-input');
                amountInput.addEventListener('input', updateSelectedIngredientsInput);

                // Update the hidden input field
                updateSelectedIngredientsInput();
            }
        });
    });

    function updateSelectedIngredientsInput() {
        const selectedIngredients = [];
        const ingredientElements = selectedIngredientsContainer.querySelectorAll('.selected-ingredient');
        ingredientElements.forEach(element => {
            const ingredientId = element.querySelector('.remove-ingredient').getAttribute('data-id');
            const quantity = element.querySelector('.amount-input').value;
            selectedIngredients.push(`${ingredientId}:${quantity}`);
        });
        selectedIngredientsInput.value = selectedIngredients.join(',');
    }
});