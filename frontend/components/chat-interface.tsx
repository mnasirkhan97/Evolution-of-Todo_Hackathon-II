"use client";

import { useState, useRef, useEffect } from "react";
import { MessageCircle, X, Send, Loader2, Bot, User } from "lucide-react";
import { api } from "@/lib/api";
import { authClient } from "@/lib/auth-client";

interface Message {
    role: "user" | "assistant";
    content: string;
}

export function ChatInterface() {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [conversationId, setConversationId] = useState<number | undefined>(undefined);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    // Get current user session
    const { data: session } = authClient.useSession();

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isOpen]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || !session?.user?.id) return;

        const userMessage = input.trim();
        setInput("");
        setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
        setIsLoading(true);

        try {
            const result = await api.chat(session.user.id, userMessage, conversationId);

            if (result) {
                setConversationId(result.conversation_id);
                setMessages((prev) => [...prev, { role: "assistant", content: result.response }]);
            }
        } catch (error) {
            console.error("Chat error:", error);
            setMessages((prev) => [...prev, { role: "assistant", content: "Sorry, I encountered an error. Please try again." }]);
        } finally {
            setIsLoading(false);
        }
    };

    if (!session?.user) return null;

    return (
        <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end">
            {/* Chat Window */}
            {isOpen && (
                <div className="mb-4 w-80 sm:w-96 bg-[#1a1d24] border border-gray-800 rounded-2xl shadow-2xl flex flex-col overflow-hidden transition-all animate-in slide-in-from-bottom-5 duration-200">
                    {/* Header */}
                    <div className="p-4 bg-[#232730] border-b border-gray-800 flex justify-between items-center">
                        <div className="flex items-center gap-2">
                            <div className="p-1.5 bg-purple-500/20 rounded-lg">
                                <Bot className="w-5 h-5 text-purple-400" />
                            </div>
                            <h3 className="font-semibold text-white">Todo AI Assistant</h3>
                        </div>
                        <button
                            onClick={() => setIsOpen(false)}
                            className="text-gray-400 hover:text-white transition-colors"
                        >
                            <X className="w-5 h-5" />
                        </button>
                    </div>

                    {/* Messages */}
                    <div className="flex-1 h-96 overflow-y-auto p-4 space-y-4 bg-[#0f1115]">
                        {messages.length === 0 && (
                            <div className="text-center text-gray-500 mt-10 text-sm">
                                <p>👋 Hi {session.user.name}!</p>
                                <p>I can help you manage your tasks.</p>
                                <p className="mt-2 text-xs">Try "Add a task to buy milk"</p>
                            </div>
                        )}

                        {messages.map((msg, idx) => (
                            <div
                                key={idx}
                                className={`flex gap-3 ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                            >
                                {msg.role === "assistant" && (
                                    <div className="w-8 h-8 rounded-full bg-purple-500/20 flex items-center justify-center flex-shrink-0">
                                        <Bot className="w-4 h-4 text-purple-400" />
                                    </div>
                                )}

                                <div
                                    className={`max-w-[80%] p-3 rounded-2xl text-sm ${msg.role === "user"
                                            ? "bg-purple-600 text-white rounded-tr-sm"
                                            : "bg-[#2a2e37] text-gray-200 rounded-tl-sm"
                                        }`}
                                >
                                    {msg.content}
                                </div>

                                {msg.role === "user" && (
                                    <div className="w-8 h-8 rounded-full bg-blue-500/20 flex items-center justify-center flex-shrink-0">
                                        <User className="w-4 h-4 text-blue-400" />
                                    </div>
                                )}
                            </div>
                        ))}

                        {isLoading && (
                            <div className="flex gap-3 justify-start">
                                <div className="w-8 h-8 rounded-full bg-purple-500/20 flex items-center justify-center flex-shrink-0">
                                    <Bot className="w-4 h-4 text-purple-400" />
                                </div>
                                <div className="bg-[#2a2e37] p-3 rounded-2xl rounded-tl-sm flex items-center">
                                    <Loader2 className="w-4 h-4 text-gray-400 animate-spin" />
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    {/* Input */}
                    <form onSubmit={handleSubmit} className="p-3 bg-[#232730] border-t border-gray-800 flex gap-2">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Type a message..."
                            className="flex-1 bg-[#1a1d24] border border-gray-700 rounded-xl px-4 py-2 text-sm text-white focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition-all placeholder:text-gray-500"
                        />
                        <button
                            type="submit"
                            disabled={isLoading || !input.trim()}
                            className="p-2 bg-purple-600 hover:bg-purple-500 disabled:opacity-50 disabled:cursor-not-allowed rounded-xl text-white transition-colors"
                        >
                            <Send className="w-4 h-4" />
                        </button>
                    </form>
                </div>
            )}

            {/* Toggle Button */}
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="w-14 h-14 bg-purple-600 hover:bg-purple-500 text-white rounded-full shadow-lg hover:shadow-purple-500/20 transition-all flex items-center justify-center"
            >
                {isOpen ? <X className="w-6 h-6" /> : <MessageCircle className="w-6 h-6" />}
            </button>
        </div>
    );
}
