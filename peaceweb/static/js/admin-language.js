/* Native POST preserves Safari touch and keyboard behaviour. */
(() => {
  'use strict';
  const languageForm = document.getElementById('admin-language-form');
  if (!languageForm) return;
  const languageSelect = document.getElementById('admin-language-select');
  const currentLanguage = languageSelect.value;
  let dirty = false;
  document.querySelectorAll('#content form').forEach(form => {
    if (form.id === 'changelist-search') return;
    form.addEventListener('input', () => { dirty = true; });
    form.addEventListener('change', () => { dirty = true; });
  });
  languageForm.addEventListener('submit', event => {
    if (dirty && !window.confirm(languageForm.dataset.unsavedMessage)) {
      event.preventDefault();
      languageSelect.value = currentLanguage;
    }
  });
})();
