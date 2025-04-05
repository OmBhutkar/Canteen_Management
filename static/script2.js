// JavaScript to toggle between login and signup forms
const loginForm = document.getElementById('login-form');
const signupForm = document.getElementById('signup-form');
const loginBtn = document.getElementById('login-btn');
const signupBtn = document.getElementById('signup-btn');

loginBtn.addEventListener('click', () => {
    loginForm.classList.add('active');
    signupForm.classList.remove('active');
});

signupBtn.addEventListener('click', () => {
    signupForm.classList.add('active');
    loginForm.classList.remove('active');
});
