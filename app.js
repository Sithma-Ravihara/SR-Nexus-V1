const searchForm = document.getElementById("searchForm");
const searchInput = document.getElementById("searchInput");

const API_URL = "https://sr-nexus-v1.vercel.app/api/search";


// Create results area automatically
let resultsContainer = document.getElementById("searchResults");

if (!resultsContainer) {
    resultsContainer = document.createElement("div");
    resultsContainer.id = "searchResults";

    resultsContainer.style.maxWidth = "900px";
    resultsContainer.style.margin = "40px auto";
    resultsContainer.style.padding = "0 20px";

    searchForm.parentNode.appendChild(resultsContainer);
}


// Search form
searchForm.addEventListener("submit", function (event) {

    event.preventDefault();

    const query = searchInput.value.trim();

    if (!query) {
        searchInput.focus();
        return;
    }

    search(query);
});


// Search function
async function search(query) {

    resultsContainer.innerHTML = `
        <div style="
            text-align:center;
            padding:30px;
            opacity:0.8;
        ">
            🔎 Searching for <strong>${escapeHTML(query)}</strong>...
        </div>
    `;

    try {

        const response = await fetch(
            `${API_URL}?q=${encodeURIComponent(query)}`
        );

        if (!response.ok) {
            throw new Error(
                `API Error: ${response.status}`
            );
        }

        const data = await response.json();

        console.log("SR Nexus:", data);

        displayResults(data);

    } catch (error) {

        console.error("SR Nexus Error:", error);

        resultsContainer.innerHTML = `
            <div style="
                text-align:center;
                padding:30px;
            ">
                <h3>⚠️ Search failed</h3>
                <p>SR Nexus API could not be reached.</p>
            </div>
        `;
    }
}


// Display results
function displayResults(data) {

    resultsContainer.innerHTML = "";

    if (!data.results || data.results.length === 0) {

        resultsContainer.innerHTML = `
            <div style="
                text-align:center;
                padding:40px;
            ">
                <h3>🔍 No results found</h3>
                <p>
                    No results found for
                    <strong>${escapeHTML(data.query)}</strong>
                </p>
            </div>
        `;

        return;
    }


    // Result header
    const header = document.createElement("div");

    header.style.marginBottom = "20px";

    header.innerHTML = `
        <h2>
            Search Results
        </h2>

        <p style="opacity:0.7;">
            ${data.count} result${data.count === 1 ? "" : "s"}
            for
            <strong>${escapeHTML(data.query)}</strong>
        </p>
    `;

    resultsContainer.appendChild(header);


    // Result cards
    data.results.forEach((result, index) => {

        const card = document.createElement("div");

        card.style.marginBottom = "18px";
        card.style.padding = "22px";
        card.style.borderRadius = "16px";
        card.style.border = "1px solid rgba(255,255,255,0.12)";
        card.style.background = "rgba(255,255,255,0.04)";
        card.style.backdropFilter = "blur(10px)";


        const title = escapeHTML(
            result.title || "Untitled"
        );

        const content = escapeHTML(
            result.content || result.description || ""
        );

        const url = result.url || "#";


        card.innerHTML = `
            <div style="
                font-size:13px;
                opacity:0.5;
                margin-bottom:8px;
            ">
                RESULT ${index + 1}
            </div>

            <h3 style="
                margin:0 0 10px 0;
            ">
                ${title}
            </h3>

            <p style="
                line-height:1.6;
                opacity:0.75;
                margin-bottom:14px;
            ">
                ${content}
            </p>

            ${
                url !== "#"
                ? `
                    <a
                        href="${escapeAttribute(url)}"
                        target="_blank"
                        rel="noopener noreferrer"
                        style="
                            text-decoration:none;
                            font-weight:600;
                        "
                    >
                        Visit result →
                    </a>
                `
                : ""
            }
        `;

        resultsContainer.appendChild(card);
    });
}


// Prevent HTML injection
function escapeHTML(value) {

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


// Prevent unsafe URL attributes
function escapeAttribute(value) {

    return String(value)
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


// Quick action buttons
document
    .querySelectorAll(".quick-actions button")
    .forEach(button => {

        button.addEventListener("click", () => {

            const query = button.dataset.query || "";

            searchInput.value = query;

            searchInput.focus();

            if (query.trim()) {
                search(query);
            }

        });

    });
