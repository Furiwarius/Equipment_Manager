async function loguot() {
    localStorage.removeItem('authToken');
    window.location.href = '/authorization';
}