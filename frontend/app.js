const searchForm = document.getElementById("searchForm");
const searchInput = document.getElementById("searchInput");

let resultsContainer = document.getElementById("searchResults");

if (!resultsContainer) {
    resultsContainer = document.createElement("div");
    resultsContainer.id = "searchResults";

    resultsContainer.style.maxWidth = "900px";
    resultsContainer.style.margin = "40px auto";
    resultsContainer.style.padding = "0 20px";

    searchForm.parentNode.appendChild(resultsContainer);
}


// ========================================
// SEARCH
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
// SR NEXUS SEARCH
// ========================================

function search(query) {

    resultsContainer.innerHTML = `
        <div style="
            text-align:center;
            padding:30px;
        ">
            🔎 Searching for
            <strong>${escapeHTML(query)}</strong>...
        </div>
    `;

    setTimeout(() => {

        const googleURL =
            "https://www.google.com/search?q=" +
            encodeURIComponent(query);

        const results = [
            {
                title: `${query} - Google Search`,
                description:
                    `Search the web for ${query} and discover the latest information, websites and resources.`,
                url: googleURL
            },
            {
                title: `Latest ${query} results`,
                description:
                    `Find websites, articles and information related to ${query}.`,
                url: googleURL
            },
            {
                title: `${query} information`,
                description:
                    `Explore more information about ${query} from web search results.`,
                url: googleURL
            }
        ];

        displayResults(query, results);

    }, 500);
}


// ========================================
// DISPLAY RESULTS
// ========================================

function displayResults(query, results) {

    resultsContainer.innerHTML = `

        <div style="
            margin-bottom:25px;
        ">

            <h2>
                Search Results
            </h2>

            <p style="opacity:.65;">
                ${results.length} results for
                <strong>
                    ${escapeHTML(query)}
                </strong>
            </p>

        </div>

    `;


    results.forEach((result, index) => {

        const card = document.createElement("div");

        card.style.marginBottom = "18px";
        card.style.padding = "22px";
        card.style.borderRadius = "18px";
        card.style.border =
            "1px solid rgba(255,255,255,.12)";
        card.style.background =
            "rgba(255,255,255,.045)";
        card.style.backdropFilter =
            "blur(12px)";

        card.innerHTML = `

            <div style="
                font-size:12px;
                opacity:.5;
                margin-bottom:8px;
                letter-spacing:1px;
            ">
                RESULT ${index + 1}
            </div>

            <h3 style="
                margin:0 0 10px;
                font-size:20px;
            ">
                ${escapeHTML(result.title)}
            </h3>

            <p style="
                line-height:1.7;
                opacity:.75;
                margin-bottom:16px;
            ">
                ${escapeHTML(result.description)}
            </p>

            <a
                href="${result.url}"
                target="_blank"
                rel="noopener noreferrer"
                style="
                    text-decoration:none;
                    font-weight:600;
                "
            >
                Visit result →
            </a>

        `;

        resultsContainer.appendChild(card);

    });
}


// ========================================
// SAFE HTML
// ========================================

function escapeHTML(value) {

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


// ========================================
// QUICK SEARCH
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
