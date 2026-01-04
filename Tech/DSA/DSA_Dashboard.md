```dataviewjs
// --- CONFIGURATION ---
const folder = "Tech/DSA/Questions";
const limit = 50; // Pagination: Show only 50 rows (Change this to see more)
const filterStatus = "All"; // Options: "All", "Solved", "To Do", "In Progress"
const filterDifficulty = "All"; // Options: "All", "Easy", "Medium", "Hard"

// --- LOGIC ---
// 1. Get all pages from the DSA folder
let pages = dv.pages(`"${folder}"`)
    .where(p => p.file.name != "DSA_Dashboard"); // Exclude the dashboard itself

// 2. Apply Filters
if (filterStatus !== "All") {
    pages = pages.where(p => p.status && p.status.includes(filterStatus));
}
if (filterDifficulty !== "All") {
    pages = pages.where(p => p.difficulty == filterDifficulty);
}

// 3. Sort by Creation Date (Newest First)
pages = pages.sort(p => p.file.ctime, "desc");

// 4. Pagination (Slice the array)
// Note: To see the next page, you would change 'limit' or add a 'start' variable manually.
// For true clickable pagination, a specialized plugin is better (see note below).
let visiblePages = pages.slice(0, limit);

// 5. Create Table Data with Serial Numbers
// We map the pages to the columns you requested
const tableData = visiblePages.map((p, index) => [
    index + 1,                          // 1. Serial Number
    p.file.link,                        // 2. Question Name (Link to Note)
    p.difficulty,                       // 3. Difficulty
    p.tags,                             // 4. Tags
    p.status,                           // 5. Status
    p.source,                           // 6. Source (LeetCode/CodeForces)
    p.review_date                       // 7. Review Date (Extra useful field)
]);

// 6. Render the Table
dv.header(2, `📚 Problem Database (${pages.length} Total Questions)`);
dv.table(
    ["SN", "Problem", "Difficulty", "Tags", "Status", "Source", "Review Due"], 
    tableData
);