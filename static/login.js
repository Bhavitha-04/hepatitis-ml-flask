// =====================
// Sample users
// =====================
if (!localStorage.getItem("users")) {
    let users = [
        {name: "Sita", phone: "1234567890", age: 25, gender: "Female", thyroid: true, pcos: false, pregnancy: false},
        {name: "Gita", phone: "2345678901", age: 28, gender: "Female", thyroid: false, pcos: true, pregnancy: false},
        {name: "Radha", phone: "3456789012", age: 30, gender: "Female", thyroid: false, pcos: false, pregnancy: true},
    ];
    localStorage.setItem("users", JSON.stringify(users));
}

// =====================
// Show/hide sections
// =====================
function showNewUser() {
    document.getElementById('login-section').style.display = 'none';
    const newUser = document.getElementById('newuser-section');
    newUser.style.display = 'block';
    newUser.classList.add('fade-in-quick'); // Triggers the slide-up again
}

function showLogin() {
    document.getElementById('newuser-section').style.display = 'none';
    const login = document.getElementById('login-section');
    login.style.display = 'block';
    login.classList.add('fade-in-quick'); // Triggers the slide-up again
}

// =====================
// Create new user
// =====================
function createUser() {
    let name = document.getElementById("newName").value.trim();
    let phone = document.getElementById("newPhone").value.trim();
    let age = document.getElementById("newAge").value;
    let gender = document.getElementById("newGender").value;
    let thyroid = document.getElementById("newThyroid").checked;
    let pcos = document.getElementById("newPCOS").checked;
    let pregnancy = document.getElementById("newPregnancy").checked;

    if (!name || !phone || !age || !gender) {
        alert("Please fill all required fields");
        return;
    }

    let users = JSON.parse(localStorage.getItem("users")) || [];
    // Check duplicate name
    if (users.some(u => u.name.toLowerCase() === name.toLowerCase())) {
        alert("User with this name already exists!");
        return;
    }

    users.push({name, phone, age, gender, thyroid, pcos, pregnancy});
    localStorage.setItem("users", JSON.stringify(users));
    alert("User created successfully!");
    showLogin();
}

// =====================
// Login function
// =====================
function login() {
    let name = document.getElementById("loginName").value.trim();
    if (!name) {
        alert("Enter name to login");
        return;
    }

    let users = JSON.parse(localStorage.getItem("users")) || [];
    let user = users.find(u => u.name.toLowerCase() === name.toLowerCase());

    if (user) {
        localStorage.setItem("currentUser", JSON.stringify(user));
        window.location.href = "/ui";
    } else {
        alert("User not found! Please create new login.");
    }
}
document.getElementById("loginName").addEventListener("keypress",function(e){
if(e.key==="Enter"){
login();
}
});
const text = "Analyzing blood reports using Artificial Intelligence...";
let i = 0;

function typingEffect(){
    if(i < text.length){
        document.querySelector(".typing").innerHTML += text.charAt(i);
        i++;
        setTimeout(typingEffect,40);
    }
}

typingEffect();