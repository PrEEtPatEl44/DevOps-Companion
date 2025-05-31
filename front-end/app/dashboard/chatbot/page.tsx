"use client";
import React, { useState } from "react";
import DOMPurify from "dompurify"; // Import DOMPurify to sanitize bot responses.
import ReactMarkdown from 'react-markdown';
const ChatBotPage: React.FC = () => {
    const [messages, setMessages] = useState<{ user: string; bot: string }[]>([]);
    const [userInput, setUserInput] = useState("");
    const [loading, setLoading] = useState(false); // State to manage loading animation

    const handleSendMessage = async () => {
        if (userInput.trim() === "") return;

        const newMessage = { user: userInput, bot: "" };
        setMessages([...messages, newMessage]);
        setLoading(true); // Start loading animation

        try {
            const response = await fetch(
                "http://127.0.0.1:5000/api/chatbot/send_message",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ message: userInput }),
                }
            );

            const data = await response.json();

            // Extract the last assistant message
            const botMessage =
                data.messages
                    ?.reverse()
                    .find((msg: { role: string }) => msg.role === "assistant")?.content ||
                "";

            console.log("Bot response:", botMessage);

            setMessages([...messages, { user: userInput, bot: botMessage }]);
        } catch (error) {
            console.error("Error sending message:", error);
        }

        setUserInput("");
        setLoading(false); // Stop loading animation
    };

    // Function to sanitize HTML using DOMPurify
    const sanitizeHTML = (html: string) => {
        return DOMPurify.sanitize(html);
    };

    return (
        <div
            style={{
                display: "flex",
                flexDirection: "column",
                height: "80vh",
                width: "100%",
                padding: "20px",
                borderRadius: "8px",
                position: "relative",
            }}
        >
            <h1 className="text-black">ChatBot</h1>

            {/* Conditional large text */}
            {messages.length === 0 && (
                <div
                    style={{
                        color: "black",
                        position: "absolute",
                        top: "50%",
                        left: "50%",
                        transform: "translate(-50%, -50%)",
                        fontSize: "2rem",
                        fontWeight: "bold",
                        textAlign: "center",
                    }}
                    className="typewriter"
                >
                    What can I help with?
                </div>
            )}

            <div
                style={{
                    flex: 1,
                    maxHeight: "100%",
                    overflowY: "auto",
                }}
                className="text-black"
            >
                {messages.map((msg, index) => (
                    <div key={index} style={{ marginBottom: "10px" }}>
                        {msg.user && (
                            <div style={{ display: "flex", justifyContent: "flex-end" }}>
                                <div
                                    style={{
                                        backgroundColor: "#d1e7dd",
                                        padding: "10px",
                                        borderRadius: "8px",
                                        maxWidth: "60%",
                                    }}
                                >
                                    {msg.user}
                                </div>
                            </div>
                        )}
                        {msg.bot && (
                            <div
                                style={{
                                    display: "flex",
                                    justifyContent: "flex-start",
                                    marginTop: "10px",
                                }}
                            >
                                <div
                                    style={{
                                        backgroundColor: "#d1e7dd",
                                        padding: "10px",
                                        borderRadius: "8px",
                                        maxWidth: "60%",
                                    }}
                                >
                                    <span>
                                        <ReactMarkdown>{msg.bot}</ReactMarkdown>
                                    </span>
                                </div>
                            </div>
                        )}
                    </div>
                ))}
                {loading && (
                    <div style={{ textAlign: "center", marginTop: "10px" }}>
                        <div className="loader"></div>
                    </div>
                )}
            </div>

            <div
                style={{
                    display: "flex",
                    justifyContent: "space-evenly",
                    alignItems: "center",
                    marginTop: "auto",
                }}
            >
                <input
                    className="text-black bg-gray-200 rounded-xl"
                    type="text"
                    value={userInput}
                    onChange={(e) => setUserInput(e.target.value)}
                    style={{ padding: "10px", width: "80%", marginRight: "10px" }}
                    placeholder="Type a message..."
                />
                <button
                    className="px-2 py-2 rounded-sm text-white"
                    onClick={handleSendMessage}
                    style={{ backgroundColor: "#4CAF50" }}
                >
                    <span className="mx-2 rounded">Send</span>
                    <input type="submit" hidden />
                </button>
                <button
                    className="px-2 py-2 rounded-sm text-white"
                    onClick={async () => {
                        try {
                            await fetch("http://127.0.0.1:5000/api/chatbot/reset_chat", {
                                method: "POST",
                                headers: {
                                    "Content-Type": "application/json",
                                },
                            });
                            setMessages([]); // Clear the chat messages
                        } catch (error) {
                            console.error("Error resetting chat:", error);
                        }
                    }}
                    style={{ backgroundColor: "#9FA6B2" }}
                >
                    Reset Chat
                </button>
            </div>

            {/* Typewriter animation CSS */}
            <style>
                {`
                    .typewriter {
                        overflow: hidden; 
                        border-right: 2px solid black; 
                        white-space: nowrap; 
                        margin: 0 auto; 
                        letter-spacing: 0.15em;
                        text:black;
                    }
                    .loader {
                        border: 4px solid #f3f3f3; 
                        border-radius: 50%;
                        border-top: 4px solid #3498db; 
                        width: 20px;
                        height: 20px;
                        -webkit-animation: spin 2s linear infinite; 
                        animation: spin 2s linear infinite;
                    }
                    @-webkit-keyframes spin {
                        0% { -webkit-transform: rotate(0deg); }
                        100% { -webkit-transform: rotate(360deg); }
                    }
                    @keyframes spin {
                        0% { transform: rotate(0deg); }
                        100% { transform: rotate(360deg); }
                    }
                `}
            </style>
        </div>
    );
};

export default ChatBotPage;
