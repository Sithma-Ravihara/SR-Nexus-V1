const searchForm = document.getElementById("searchForm");
const searchInput = document.getElementById("searchInput");

searchForm.addEventListener("submit", function (event) {

    event.preventDefault();

    const query = searchInput.value.trim();

    if (!query) {
        searchInput.focus();
        return;
    }

    /*
     * Temporary search action.
     *
     * Backend API එක හදනකම්
     * search query එක URL එකට පෙන්වනවා.
     */

    const searchURL =
        `?q=${encodeURIComponent(query)}`;

    window.location.href = searchURL;
});


/*
 * Quick search buttons
 */

document
    .querySelectorAll(".quick-actions button")
    .forEach(button => {

        button.addEventListener("click", () => {

            const query =
                button.dataset.query;

            searchInput.value = query;

            searchInput.focus();

        });

    });
