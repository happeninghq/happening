import _ from 'lodash';

export const showTab = (toggle, tab) => {
	toggle.dispatchEvent(new CustomEvent('changeTab', {detail: {tab}}));

	// Hide all targets
	_.each(toggle.getElementsByClassName("toggle__item"), (i) => {
		const target = document.querySelector(i.dataset.toggle);
		if (target) {
			target.style.display = 'none';
		}
	});

	// Remove all active
	_.each(toggle.getElementsByClassName("toggle__item--active"), (i) => {
		i.classList.remove("toggle__item--active");
	});

	// Show our target
	tab.classList.add("toggle__item--active");
	const target = document.querySelector(tab.dataset.toggle);
	if (target != null) {
		target.style.display = 'block';
	}

	// If needed, update the field value
	if (toggle.dataset['selected-tab-field']) {
		const field = document.querySelector(toggle.dataset['selected-tab-field']);
		field.value = tab.dataset.value;
	}

	// If there is a single link contained in this tab - click it
	const aChildren = tab.getElementsByTagName("a");
	if (aChildren.length == 1) {
		aChildren[0].click();
	}
};

export const init = () => {
	_.each(document.getElementsByClassName("toggle"), (toggle) => {
		let initial_value = null;
		if (toggle.dataset['selected-tab-field']) {
			const field = document.querySelector(toggle.dataset['selected-tab-field']);
			initial_value = field.value;
		}

		_.each(toggle.getElementsByClassName("toggle__item"), (i) => {
			if (!i.classList.contains("toggle__item--active")) {
				const target = document.querySelector(i.dataset.toggle);
				if (target) {
					target.style.display = 'none';
				}
			}

			i.addEventListener('click', () => {
				showTab(toggle, i);
			});

			if (i.dataset.value && i.dataset.value == initial_value) {
				showTab(toggle, i);
			}
		});
	});
};