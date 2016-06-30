import _ from 'lodash';
import ko from 'knockout';

export const showTab = (toggle, tab) => {
	toggle.dispatchEvent(new CustomEvent('changeTab', {detail: {tab}}));

	// Hide all targets
	_.each(toggle.getElementsByClassName("toggle__item"), (i) => {
		const target = document.querySelector(i.dataset.toggle);
		target.style.display = 'none';
	});

	// Remove all active
	_.each(toggle.getElementsByClassName("toggle__item--active"), (i) => {
		i.classList.remove("toggle__item--active");
	});

	// Show our target
	tab.classList.add("toggle__item--active");
	const target = document.querySelector(tab.dataset.toggle);
	target.style.display = 'block';
};

export const init = () => {
	_.each(document.getElementsByClassName("toggle"), (toggle) => {
		_.each(toggle.getElementsByClassName("toggle__item"), (i) => {
			if (!i.classList.contains("toggle__item--active")) {
				const target = document.querySelector(i.dataset.toggle);
				target.style.display = 'none';
			}

			i.addEventListener('click', () => {
				showTab(toggle, i);
			});
		});
	});
};