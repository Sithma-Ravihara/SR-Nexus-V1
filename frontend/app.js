const searchForm = document.getElementById("searchForm");
const searchInput = document.getElementById("searchInput");

searchForm.addEventListener("submit", function (event) {

    event.preventDefault();

    const query = searchInput.value.trim();

    if (!query) {
        searchInput.focus();
        return;
    }

    search(query);
});


async function search(query) {

    /*
     * Backend API
     *
     * Local development:
     * http://127.0.0.1:8000/api/search
     */

    const API_URL = "http://127.0.0.1:8000/api/search";

    try {

        const response = await fetch(
            `${API_URL}?q=${encodeURIComponent(query)}`
        );

        if (!response.ok) {
            throw new Error("Search API error");
        }

        const data = await response.json();

        console.log("SR Nexus Results:", data);

        alert(
            `Search completed!\n\nQuery: ${data.query}\nResults: ${data.results.length}`
        );

    } catch (error) {

        console.error(error);

        alert(
            "SR Search API is not connected yet."
        );
    }
}


document
    .querySelectorAll(".quick-actions button")
    .forEach(button => {

        button.addEventListener("click", () => {

            searchInput.value =
                button.dataset.query;

            searchInput.focus();

        });

    });
