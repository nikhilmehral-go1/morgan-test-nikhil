document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chat-form");
    const chatInput = document.getElementById("chat-input");
    const chatWindow = document.getElementById("chat-window");

    // --- CONFIGURATION ---
    // Replace this with your actual bearer token
    const BEARER_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnbzEuYWNjZXNzIiwidmVyIjoidjEuMCIsImV4cCI6MTc1NDk3Njg5Mywic2lkIjoiN2FkZDM5YTNjZTVhZmUyNTNlZDM3ZDAyN2ZjNzk1OTVmYWVmZDYwZTEyYzA4NjNjMjgxZGM5ZjMxZGZmZTlhOTQ2YTAxZjc5NzQ0NDYzMWJlMjk1MGRjMTRjYTI0ZmE5NTAxYzgyZDAwNGFlZjRkMTgwYzE2ODM5MTYzZDA0MzEwcmVnMGF1c3RyYWxpYWVhc3QiLCJzdWIiOiJ1c3JfMDFGNDNTNDZGRzZNV0tDQ0hRNjRUM0NDMUsiLCJvYmplY3QiOnsidHlwZSI6InVzZXIiLCJjb250ZW50Ijp7ImlkIjo1OTYyNzE0LCJpbnN0YW5jZSI6ImFjY291bnRzLmdvY2F0YWx5emUuY29tIiwicHJvZmlsZV9pZCI6NTk2MjcxNCwibmFtZSI6Ik5pa2hpbCBNZWhyYWwiLCJyb2xlcyI6WyJkZXZlbG9wZXIiXSwibWFpbCI6Im5pa2hpbC5tZWhyYWxAZ28xLmNvbSIsImdpdmVuX25hbWUiOiJOaWtoaWwiLCJmYW1pbHlfbmFtZSI6Ik1laHJhbCIsImFjY291bnRzIjpbeyJpZCI6MzgzODE5OTMsImluc3RhbmNlIjoiYWktYWdlbnQubXlnbzEuY29tIiwicHJvZmlsZV9pZCI6MzgzODE5OTMsIm5hbWUiOiJOaWtoaWwgTWVocmFsIiwicm9sZXMiOlsiYWRtaW5pc3RyYXRvciIsIlN0dWRlbnQiXSwicG9ydGFsX2lkIjozNjU4MTEzMSwicGFydG5lcl9wb3J0YWxfaWQiOjAsInVsaWQiOiJhY2NfMDFLMDVUSEFOWTREQlFLRU1IU1MwUkRZVFoifV0sIm1pZ3JhdGVkIjowfX0sInVzZWRDcmVkcyI6MSwiaWF0IjoxNzU0MzcyMDkzfQ.MBySf_CARg8h4jKxIcSwIeDOKTxlNwqXt_BHjr7s6k0oAW9r7YNM6YD5z8rGCZITeRQHJZDOaHu7L3l2MkfPInSXhLnyqBi_8cU63DDptbhkHfdwzrkfNk3bRROi5i_sk8W3v7xta_d_nSIDIWHArBImHpgnui42zYfphqmClbYGuTlqVguzwoUNMqujpQvzN4lYJaxZln8eA8o-EXrF9HDt4p-T0jw7tQHp2YJ0U6RiyUipjLYgLqY1NXh_bkKGhN_zL3fNROY3fYcigSJAq0OwU5rsSaTmG3yfcQmFXtl4ZHIW0cXpv1NowGW-MXJ0UAjG1F3HIvA9GsGjqR6UUg";
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
