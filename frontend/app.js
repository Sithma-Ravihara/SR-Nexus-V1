const searchForm = document.getElementById("searchForm");
const searchInput = document.getElementById("searchInput");

// ========================================
// SEARCH FORM
// ========================================

searchForm.addEventListener("submit", function (event) {

    event.preventDefault();

    const query = searchInput.value.trim();

    if (!query) {
        searchInput.focus();
        return;
    }

    search(query);
});


// ========================================
// GOOGLE SEARCH
// ========================================

function search(query) {

    const googleURL =
        "https://www.google.com/search?q=" +
        encodeURIComponent(query);

    window.location.href = googleURL;
}


// ========================================
// QUICK SEARCH BUTTONS
// ========================================

document
    .querySelectorAll(".quick-actions button")
    .forEach(button => {

        button.addEventListener("click", () => {

            const query =
                button.dataset.query || "";

            if (!query.trim()) {
                return;
            }

            searchInput.value = query;

            search(query);

        });

    });
