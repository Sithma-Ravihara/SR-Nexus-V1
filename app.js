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

    // Online SR Nexus Backend API
    const API_URL = "https://sr-nexus-v1.vercel.app/api/search";

    try {

        const response = await fetch(
            `${API_URL}?q=${encodeURIComponent(query)}`
        );

        if (!response.ok) {
            throw new Error(`Search API error: ${response.status}`);
        }

        const data = await response.json();

        console.log("SR Nexus Results:", data);

        alert(
            `Search completed!\n\nQuery: ${data.query}\nResults: ${data.results.length}`
        );

    } catch (error) {

        console.error("SR Nexus API Error:", error);

        alert(
            "SR Search API is not connected."
        );
    }
}


// Quick search buttons
document
    .querySelectorAll(".quick-actions button")
    .forEach(button => {

        button.addEventListener("click", () => {

            const query = button.dataset.query;

            searchInput.value = query;

            searchInput.focus();

        });

    });
