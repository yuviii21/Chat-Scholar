document.addEventListener('DOMContentLoaded', () => {
  // Theme Toggle Logic
  const themeToggle = document.getElementById('themeToggle');
  const storedTheme = localStorage.getItem('cs-theme') || 'light';
  document.documentElement.setAttribute('data-theme', storedTheme);

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme') || 'light';
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('cs-theme', next);
    });
  }

  // File Upload Drag & Drop & Name Preview
  const input = document.querySelector('[data-file-input]');
  const name = document.querySelector('[data-file-name]');
  const zone = document.querySelector('[data-upload-zone]');

  if (input && name) {
    input.addEventListener('change', () => {
      if (input.files.length === 1) {
        name.textContent = input.files[0].name;
      } else if (input.files.length > 1) {
        name.textContent = `${input.files.length} documents selected`;
      } else {
        name.textContent = 'PDF files only';
      }
    });
  }

  if (zone) {
    ['dragenter', 'dragover'].forEach(event => {
      zone.addEventListener(event, (e) => {
        e.preventDefault();
        zone.classList.add('drag');
      });
    });

    ['dragleave', 'drop'].forEach(event => {
      zone.addEventListener(event, (e) => {
        e.preventDefault();
        zone.classList.remove('drag');
      });
    });

    if (input) {
      zone.addEventListener('drop', (e) => {
        if (e.dataTransfer && e.dataTransfer.files.length) {
          input.files = e.dataTransfer.files;
          input.dispatchEvent(new Event('change'));
        }
      });
    }
  }

  // Form Submission Loading State
  document.querySelectorAll('form[data-loading]').forEach(form => {
    form.addEventListener('submit', () => {
      const button = form.querySelector('button[type="submit"]');
      if (button && form.checkValidity()) {
        button.innerHTML = 'Analyzing sources…';
        button.disabled = true;
      }
    });
  });

  // Auto-scroll chat messages to latest
  const messagesContainer = document.querySelector('.messages');
  if (messagesContainer) {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }
});
