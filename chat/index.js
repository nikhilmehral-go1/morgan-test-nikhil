document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chat-form");
    const chatInput = document.getElementById("chat-input");
    const chatWindow = document.getElementById("chat-window");

    // --- CONFIGURATION ---
    // Replace this with your actual bearer token
    const BEARER_TOKEN = "";
    const API_URL = "http://localhost:8000/api/v1/ask";

    chatForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const userMessage = chatInput.value.trim();

        if (!userMessage) return;

        // Display user's message
        appendMessage(userMessage, "user-message");
        chatInput.value = "";

        try {
            // Display a thinking indicator
            appendMessage("...", "agent-message", true);

            const response = await fetch(API_URL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${BEARER_TOKEN}`,
                },
                body: JSON.stringify({ question: userMessage }),
            });

            // Remove the thinking indicator
            removeThinkingIndicator();

            if (!response.ok) {
                throw new Error(`API Error: ${response.statusText}`);
            }

            const data = await response.json();
            appendMessage(data.answer, "agent-message");

        } catch (error) {
            console.error("Failed to get response:", error);
            removeThinkingIndicator();
            appendMessage("Sorry, something went wrong. Please check the console.", "agent-message");
        }
    });

    function appendMessage(text, className, isThinking = false) {
        const messageElement = document.createElement("div");
        messageElement.className = `message ${className}`;
        messageElement.textContent = text;
        if (isThinking) {
            messageElement.id = "thinking-indicator";
        }
        chatWindow.appendChild(messageElement);
        chatWindow.scrollTop = chatWindow.scrollHeight; // Auto-scroll to bottom
    }

    function removeThinkingIndicator() {
        const indicator = document.getElementById("thinking-indicator");
        if (indicator) {
            indicator.remove();
        }
    }
});
