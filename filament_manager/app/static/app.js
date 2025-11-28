/* Filament Manager - JavaScript */

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
    // form.action est déjà une URL résolue par le navigateur
    const url = form.action;
    const isEdit = url.includes('/api/filaments/');
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
            // Redirection relative selon la page actuelle
            if (window.location.pathname.includes('/edit/')) {
                window.location.href = '../inventory';
            } else {
                window.location.href = './inventory';
            }
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
        // Utilisation de chemin relatif pour l'API
        const response = await fetch(`./api/filaments/${filamentId}/consume`, {
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
    document.querySelectorAll('.modal').forEach(modal => {
        modal.classList.remove('active');
    });
}

// Fermer le modal en cliquant en dehors
window.addEventListener('click', function (e) {
    if (e.target.classList.contains('modal')) {
        closeModal();
    }
});

// ============ AMS ============

async function scanAMS() {
    const modal = document.getElementById('amsModal');
    const list = document.getElementById('amsList');
    const loading = document.getElementById('amsLoading');

    modal.classList.add('active');
    loading.style.display = 'block';
    list.innerHTML = '';

    try {
        // Fetch AMS and Inventory in parallel
        const [amsRes, invRes] = await Promise.all([
            fetch('./api/ams/scan'),
            fetch('./api/filaments')
        ]);

        const amsData = await amsRes.json();
        const filaments = await invRes.json();

        loading.style.display = 'none';

        if (!amsData.success) {
            list.innerHTML = `<div class="error">Erreur AMS: ${amsData.error}</div>`;
            return;
        }

        if (amsData.slots.length === 0) {
            list.innerHTML = '<div class="empty-state"><p>Aucun filament détecté dans l\'AMS</p></div>';
            return;
        }

        amsData.slots.forEach(slot => {
            const div = document.createElement('div');
            div.className = 'ams-slot-card';

            // Build options for dropdown
            let options = '<option value="">-- Associer à l\'inventaire --</option>';
            filaments.forEach(fil => {
                options += `<option value="${fil.id}">${fil.name} (${fil.type}, ${fil.color})</option>`;
            });

            div.innerHTML = `
                <div class="slot-header">
                    <span class="slot-id">Slot ${slot.id}</span>
                    <span class="slot-type">${slot.type}</span>
                </div>
                <div class="slot-color" style="background-color: ${slot.color}"></div>
                <div class="slot-name" title="${slot.name}">${slot.name}</div>
                <div class="slot-actions">
                    <select id="ams-select-${slot.id}" class="ams-select">
                        ${options}
                    </select>
                    <button onclick="activateFromAMS(${slot.id})" class="btn-primary btn-sm">Activer</button>
                </div>
            `;
            list.appendChild(div);
        });

    } catch (error) {
        loading.style.display = 'none';
        list.innerHTML = `<div class="error">Erreur de communication: ${error.message}</div>`;
    }
}

async function activateFromAMS(slotId) {
    const select = document.getElementById(`ams-select-${slotId}`);
    const filamentId = select.value;

    if (!filamentId) {
        alert('Veuillez sélectionner un filament de l\'inventaire à associer.');
        return;
    }

    try {
        const response = await fetch(`./api/filaments/${filamentId}/set_active`, {
            method: 'POST'
        });
        const result = await response.json();
        if (result.success) {
            location.reload();
        } else {
            alert('Erreur: ' + result.error);
        }
    } catch (e) {
        alert('Erreur: ' + e.message);
    }
}

// ============ Suppression ============

// ============ Suppression ============

async function deleteFilament(id, btn) {
    const card = btn.closest('.filament-card');
    // Récupérer le nom et nettoyer le badge "ACTIF" si présent
    let name = card.querySelector('.filament-name').childNodes[0].textContent.trim();

    if (!confirm(`Êtes-vous sûr de vouloir supprimer le filament "${name}" ?\n\nCette action est irréversible.`)) {
        return;
    }

    try {
        // Utilisation de chemin relatif pour l'API
        const response = await fetch(`./api/filaments/${id}`, {
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

// ============ Activation Filament ============

async function setActiveFilament(id, btn) {
    const card = btn.closest('.filament-card');
    // Récupérer le nom et nettoyer le badge "ACTIF" si présent
    let name = card.querySelector('.filament-name').childNodes[0].textContent.trim();

    if (!confirm(`Définir "${name}" comme filament actif ?\n\nL'impression automatique décomptera le stock de ce filament.`)) {
        return;
    }

    try {
        const response = await fetch(`./api/filaments/${id}/set_active`, {
            method: 'POST'
        });

        const result = await response.json();

        if (result.success) {
            location.reload();
        } else {
            alert('Erreur lors de l\'activation');
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
