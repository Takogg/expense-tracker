// Load expenses and statistics on page load
document.addEventListener('DOMContentLoaded', () => {
    loadExpenses();
    loadStatistics();
});

// Logout function
function logout() {
    fetch('/api/logout', { method: 'POST' })
        .then(() => window.location.href = '/');
}

// Load all expenses
async function loadExpenses() {
    try {
        const response = await fetch('/api/expenses');
        const expenses = await response.json();

        const tbody = document.getElementById('expenses-tbody');
        tbody.innerHTML = '';

        if (expenses.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;">No expenses found. Add your first expense!</td></tr>';
            return;
        }

        expenses.forEach(expense => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${expense.date}</td>
                <td>${expense.category}</td>
                <td>$${parseFloat(expense.amount).toFixed(2)}</td>
                <td>${expense.note || '-'}</td>
                <td>
                    <button class="btn btn-delete" onclick="deleteExpense(${expense.id})">Delete</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading expenses:', error);
    }
}

// Delete expense
async function deleteExpense(id) {
    if (!confirm('Are you sure you want to delete this expense?')) {
        return;
    }

    try {
        const response = await fetch(`/api/expenses/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            loadExpenses();
            loadStatistics();
        }
    } catch (error) {
        console.error('Error deleting expense:', error);
    }
}

// Load statistics
async function loadStatistics() {
    try {
        const response = await fetch('/api/statistics');
        const stats = await response.json();

        document.getElementById('total-expenses').textContent = `$${stats.total.toFixed(2)}`;
        document.getElementById('monthly-expenses').textContent = `$${stats.monthly_total.toFixed(2)}`;

        // Update chart
        updateChart(stats.categories);
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}
