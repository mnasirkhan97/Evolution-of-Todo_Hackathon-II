"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { cn } from "@/lib/utils";
import { FaCheck, FaTrash, FaUndo } from "react-icons/fa";

// Define Task interface locally or import from shared types
interface Task {
    id: number;
    title: string;
    description?: string;
    status: string;
    is_recurring?: boolean;
    recurrence_interval?: string;
    due_date?: string;
}

interface TaskListProps {
    refreshTrigger: number;
}

export function TaskList({ refreshTrigger }: TaskListProps) {
    const [tasks, setTasks] = useState<Task[]>([]);
    const [loading, setLoading] = useState(true);

    const fetchTasks = async () => {
        try {
            const data = await api.getTasks();
            setTasks(data);
        } catch (error) {
            console.error("Failed to fetch tasks", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchTasks();
    }, [refreshTrigger]);

    const toggleComplete = async (task: Task) => {
        // Optimistic updatelikely needed for best UX, but simple reload for now
        try {
            if (task.status === "completed") {
                // Re-open not explicit in API yet, but let's assume updateTask handles it
                await api.updateTask(task.id, { status: "pending" });
            } else {
                await api.completeTask(task.id);
            }
            fetchTasks();
        } catch (e) { console.error(e) }
    }

    const handleDelete = async (id: number) => {
        if (!confirm("Are you sure?")) return;
        try {
            await api.deleteTask(id);
            fetchTasks();
        } catch (e) { console.error(e) }
    }

    if (loading) return <div className="text-center text-gray-400 py-10">Loading your tasks...</div>;

    if (tasks.length === 0) {
        return (
            <div className="text-center py-20 bg-white/5 rounded-2xl border border-white/10">
                <p className="text-gray-400 text-lg">No tasks yet. Add one to get started!</p>
            </div>
        );
    }

    return (
        <div className="space-y-4">
            {tasks.map((task) => (
                <div
                    key={task.id}
                    className={cn(
                        "group bg-white/5 backdrop-blur-sm border border-white/10 p-5 rounded-xl transition-all hover:bg-white/10 hover:border-white/20",
                        task.status === "completed" && "opacity-60 grayscale"
                    )}
                >
                    <div className="flex items-start justify-between gap-4">
                        <div className="flex-1">
                            <h3 className={cn(
                                "text-lg font-medium text-white transition-all",
                                task.status === "completed" && "line-through text-gray-400"
                            )}>
                                {task.title}
                            </h3>
                            {task.description && (
                                <p className="text-gray-400 mt-1 text-sm">{task.description}</p>
                            )}

                            <div className="flex gap-2 mt-2 text-xs">
                                {task.is_recurring && (
                                    <span className="px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 border border-blue-500/30">
                                        ↻ {task.recurrence_interval}
                                    </span>
                                )}
                                {task.due_date && (
                                    <span className="px-2 py-0.5 rounded bg-purple-500/20 text-purple-300 border border-purple-500/30">
                                        📅 {new Date(task.due_date).toLocaleDateString()}
                                    </span>
                                )}
                            </div>
                        </div>

                        <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                            <button
                                onClick={() => toggleComplete(task)}
                                className={cn(
                                    "p-2 rounded-lg transition-colors",
                                    task.status === "completed"
                                        ? "bg-yellow-500/20 text-yellow-500 hover:bg-yellow-500/30"
                                        : "bg-green-500/20 text-green-500 hover:bg-green-500/30"
                                )}
                                title={task.status === "completed" ? "Mark Pending" : "Mark Complete"}
                            >
                                {task.status === "completed" ? <FaUndo size={14} /> : <FaCheck size={14} />}
                            </button>
                            <button
                                onClick={() => handleDelete(task.id)}
                                className="p-2 rounded-lg bg-red-500/20 text-red-500 hover:bg-red-500/30 transition-colors"
                            >
                                <FaTrash size={14} />
                            </button>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
}
