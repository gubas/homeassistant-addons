/* Filament Manager - JavaScript */

// Configuration de base
const INGRESS_PATH = window.location.pathname.split('/').slice(0, -1).join('') || '';

// ============ Form Handling ============

document.addEventListener('DOMContentLoaded', function () {
    const filamentForm = document.getElementById('filamentForm');
    if (filamentForm) {
        filamentForm.addEventListener('submit', handleFilamentSubmit);
    }

    const consumeForm = document.getElementById('consumeForm');
    if (consumeForm) {
        consumeForm.addEventListener('submit', handleConsumeSubmit);
    }
});

async function handleFilamentSubmit(e) {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);

    // Déterminer si c'est un ajout ou une modification
    const isEdit = form.action.includes('/api/filaments/');
    const url = form.action;
    const method = isEdit ? 'PUT' : 'POST';

    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            window.location.href = `${INGRESS_PATH}/inventory`;
        } else {
            alert('Erreur: ' + (result.error || 'Erreur inconnue'));
        }
    } catch (error) {
        alert('Erreur de communication: ' + error.message);
    }
}

// ============ Consommation ============

function consumeFilament(id, name) {
    document.getElementById('consumeFilamentId').value = id;
    document.getElementById('consumeFilamentName').value = name;
    document.getElementById('consumeWeight').value = '';
    document.getElementById('consumePrintName').value = '';

    const modal = document.getElementById('consumeModal');
    modal.classList.add('active');
}

async function handleConsumeSubmit(e) {
    e.preventDefault();

    const filamentId = document.getElementById('consumeFilamentId').value;
    const weight = parseFloat(document.getElementById('consumeWeight').value);
    const printName = document.getElementById('consumePrintName').value;

    if (!weight || weight <= 0) {
        alert('Veuillez entrer un poids valide');
        return;
    }

    try {
        const response = await fetch(`${INGRESS_PATH}/api/filaments/${filamentId}/consume`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                weight_used: weight,
                print_name: printName
            })
        });

        const result = await response.json();

        if (result.success) {
            closeModal();
            location.reload();
        } else {
            alert('Erreur: ' + (result.error || 'Erreur inconnue'));
        }
    } catch (error) {
        alert('Erreur de communication: ' + error.message);
    }
}

function closeModal() {
    const modal = document.getElementById('consumeModal');
    if (modal) {
        modal.classList.remove('active');
    }
}

// Fermer le modal en cliquant en dehors
window.addEventListener('click', function (e) {
    const modal = document.getElementById('consumeModal');
    if (e.target === modal) {
        closeModal();
    }
});

// ============ Suppression ============

async function deleteFilament(id, name) {
    if (!confirm(`Êtes-vous sûr de vouloir supprimer le filament "${name}" ?\n\nCette action est irréversible.`)) {
        return;
    }

    try {
        const response = await fetch(`${INGRESS_PATH}/api/filaments/${id}`, {
            method: 'DELETE'
        });

        const result = await response.json();

        if (result.success) {
            location.reload();
        } else {
            alert('Erreur lors de la suppression');
        }
    } catch (error) {
        alert('Erreur de communication: ' + error.message);
    }
}

// ============ Utilitaires ============

// Fermer les modals avec la touche Escape
document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
        closeModal();
    }
});
