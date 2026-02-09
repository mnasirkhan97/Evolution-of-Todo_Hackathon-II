"use client";

import { useState } from "react";
import { TaskForm } from "@/components/task-form";
import { TaskList } from "@/components/task-list";
import { ChatInterface } from "@/components/chat-interface";

export default function Home() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleTaskAdded = () => {
    setRefreshTrigger((prev) => prev + 1);
  };

  return (
    <main className="min-h-screen bg-[#0f1115] text-white selection:bg-purple-500/30">
      <div className="absolute inset-0 bg-[url('/grid.png')] bg-center [mask-image:linear-gradient(180deg,white,rgba(255,255,255,0))]" />

      <div className="relative max-w-5xl mx-auto px-4 py-12 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h1 className="text-5xl font-extrabold tracking-tight mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 animate-gradient-x">
            Evolution of Todo
          </h1>
          <p className="text-xl text-gray-400">
            Mastering the Architecture of Intelligence
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          <div className="lg:col-span-4 lg:sticky lg:top-8">
            <TaskForm onTaskAdded={handleTaskAdded} />
          </div>

          <div className="lg:col-span-8">
            <TaskList refreshTrigger={refreshTrigger} />
          </div>
        </div>
      </div>

      <ChatInterface />
    </main>
  );
}
