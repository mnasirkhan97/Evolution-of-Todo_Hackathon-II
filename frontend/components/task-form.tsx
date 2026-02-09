"use client";

import { useState } from "react";
import { api } from "@/lib/api";
import { cn } from "@/lib/utils";

interface TaskFormProps {
    onTaskAdded: () => void;
}

export function TaskForm({ onTaskAdded }: TaskFormProps) {
    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [isRecurring, setIsRecurring] = useState(false);
    const [recurrenceInterval, setRecurrenceInterval] = useState("daily");
    const [dueDate, setDueDate] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!title.trim()) return;

        setLoading(true);
        try {
            await api.createTask({
                title,
                description,
                is_recurring: isRecurring,
                recurrence_interval: isRecurring ? recurrenceInterval : undefined,
                due_date: dueDate || undefined
            });
            setTitle("");
            setDescription("");
            setIsRecurring(false);
            setDueDate("");
            onTaskAdded();
        } catch (error) {
            console.error("Failed to create task", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="bg-white/5 backdrop-blur-md border border-white/10 p-6 rounded-2xl shadow-xl transition-all hover:shadow-2xl hover:border-white/20">
            <h2 className="text-xl font-bold mb-4 text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">
                New Task
            </h2>
            <div className="space-y-4">
                <input
                    type="text"
                    placeholder="What needs to be done?"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    className="w-full bg-black/20 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all"
                    required
                />
                <textarea
                    placeholder="Add details..."
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    className="w-full bg-black/20 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500/50 transition-all resize-none h-24"
                />

                {/* Advanced Fields */}
                <div className="flex flex-wrap gap-4">
                    <div className="flex-1 min-w-[150px]">
                        <label className="block text-xs text-gray-400 mb-1 ml-1">Due Date</label>
                        <input
                            type="datetime-local"
                            value={dueDate}
                            onChange={(e) => setDueDate(e.target.value)}
                            className="w-full bg-black/20 border border-white/10 rounded-lg px-3 py-2 text-white text-sm"
                        />
                    </div>
                </div>

                <div className="flex items-center gap-3 bg-black/20 p-3 rounded-lg border border-white/5">
                    <input
                        type="checkbox"
                        id="recurring"
                        checked={isRecurring}
                        onChange={(e) => setIsRecurring(e.target.checked)}
                        className="w-4 h-4 rounded border-gray-600 bg-gray-700 text-blue-600 focus:ring-blue-500"
                    />
                    <label htmlFor="recurring" className="text-sm text-gray-300">Recurring?</label>

                    {isRecurring && (
                        <select
                            value={recurrenceInterval}
                            onChange={(e) => setRecurrenceInterval(e.target.value)}
                            className="bg-black/30 border border-white/10 rounded px-2 py-1 text-sm text-white focus:outline-none"
                        >
                            <option value="daily">Daily</option>
                            <option value="weekly">Weekly</option>
                            <option value="monthly">Monthly</option>
                        </select>
                    )}
                </div>

                <button
                    type="submit"
                    disabled={loading}
                    className={cn(
                        "w-full py-3 px-6 rounded-lg font-semibold text-white shadow-lg transition-all transform hover:-translate-y-0.5 active:translate-y-0",
                        "bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500",
                        loading && "opacity-50 cursor-not-allowed"
                    )}
                >
                    {loading ? "Adding..." : "Add Task"}
                </button>
            </div>
        </form>
    );
}
