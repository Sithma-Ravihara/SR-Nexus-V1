const searchForm = document.getElementById("searchForm");
const searchInput = document.getElementById("searchInput");

const API_URL = "https://sr-nexus-v2.vercel.app/api";

// ========================================
// RESULTS CONTAINER
// ========================================

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
// SEARCH API
// ========================================

async function search(query) {

    resultsContainer.innerHTML = `
        <div style="
            text-align:center;
            padding:30px;
            font-size:16px;
            opacity:0.8;
        ">
            🔎 Searching for
            <strong>${escapeHTML(query)}</strong>...
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

        console.log(
            "SR Nexus Search Results:",
            data
        );

        displayResults(data);

    } catch (error) {

        console.error(
            "SR Nexus API Error:",
            error
        );

        resultsContainer.innerHTML = `
            <div style="
                text-align:center;
                padding:40px;
            ">

                <h3>
                    ⚠️ Search Failed
                </h3>

                <p>
                    SR Nexus API could not be reached.
                </p>

                <p style="
                    opacity:0.6;
                    font-size:13px;
                ">
                    ${escapeHTML(error.message)}
                </p>

            </div>
        `;
    }
}

// ========================================
// DISPLAY RESULTS
// ========================================

function displayResults(data) {

    resultsContainer.innerHTML = "";

    if (
        !data.results ||
        data.results.length === 0
    ) {

        resultsContainer.innerHTML = `
            <div style="
                text-align:center;
                padding:50px 20px;
            ">

                <div style="
                    font-size:40px;
                    margin-bottom:15px;
                ">
                    🔍
                </div>

                <h3>
                    No results found
                </h3>

                <p style="opacity:0.7;">
                    No results found for
                    <strong>
                        ${escapeHTML(data.query)}
                    </strong>
                </p>

                ${
                    data.error
                    ?
                    `
                    <p style="
                        margin-top:15px;
                        opacity:0.5;
                        font-size:13px;
                    ">
                        ${escapeHTML(data.error)}
                    </p>
                    `
                    :
                    ""
                }

            </div>
        `;

        return;
    }

    // ========================================
    // HEADER
    // ========================================

    const header = document.createElement("div");

    header.style.marginBottom = "25px";

    header.innerHTML = `
        <h2 style="
            margin-bottom:8px;
        ">
            Search Results
        </h2>

        <p style="
            opacity:0.65;
        ">
            ${data.count}
            result${data.count === 1 ? "" : "s"}
            for
            <strong>
                ${escapeHTML(data.query)}
            </strong>
        </p>
    `;

    resultsContainer.appendChild(header);

    // ========================================
    // RESULT CARDS
    // ========================================

    data.results.forEach(
        (result, index) => {

            const card =
                document.createElement("div");

            card.style.marginBottom = "18px";

            card.style.padding = "22px";

            card.style.borderRadius = "18px";

            card.style.border =
                "1px solid rgba(255,255,255,0.12)";

            card.style.background =
                "rgba(255,255,255,0.045)";

            card.style.backdropFilter =
                "blur(12px)";

            card.style.boxShadow =
                "0 10px 30px rgba(0,0,0,0.15)";

            const title =
                escapeHTML(
                    result.title ||
                    "Untitled Result"
                );

            const content =
                escapeHTML(
                    result.content ||
                    result.description ||
                    "No description available."
                );

            const url =
                safeURL(result.url);

            card.innerHTML = `

                <div style="
                    font-size:12px;
                    opacity:0.5;
                    margin-bottom:8px;
                    letter-spacing:1px;
                ">
                    RESULT ${index + 1}
                </div>

                <h3 style="
                    margin:0 0 10px 0;
                    font-size:20px;
                ">
                    ${title}
                </h3>

                <p style="
                    margin:0 0 16px 0;
                    line-height:1.7;
                    opacity:0.75;
                ">
                    ${content}
                </p>

                ${
                    url
                    ?
                    `
                    <a
                        href="${url}"
                        target="_blank"
                        rel="noopener noreferrer"
                        style="
                            display:inline-block;
                            text-decoration:none;
                            font-weight:600;
                        "
                    >
                        Visit result →
                    </a>
                    `
                    :
                    ""
                }

            `;

            resultsContainer.appendChild(card);
        }
    );
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
// SAFE URL
// ========================================

function safeURL(value) {

    if (!value) {
        return "";
    }

    try {

        const url =
            new URL(value);

        if (
            url.protocol === "https:" ||
            url.protocol === "http:"
        ) {

            return escapeHTML(
                url.href
            );
        }

    } catch (error) {

        console.warn(
            "Invalid result URL:",
            value
        );
    }

    return "";
}

// ========================================
// QUICK SEARCH BUTTONS
// ========================================

document
    .querySelectorAll(
        ".quick-actions button"
    )
    .forEach(button => {

        button.addEventListener(
            "click",
            () => {

                const query =
                    button.dataset.query ||
                    "";

                searchInput.value =
                    query;

                searchInput.focus();

                if (query.trim()) {
                    search(query);
                }
            }
        );
    });
