let currentUser = null;

// Login form submission
document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: document.getElementById('loginUsername').value,
            password: document.getElementById('loginPassword').value
        })
    });
    const data = await response.json();
    if (data.success) {
        currentUser = {
            id: data.user_id,
            role: data.role
        };
        alert('Login successful!');
        if (data.role === 'admin') {
            loadPendingHours();
        }
        loadUserHours();
    } else {
        alert('Login failed: ' + data.message);
    }
});

// Register form submission
document.getElementById('registerForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const response = await fetch('/api/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: document.getElementById('regUsername').value,
            email: document.getElementById('regEmail').value,
            password: document.getElementById('regPassword').value
        })
    });
    const data = await response.json();
    if (data.success) {
        alert('Registration successful! Please login.');
        showTab('login');
    } else {
        alert('Registration failed: ' + data.error);
    }
});

// Log hours form submission
document.getElementById('logHoursForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    if (!currentUser) {
        alert('Please login first');
        return;
    }
    const response = await fetch('/api/hours', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            user_id: currentUser.id,
            service_date: document.getElementById('serviceDate').value,
            hours_served: document.getElementById('hoursServed').value,
            activity_description: document.getElementById('description').value
        })
    });
    const data = await response.json();
    if (data.success) {
        alert('Hours logged successfully!');
        loadUserHours();
    } else {
        alert('Failed to log hours: ' + data.error);
    }
});

// Load user's hours
async function loadUserHours() {
    if (!currentUser) return;
    const response = await fetch(`/api/hours/${currentUser.id}`);
    const data = await response.json();
    if (data.success) {
        const tbody = document.getElementById('hoursTable');
        tbody.innerHTML = '';
        data.hours.forEach(hour => {
            tbody.innerHTML += `
                <tr>
                    <td>${hour.service_date}</td>
                    <td>${hour.hours_served}</td>
                    <td>${hour.activity_description}</td>
                    <td>${hour.status}</td>
                </tr>
            `;
        });
    }
}

// Load pending hours for admin
async function loadPendingHours() {
    if (!currentUser || currentUser.role !== 'admin') return;
    const response = await fetch('/api/admin/pending');
    const data = await response.json();
    if (data.success) {
        const tbody = document.getElementById('adminTable');
        tbody.innerHTML = '';
        data.pending_hours.forEach(hour => {
            tbody.innerHTML += `
                <tr>
                    <td>${hour.user_id}</td>
                    <td>${hour.service_date}</td>
                    <td>${hour.hours_served}</td>
                    <td>${hour.activity_description}</td>
                    <td>
                        <button onclick="verifyHours(${hour.record_id}, 'approved')">Approve</button>
                        <button onclick="verifyHours(${hour.record_id}, 'rejected')">Reject</button>
                    </td>
                </tr>
            `;
        });
    }
}

// Verify hours (admin function)
async function verifyHours(recordId, status) {
    if (!currentUser || currentUser.role !== 'admin') return;
    const response = await fetch(`/api/admin/verify/${recordId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            status: status,
            admin_id: currentUser.id
        })
    });
    const data = await response.json();
    if (data.success) {
        alert(`Hours ${status} successfully!`);
        loadPendingHours();
    } else {
        alert('Failed to verify hours: ' + data.error);
    }
}

function showTab(tabId) {
    // Hide all tab contents
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    
    // Remove active class from all tabs
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Show selected tab content
    document.getElementById(tabId).classList.add('active');
    
    // Add active class to clicked tab
    event.target.classList.add('active');
} 