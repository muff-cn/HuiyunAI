const chatBody = document.querySelector(".chat-body");
const messageInput = document.querySelector(".message-input");
const sendMessageButton = document.querySelector("#send-message");
const fileInput = document.querySelector("#file-input");
const chatbotToggler = document.querySelector("#chatbot-toggler");
const closeChatbot = document.querySelector("#close-chatbot");
// 跳转链接函数
const jumpToLink = (url) => {
    window.open(url, '_blank');
};

// API setup - 适配 FastAPI 后端
const API_URL = "/api/chat";  // FastAPI 后端的聊天接口路径

const userData = {
    message: null,
    file: {
        data: null,
        mime_type: null,
    },
};

const chatHistory = [];
const initialInputHeight = messageInput.scrollHeight;

// Create message element with dynamic classes and return it
const createMessageElement = (content, ...classes) => {
    const div = document.createElement("div");
    div.classList.add("message", ...classes);
    div.innerHTML = content;
    return div;
};

// Generate bot response using FastAPI backend
const generateBotResponse = async (incomingMessageDiv) => {
    const messageElement = incomingMessageDiv.querySelector(".message-text");
    const city = document.getElementById("city-name").textContent;
    
    // Add user message to chat history (optional, backend doesn't use this)
    chatHistory.push({
        role: "user",
        parts: [
            {text: userData.message},
            ...(userData.file.data ? [{inline_data: userData.file}] : []),
        ],
    });

    try {
        // 构建带查询参数的URL
        const url = new URL(API_URL, window.location.origin);
        url.searchParams.append('city', city);
        url.searchParams.append('prompt', userData.message);
        
        // 发起GET请求获取流式响应
        const response = await fetch(url);
        
        if (!response.ok) {
            // throw new Error('API请求失败');

        }
        
        // 获取ReadableStream并处理流式响应
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let result = '';
        
        // 逐块处理响应数据
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            // 解码新数据并更新UI
            const chunk = decoder.decode(value, { stream: true });
            result += chunk;
            messageElement.innerText = result;
            chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: "smooth" });
        }
        
        // Add bot response to chat history (optional)
        chatHistory.push({
            role: "model",
            parts: [{text: result}]
        });
        
    } catch (error) {
        console.error("API Error:", error);
        messageElement.innerText = "抱歉，我暂时无法响应您的请求。";
        messageElement.style.color = "#ff0000";
    } finally {
        incomingMessageDiv.classList.remove("thinking");
        chatBody.scrollTo({top: chatBody.scrollHeight, behavior: "smooth"});
        // 重置文件数据
        userData.file = { data: null, mime_type: null };
    }
};

// Handle outgoing user messages
const handleOutgoingMessage = (e) => {
    e.preventDefault();

    userData.message = messageInput.value.trim();
    if (!userData.message && !userData.file.data) return;

    messageInput.value = "";
    messageInput.dispatchEvent(new Event("input"));

    // Create and display user message
    const messageContent = `<div class="message-text">${userData.message}</div>
                          ${
        userData.file.data
            ? `<img src="data:${userData.file.mime_type};base64,${userData.file.data}" class="attachment"  alt=""/>`
            : ""
    }`;

    const outgoingMessageDiv = createMessageElement(messageContent, "user-message");
    chatBody.appendChild(outgoingMessageDiv);
    chatBody.scrollTo({top: chatBody.scrollHeight, behavior: "smooth"});

    // Show bot thinking indicator
    setTimeout(() => {
        const messageContent = `<svg 
            class="bot-avatar"
            xmlns="http://www.w3.org/2000/svg"
            width="50"
            height="50"
            viewBox="0 0 1024 1024"
          >
          <path
              d="M738.3 287.6H285.7c-59 0-106.8 47.8-106.8 106.8v303.1c0 59 47.8 106.8 106.8 106.8h81.5v111.1c0 .7.8 1.1 1.4.7l166.9-110.6 41.8-.8h117.4l43.6-.4c59 0 106.8-47.8 106.8-106.8V394.5c0-59-47.8-106.9-106.8-106.9zM351.7 448.2c0-29.5 23.9-53.5 53.5-53.5s53.5 23.9 53.5 53.5-23.9 53.5-53.5 53.5-53.5-23.9-53.5-53.5zm157.9 267.1c-67.8 0-123.8-47.5-132.3-109h264.6c-8.6 61.5-64.5 109-132.3 109zm110-213.7c-29.5 0-53.5-23.9-53.5-53.5s23.9-53.5 53.5-53.5 53.5 23.9 53.5 53.5-23.9 53.5-53.5 53.5zM867.2 644.5V453.1h26.5c19.4 0 35.1 15.7 35.1 35.1v121.1c0 19.4-15.7 35.1-35.1 35.1h-26.5zM95.2 609.4V488.2c0-19.4 15.7-35.1 35.1-35.1h26.5v191.3h-26.5c-19.4 0-35.1-15.7-35.1-35.1zM561.5 149.6c0 23.4-15.6 43.3-36.9 49.7v44.9h-30v-44.9c-21.4-6.5-36.9-26.3-36.9-49.7 0-28.6 23.3-51.9 51.9-51.9s51.9 23.3 51.9 51.9z"
            ></path>
          </svg>
          <div class="message-text">
            <div class="thinking-indicator">
              <div class="dot"></div>
              <div class="dot"></div>
              <div class="dot"></div>
            </div>
          </div>`;

        const incomingMessageDiv = createMessageElement(messageContent, "bot-message", "thinking");
        chatBody.appendChild(incomingMessageDiv);
        chatBody.scrollTo({top: chatBody.scrollHeight, behavior: "smooth"});
        generateBotResponse(incomingMessageDiv).then();
    }, 600);
};

// Handle Enter key press for sending messages
messageInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 768) {
        handleOutgoingMessage(e);
    }
});

// Auto resize message input
messageInput.addEventListener("input", (e) => {
    if (e){ }
    // messageInput.style.height = `${initialInputHeight}px`;
    // messageInput.style.height = `${messageInput.scrollHeight}px`;
    // // 修正选择器错误：chat-form → .chat-form
    // document.querySelector(".chat-form").style.borderRadius = messageInput.scrollHeight > initialInputHeight ? "15px" : "32px";
});

// Handle file input change
fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
        const base64String = e.target.result.split(",")[1];

        // Store file data in userData
        userData.file = {
            data: base64String,
            mime_type: file.type,
        };

        fileInput.value = "";
    };

    reader.readAsDataURL(file);
});

// Emoji picker setup
const picker = new EmojiMart.Picker({
    theme: "light",
    skinTonePosition: "none",
    preview: "none",
    onEmojiSelect: (emoji) => {
        const {selectionStart: start, selectionEnd: end} = messageInput;
        messageInput.setRangeText(emoji.native, start, end, "end");
        messageInput.focus();
    },
    onClickOutside: (e) => {
        if (e.target.id === "emoji-picker") {
            document.body.classList.toggle("show-emoji-picker");
        } else {
            document.body.classList.remove("show-emoji-picker");
        }
    }
});

document.querySelector(".chat-form").appendChild(picker);

// Event listeners
sendMessageButton.addEventListener("click", (e) => handleOutgoingMessage(e));
document.querySelector("#file-upload").addEventListener("click", () => fileInput.click());

chatbotToggler.addEventListener("click", () => {
    document.body.classList.toggle("show-chatbot");
});

closeChatbot.addEventListener("click", () => {
    document.body.classList.remove("show-chatbot");
});

// 页面加载完成后自动打开聊天机器人
// static/scripts/script.js 中新增
document.addEventListener("DOMContentLoaded", () => {
    // 原有逻辑...
    document.body.classList.add('show-chatbot');

    // AI天气咨询按钮
    const weatherAIButton = document.getElementById("ai-consult-weather");
    weatherAIButton.addEventListener("click", () => {
        const city = document.getElementById("city-name").textContent;
        messageInput.value = `请根据${city}的气象条件（温度、湿度、风速、天气），并提供${city}天气解读与出行建议`;
        // 自动触发发送
        sendMessageButton.click();
    });

    // AI天文咨询按钮
    const astronomyAIButton = document.getElementById("ai-consult-astronomy");
    astronomyAIButton.addEventListener("click", () => {
        const city = document.getElementById("city-name").textContent;
        messageInput.value = `请提供${city}的天文观星建议（含月相、光污染、视宁度）`;
        sendMessageButton.click();
    });
});