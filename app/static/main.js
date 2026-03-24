document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("query-form");
    const input = document.getElementById("query-input");
    const submitBtn = document.getElementById("submit-btn");
    const submitIcon = submitBtn.querySelector("i");
    
    // Result elements
    const resultsContainer = document.getElementById("results-container");
    const loadingEl = document.getElementById("loading");
    const answerBox = document.getElementById("answer-box");
    const answerContent = document.getElementById("answer-content");
    const sourcesBox = document.getElementById("sources-box");
    const sourcesList = document.getElementById("sources-list");
    const errorBox = document.getElementById("error-box");
    const errorMessage = document.getElementById("error-message");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        const query = input.value.trim();
        if (!query) return;

        // UI state: Loading
        resultsContainer.classList.remove("hidden");
        loadingEl.classList.remove("hidden");
        answerBox.classList.add("hidden");
        sourcesBox.classList.add("hidden");
        errorBox.classList.add("hidden");
        
        // Disable input
        input.disabled = true;
        submitBtn.disabled = true;
        submitIcon.classList.replace("ph-paper-plane-right", "ph-spinner");
        submitIcon.classList.add("ph-spin");

        try {
            const res = await fetch("/api/query", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ query })
            });
            
            const data = await res.json();
            
            if (!res.ok) {
                throw new Error(data.error || `Server error: ${res.status}`);
            }

            // Render Answer
            answerContent.innerHTML = formatAnswer(data.answer);
            answerBox.classList.remove("hidden");

            // Render Sources
            if (data.sources && data.sources.length > 0) {
                sourcesList.innerHTML = "";
                // The backend returns an array of strings directly
                const uniqueSources = [...new Set(data.sources)];
                
                uniqueSources.forEach(sourceName => {
                    const li = document.createElement("li");
                    li.innerHTML = `<i class="ph ph-file-text"></i> ${sourceName}`;
                    sourcesList.appendChild(li);
                });
                sourcesBox.classList.remove("hidden");
            }
            
        } catch (err) {
            errorMessage.textContent = err.message || "An unexpected error occurred.";
            errorBox.classList.remove("hidden");
        } finally {
            // Restore UI state
            loadingEl.classList.add("hidden");
            input.disabled = false;
            submitBtn.disabled = false;
            submitIcon.classList.remove("ph-spin");
            submitIcon.classList.replace("ph-spinner", "ph-paper-plane-right");
            
            // Focus input for next query
            setTimeout(() => input.focus(), 100);
        }
    });

    // Helper to format the answer text nicely
    function formatAnswer(text) {
        if (!text) return "No answer generated.";
        // Escape basic HTML to prevent XSS
        let safeText = text.replace(/</g, "&lt;").replace(/>/g, "&gt;");
        
        // Convert basic markdown-style things if needed (though LLMs return complex markdown)
        // For a sophisticated UI, linking marked.js would be better, but this handles basic paragraphs:
        return safeText.split('\n\n').filter(p => p.trim()).map(p => `<p>${p}</p>`).join('');
    }
});
