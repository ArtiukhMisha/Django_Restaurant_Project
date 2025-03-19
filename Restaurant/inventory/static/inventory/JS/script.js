document.addEventListener('DOMContentLoaded', function() {
    const dropdownItems = document.querySelectorAll('.dropdown-item');
    const selectedIngredientsContainer = document.getElementById('selected-ingredients-container');
    const ingredientsSelect = document.getElementById('ingredients');

    dropdownItems.forEach(item => {
        item.addEventListener('click', function(event) {
            event.preventDefault();
            const ingredientId = this.getAttribute('data-id');
            const ingredientName = this.getAttribute('data-name');
            const ingredientUnit = this.getAttribute('data-unit');
            // Check if the ingredient is already selected
            if (!ingredientsSelect.querySelector(`option[value="${ingredientId}"]`).selected) {
                // Add the ingredient to the hidden select field
                const option = ingredientsSelect.querySelector(`option[value="${ingredientId}"]`);
                if (option) {
                    option.selected = true;
                }

                // Create a new element for the selected ingredient
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
                    // Remove the ingredient from the hidden select field
                    const option = ingredientsSelect.querySelector(`option[value="${ingredientId}"]`);
                    if (option) {
                        option.selected = false;
                    }

                    // Remove the ingredient element from the container
                    selectedIngredientsContainer.removeChild(ingredientElement);
                });

                // Add event listener to the amount input field to move focus to the next input field on Enter key press
                const amountInput = ingredientElement.querySelector('.amount-input');
                amountInput.addEventListener('keydown', function(event) {
                    if (event.key === 'Enter') {
                        event.preventDefault();
                        const inputs = Array.from(document.querySelectorAll('input'));
                        const index = inputs.indexOf(this);
                        if (index > -1 && index < inputs.length - 1) {
                            inputs[index + 1].focus();
                        }
                    }
                });
            }
        });
    });

    // Add event listener to all input fields to move focus to the next input field on Enter key press
    const allInputs = document.querySelectorAll('input');
    allInputs.forEach(input => {
        input.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                const inputs = Array.from(document.querySelectorAll('input'));
                const index = inputs.indexOf(this);
                if (index > -1 && index < inputs.length - 1) {
                    inputs[index + 1].focus();
                }
            }
        });
    });
});