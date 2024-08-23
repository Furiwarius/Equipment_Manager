const clientTimeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;
document.getElementById('timezone').value = clientTimeZone;