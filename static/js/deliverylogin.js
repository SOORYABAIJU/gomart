function debounce(func, delay) {
	let timeoutId;

	return function (...args) {
		const context = this;

		clearTimeout(timeoutId);

		timeoutId = setTimeout(() => func.apply(context, args), delay);
	};
}

/**
 * Table Instance
 */

const defaults = {
	data: [],
	elements: { table: "#table", body: "#body", empty: "#empty" }
};

class Table {
	constructor(config = {}) {
		this.config = Object.assign({}, defaults, config);

		this.table = document.querySelector(this.config.elements.table);
		this.body = document.querySelector(this.config.elements.body);
		this.empty = document.querySelector(this.config.elements.empty);

		this.initial = this.config.data;

		this.data = [...this.initial];
		this.columns = [
			"checkbox",
			"invoice",
			"contact",
			"company",
			"progress",
			"details",
			"datetime",
			"status",
			"amount"
		];
		this.rows = [];
		this.total = this.initial.length;

		this.init();
	}

	init() {
		this.validate();

		this.limit = 5;
		this.total = this.initial.length;

		this.sort("datetime", "asc");

		this.limitEl = this.table.querySelector("[data-limit]");
		this.totalEl = this.table.querySelector("[data-total]");
		this.loadMoreEl = document.querySelector("[data-load-more]");

		if (this.limitEl) this.limitEl.textContent = this.limit;
		if (this.totalEl) this.totalEl.textContent = this.total;

		if (this.loadMoreEl) {
			this.loadMoreEl.addEventListener("click", () => this.loadMore());
		}
	}

	// Data Methods

	retrieve(item, key) {
		if (key === "invoice") return item.invoice.title;
		if (key === "contact") return item.contact.title;
		if (key === "company") return item.company;
		if (key === "progress") return parseInt(item.progress);
		if (key === "datetime")
			return new Date(`${item.datetime.date} ${item.datetime.time}`).getTime();
		if (key === "status") return item.status;
		if (key === "amount") return parseFloat(item.amount.replace(",", ""));

		return null;
	}

	create(key, value) {
		const cell = document.createElement("div");

		cell.classList.add("table__td");

		switch (key) {
			case "checkbox":
				cell.classList.add("fixed");

				cell.innerHTML = `
                    <div class="table-checkbox">
                        <label title="Select row" tabindex="0">
                            <input hidden type="checkbox" ${
																													value ? "checked" : ""
																												}>
                        </label>
                    </div>
                `;
				break;
			case "invoice":
				cell.classList.add("fixed");

				cell.innerHTML = `
                    <a title="${value.title}" href="${value.url}" target="_blank" class="table-link">
                        <span>${value.title}</span>
                    </a>
                `;
				break;
			case "contact":
				cell.innerHTML = `
                    <a title="${value.title}" href="mailto:${value.email}" class="table-contact">
                        <img src="${value.img_url}" alt="${value.title}" class="table-contact__image">
                        <div class="table-contact__data">
                            <div class="table-contact__name">${value.title}</div>
                            <div class="table-contact__email">${value.email}</div>
                        </div>
                    </a>
                `;
				break;
			case "company":
				cell.innerHTML = `
                    <div class="table-text">${value}</div>
                `;
				break;
			case "progress":
				cell.innerHTML = `
                    <div class="table-progress">
                        <div class="table-progress__bar"><span style="width: ${value}%"></span></div>
                        <div class="table-progress__value">${value}%</div>
                    </div>
                `;
				break;
			case "details":
				cell.innerHTML = `
                    <div class="table-text details">${value}</div>
                `;
				break;
			case "datetime":
				cell.innerHTML = `
                    <div class="table-datetime">
                        <div class="table-datetime__date">${value.date}</div>
                        <div class="table-datetime__time">${value.time}</div>
                    </div>
                `;
				break;
			case "status":
				cell.innerHTML = `
                    <div class="table-status ${value}">${value}</div>
                `;
				break;
			case "amount":
				cell.classList.add("fixed");

				cell.innerHTML = `
                    <div class="table-text amount">$${value}</div>
                `;
				break;
		}

		return cell;
	}

	// Data Actions

	sort(key, type = "asc") {
		this.data = this.initial.sort((a, b) => {
			const valA = this.retrieve(a, key);
			const valB = this.retrieve(b, key);

			let result;
			if (typeof valA === "number" && typeof valB === "number") {
				result = valA - valB;
			} else {
				result = String(valA).localeCompare(String(valB), undefined, {
					numeric: true
				});
			}

			if (key === "datetime") result *= -1;

			return type === "desc" ? -result : result;
		});

		this.total = this.data.length;
		this.limit = Math.min(5, this.total);
		this.update();
	}

	filter(key, value) {
		if (value === "all") {
			this.data = this.initial;
			this.total = this.initial.length;
			this.limit = Math.min(5, this.total);
			this.loadMoreEl.classList.remove("hidden");
		} else {
			this.data = this.initial.filter(
				(item) => this.retrieve(item, key) === value
			);
			this.total = this.data.length;
			this.limit = Math.min(5, this.total);
		}

		this.update();
	}

	search(keys, value) {
		if (!value) {
			this.data = this.initial;
			this.total = this.initial.length;
			this.limit = Math.min(5, this.total);
			this.update();

			return;
		}

		const search = value.toLowerCase().replaceAll(" ", "");

		this.data = this.initial.filter((item) => {
			const values = keys.map((key) => {
				return this.retrieve(item, key).toLowerCase().replaceAll(" ", "");
			});

			return values.some((val) => val.includes(search));
		});

		this.total = this.data.length;
		this.limit = Math.min(this.limit, this.total);
		this.update();
	}

	select(value) {
		const updateCheckboxes = () => {
			const checkboxes = this.body.querySelectorAll('input[type="checkbox"]');
			if (!checkboxes.length) return;
			checkboxes.forEach((checkbox) => (checkbox.checked = value));
		};

		updateCheckboxes();

		const observer = new MutationObserver(updateCheckboxes);
		observer.observe(this.body, { childList: true, subtree: true });
	}

	// Table Actions

	validate() {
		if (!this.table) throw new Error("Mount point is not defined");
		if (!this.body) throw new Error("Table body is not defined");

		if (!this.empty) console.warn('"Nothing Found" template is not defined');
	}

	loadMore() {
		const prevLimit = this.limit;
		this.limit = Math.min(this.limit + 5, this.total);

		if (this.limit >= this.total) {
			this.loadMoreEl.classList.add("hidden");
		}

		this.appendRows(prevLimit);
	}

	appendRows(start) {
		const rows = this.data.slice(start, this.limit).map((item, index) => {
			const row = document.createElement("div");

			row.classList.add("table__tr", "animate");
			row.style.animationDelay = `${index * 0.2}s`;

			this.columns.forEach((key) => {
				const cell = this.create(key, item[key]);

				row.appendChild(cell);
			});

			return row;
		});

		rows.forEach((row) => this.body.appendChild(row));

		if (this.limitEl) this.limitEl.textContent = this.limit;
	}

	update() {
		const rows = [];

		this.data.slice(0, this.limit).forEach((item) => {
			const row = document.createElement("div");

			row.classList.add("table__tr");
			row.classList.add("animate");

			this.columns.forEach((key) => {
				const cell = this.create(key, item[key]);

				row.appendChild(cell);
			});

			rows.push(row);
		});

		this.rows = rows;

		this.mount();

		if (this.loadMoreEl) {
			if (this.limit < this.total) {
				this.loadMoreEl.classList.remove("hidden");
			} else {
				this.loadMoreEl.classList.add("hidden");
			}
		}
	}

	mount() {
		this.body.innerHTML = "";

		if (!this.rows.length && this.empty) {
			const empty = this.empty.content.cloneNode(true);

			this.body.appendChild(empty);

			return;
		}

		this.rows.forEach((row, index) => {
			setTimeout(() => {
				this.body.appendChild(row);
			}, 200 * index);
		});

		if (this.limitEl) this.limitEl.textContent = this.limit;
		if (this.totalEl) this.totalEl.textContent = this.total;
	}
}

document.addEventListener("DOMContentLoaded", async () => {
	try {
		const response = await fetch(
			"https://bato-web-agency.github.io/bato-shared/table-view/assets/data.json?v=1"
		);

		const data = await response.json();

		const table = new Table({ data: data.data });

		/**
		 * Table controls
		 */

		/* Checkboxes */
		const selection = document.querySelector("#head [data-control=checkbox]");

		selection.addEventListener("change", () => {
			if (selection.dataset.select === "all") {
				table.select(true);
				selection.setAttribute("data-select", "none");
				return;
			}

			if (selection.dataset.select === "none") {
				table.select(false);
				selection.setAttribute("data-select", "all");
				return;
			}
		});

		/* Sort */
		const controls = [
			...document.querySelectorAll(
				"#head [data-control]:not([data-control=checkbox])"
			)
		];

		controls.forEach((control) => {
			function sortHandler() {
				table.sort(control.dataset.control, control.dataset.sort);

				if (control.dataset.sort === "desc") {
					control.setAttribute("data-sort", "asc");
					return;
				}

				if (control.dataset.sort === "asc") {
					control.setAttribute("data-sort", "desc");
					return;
				}
			}

			control.addEventListener("click", debounce(sortHandler, 250));
		});

		/* Search */
		const search = document.querySelector("#filter-search input[name=search]");

		function searchHandler() {
			table.search(["invoice", "contact", "company"], search.value.toLowerCase());
		}

		search.addEventListener("input", debounce(searchHandler, 500));

		/* Filter */
		const select = document.querySelector("#filter-select");

		document.addEventListener("click", (event) => {
			event.stopPropagation();
			select.classList.remove("active");
		});

		const trigger = select.querySelector("input[name=status]");
		const options = [...select.querySelectorAll("[data-option]")];

		select.addEventListener("click", (event) => {
			event.stopPropagation();
			select.classList.toggle("active");
		});

		options.forEach((option) => {
			option.addEventListener("click", (event) => {
				event.stopPropagation();
				options.forEach((option) => option.classList.remove("selected"));

				trigger.value = option.textContent;
				trigger.dispatchEvent(new Event("change"));

				option.classList.add("selected");
				select.classList.remove("active");
			});
		});

		function filterHandler() {
			table.filter("status", trigger.value.toLowerCase());
		}

		trigger.addEventListener("change", debounce(filterHandler, 250));
	} catch (error) {
		console.error("Error loading JSON:", error);
	}
});
