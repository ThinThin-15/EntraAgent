// Copyright (c) Microsoft. All rights reserved.
// Licensed under the MIT license. See LICENSE.md file in the project root for full license information.

import ChatUI from './ChatUI.js';
import ChatClient from './ChatClient.js';

const chatUI = new ChatUI();
const chatClient = new ChatClient(chatUI);

function initChat() {
 
    const form = document.getElementById("chat-form");
    const messageInput = document.getElementById("message");
    const targetContainer = document.getElementById("messages");

    form.addEventListener("submit", async function(e) {
        e.preventDefault();
        
        await chatClient.sendMessage("/chat", messageInput.value.trim());
        messageInput.value = "";
    });

    window.onbeforeunload = function() {
        chatClient.closeEventSource();
    };
}

document.addEventListener("DOMContentLoaded", initChat);

window.chatUI = chatUI;
window.chatClient = chatClient;

await chatUI.loadChatHistory();