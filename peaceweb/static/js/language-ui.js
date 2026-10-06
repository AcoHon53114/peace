(function () {
  'use strict';
  const form = document.querySelector('.language-switcher');
  if (!form) return;
  // A language reload would lose file selections and unsent form data.
  // Update the preference without reloading while a form is being edited.
  let dirty = false;
  document.querySelectorAll('form:not(.language-switcher)').forEach(function (other) {
    other.addEventListener('input', function () { dirty = true; });
    other.addEventListener('change', function () { dirty = true; });
  });
  const select = form.querySelector('select');
  let previous = select.value;
  const custom = form.querySelector('.language-custom');
  const toggle = form.querySelector('.language-toggle');
  const options = form.querySelector('.language-options');
  const choices = Array.from(options.querySelectorAll('[data-language]'));
  const labels = {'en':'EN','zh-hant':'繁','zh-hans':'简'};
  function refresh() {
    form.querySelector('.language-current').textContent = labels[select.value];
    choices.forEach(function (choice) { choice.setAttribute('aria-current', String(choice.dataset.language === select.value)); });
  }
  function close(focus) { options.hidden = true; toggle.setAttribute('aria-expanded','false'); if (focus) toggle.focus(); }
  custom.hidden = false;
  select.classList.add('language-enhanced');
  refresh();
  const nav = form.closest('.navbar');
  const container = nav.querySelector('.container');
  const brand = nav.querySelector('.navbar-brand');
  const links = nav.querySelector('.navbar-nav');
  const control = nav.querySelector('.language-control');
  function fitNavigation() {
    nav.classList.remove('nav-compact');
    if (window.innerWidth < 992) return;
    const style = window.getComputedStyle(container);
    const available = container.clientWidth - parseFloat(style.paddingLeft) - parseFloat(style.paddingRight);
    const required = brand.getBoundingClientRect().width + links.scrollWidth + control.getBoundingClientRect().width + 24;
    nav.classList.toggle('nav-compact', required > available);
  }
  window.addEventListener('resize', fitNavigation);
  fitNavigation();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitNavigation);

  toggle.addEventListener('click', function () {
    if (!options.hidden) { close(false); return; }
    options.hidden = false; toggle.setAttribute('aria-expanded','true');
    choices.find(function (choice) { return choice.dataset.language === select.value; }).focus();
  });
  choices.forEach(function (choice) {
    choice.addEventListener('click', function () {
      if (select.disabled) return;
      close(true);
      if (choice.dataset.language === select.value) return;
      select.value = choice.dataset.language;
      select.dispatchEvent(new Event('change', {bubbles:true}));
    });
  });
  document.addEventListener('click', function (event) { if (!custom.contains(event.target)) close(false); });
  custom.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') { close(true); event.preventDefault(); }
    if (!options.hidden && (event.key === 'ArrowDown' || event.key === 'ArrowUp')) {
      event.preventDefault();
      const index = choices.indexOf(document.activeElement);
      choices[(index + (event.key === 'ArrowDown' ? 1 : -1) + choices.length) % choices.length].focus();
    }
  });
  custom.addEventListener('focusout', function (event) {
    // Safari may report no next focus target when tapping an option.
    // Closing here would hide the option before its click can run.
    // Outside clicks and Escape still close the dropdown.
    if (event.relatedTarget && !custom.contains(event.relatedTarget)) close(false);
  });

  select.addEventListener('change', async function () {
    form.elements.next.value = window.location.pathname + window.location.search + window.location.hash;
    if (!dirty) { form.submit(); return; }
    select.disabled = true;
    const body = new FormData(form);
    body.set('language', select.value);
    try {
      const response = await fetch(form.action, {
        method: 'POST', body: body, credentials: 'same-origin',
        headers: {'Accept': 'application/json'}
      });
      if (!response.ok) throw new Error('Language update failed');
      previous = select.value;
      refresh();
      const messages = {
        'zh-hant': '已記住語言選擇。為保留未提交的資料，本頁暫維持原語言；提交表單或前往下一頁後套用。',
        'zh-hans': '已记住语言选择。为保留未提交的数据，本页暂时保持原语言；提交表单或进入下一页后生效。',
        'en': 'Language preference saved. This page will keep its current language to preserve your unsent data. The selected language will apply after submission or on the next page.'
      };
      let note = form.querySelector('[role="status"]');
      if (!note) { note = document.createElement('small'); note.setAttribute('role', 'status'); note.style.display='block'; note.style.maxWidth='18rem'; form.appendChild(note); }
      note.textContent = messages[select.value];
    } catch (error) {
      select.value = previous;
      refresh();
      let note = form.querySelector('[role="status"]');
      if (!note) { note = document.createElement('small'); note.setAttribute('role', 'status'); form.appendChild(note); }
      note.textContent = {'zh-hant':'語言未能更新，請稍後重試。','zh-hans':'语言未能更新，请稍后重试。','en':'Unable to update language. Please try again.'}[previous];
    } finally { select.disabled = false; }
  });
})();
