// --------- Chart Logic ----------
function initChart(expensesData) {
    if (!expensesData || expensesData.length === 0) {
        return;
    }

    const categoryTotals = {};
    expensesData.forEach(e => {
        if (categoryTotals[e.category]) {
            categoryTotals[e.category] += parseFloat(e.amount);
        } else {
            categoryTotals[e.category] = parseFloat(e.amount);
        }
    });

    const labels = Object.keys(categoryTotals);
    const data = Object.values(categoryTotals);

    const canvas = document.getElementById('expenseChart');
    if (!canvas) return;

new Chart(ctx, {
    type: 'pie',
    data: {
        labels: labels,
        datasets: [{
            data: data
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false
    }
});
}

// --------- Small UI Animations ----------
document.addEventListener("DOMContentLoaded", () => {
    // Animate expense cards
    const items = document.querySelectorAll("ul li");
    items.forEach((item, index) => {
        item.style.opacity = 0;
        item.style.transform = "translateY(10px)";
        setTimeout(() => {
            item.style.transition = "all 0.4s ease";
            item.style.opacity = 1;
            item.style.transform = "translateY(0)";
        }, index * 80);
    });

    // Button click feedback
    const buttons = document.querySelectorAll("button");
    buttons.forEach(btn => {
        btn.addEventListener("click", () => {
            btn.style.transform = "scale(0.97)";
            setTimeout(() => {
                btn.style.transform = "scale(1)";
            }, 150);
        });
    });

    // Confirm before delete
    const deleteLinks = document.querySelectorAll("a.delete-link");
    deleteLinks.forEach(link => {
        link.addEventListener("click", (e) => {
            const ok = confirm("Are you sure you want to delete this expense?");
            if (!ok) {
                e.preventDefault();
            }
        });
    });
});