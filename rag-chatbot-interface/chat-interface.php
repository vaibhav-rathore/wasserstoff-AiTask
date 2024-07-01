<?php
/*
Plugin Name: RAG Chatbot Interface
Description: A plugin to add a chatbot interface to WordPress.
Version: 1.0
Author: Vaibhav
*/

if (!defined('ABSPATH')) {
    exit;
}

function chatbot_interface() {
    echo '<div id="chatbot"></div>';
    echo '
    <style>
        #chatbot {
            position: fixed;
            bottom: 0;
            right: 0;
            width: 300px;
            height: 400px;
            border: 1px solid #ccc;
            background: #fff;
            padding: 10px;
        }
    </style>';
    echo '
    <script>
        async function sendMessage(message) {
            try {
                const response = await fetch("http://localhost:5000/search", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ query: message })
                });

                if (!response.ok) {
                    throw new Error("Network response was not ok " + response.statusText);
                }

                const data = await response.json();
                return data.results;
            } catch (error) {
                console.error("There was a problem with the fetch operation:", error);
                return ["Error: Could not process the request."];
            }
        }

        document.getElementById("chatbot").innerHTML = `
            <div id="chat-log"></div>
            <input type="text" id="chat-input" placeholder="Type your message here..." />
            <button onclick="sendChatMessage()">Send</button>
        `;

        async function sendChatMessage() {
            const input = document.getElementById("chat-input");
            const message = input.value;
            const results = await sendMessage(message);
            const log = document.getElementById("chat-log");
            log.innerHTML += `<div>User: ${message}</div>`;
            results.forEach(result => {
                log.innerHTML += `<div>Bot: ${result}</div>`;
            });
            input.value = "";
        }
    </script>';
}

add_shortcode('chatbot', 'chatbot_interface');
