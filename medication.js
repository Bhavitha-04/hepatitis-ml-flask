// LOAD FROM STORAGE
let medicines = JSON.parse(localStorage.getItem("medicines")) || [];
let doctorReminder = localStorage.getItem("doctorReminder");
let testReminder = localStorage.getItem("testReminder");

// DISPLAY ON LOAD
window.onload = function () {
    displayMedicines();
    showSavedReminders();
};

// SHOW SAVED REMINDERS
function showSavedReminders() {
    if (doctorReminder) {
        document.getElementById("doctorOutput").innerHTML =
            `Doctor visit scheduled on ${doctorReminder} ✔`;
    }

    if (testReminder) {
        document.getElementById("testOutput").innerHTML =
            `Follow-up test on ${testReminder} 📅`;
    }
}

// ADD MEDICINE
function addMedicine() {
    let name = document.getElementById("medName").value;
    let dosage = document.getElementById("dosage").value;
    let timing = document.getElementById("timing").value;
    let food = document.getElementById("food").value;

    if (!name || !dosage || !timing || !food) {
        alert("Please fill all details");
        return;
    }

    let med = {
        name,
        dosage,
        timing,
        food,
        taken: false
    };

    medicines.push(med);
    localStorage.setItem("medicines", JSON.stringify(medicines));

    displayMedicines();

    document.getElementById("medName").value = "";
    document.getElementById("dosage").value = "";
}

// DISPLAY MEDICINES
function displayMedicines() {
    let output = document.getElementById("medList");
    output.innerHTML = "";

    if (medicines.length === 0) {
        output.innerHTML = "No medicines added yet.";
        return;
    }

    medicines.forEach((med, index) => {
        output.innerHTML += `
        <div style="border:1px solid #ccc; padding:10px; margin-top:10px; border-radius:10px;">
            <b>${med.name}</b><br>
            Dosage: ${med.dosage}<br>
            Time: ${med.timing}<br>
            ${med.food}<br><br>

            Status: <b style="color:${med.taken ? 'green' : 'red'}">
            ${med.taken ? 'Taken ✔' : 'Pending'}
            </b><br><br>

            <button onclick="markTaken(${index})">Mark as Taken</button>
            <button onclick="markMissed(${index})">Missed</button>
            <button onclick="deleteMedicine(${index})">Delete</button>
        </div>
        `;
    });
}

// MARK TAKEN
function markTaken(index) {
    medicines[index].taken = true;
    localStorage.setItem("medicines", JSON.stringify(medicines));
    displayMedicines();
    alert("Medicine taken 👍");
}

// MISSED DOSE
function markMissed(index) {
    medicines[index].taken = false;
    localStorage.setItem("medicines", JSON.stringify(medicines));
    displayMedicines();
    alert("⚠ You missed your dose!");
}

// DELETE
function deleteMedicine(index) {
    medicines.splice(index, 1);
    localStorage.setItem("medicines", JSON.stringify(medicines));
    displayMedicines();
}