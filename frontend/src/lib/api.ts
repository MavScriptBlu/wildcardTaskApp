/** @format */

import type { Task, NewTask, TaskUpdate } from "./types";

// this gets baked in when the frontend is built, (see the frontend Containerfile, later)
const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export async function getTasks(): Promise<Task[]> {
	const res = await fetch(`${API_URL}/tasks`);
	if (!res.ok) throw new Error(`Could not load tasks: ${res.status}`);

	return res.json();
}

export async function createTask(task: NewTask): Promise<Task> {
	const res = await fetch(`${API_URL}/tasks`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify(task),
	});
	if (!res.ok) throw new Error(`Could not create task: ${res.status}`);

	return res.json();
}

export async function updateTask(
	id: number,
	updates: TaskUpdate,
): Promise<Task> {
	const res = await fetch(`${API_URL}/tasks/${id}`, {
		method: "PUT",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify(updates),
	});
	if (!res.ok) throw new Error(`Could not update task: ${res.status}`);

	return res.json();
}

export async function deleteTask(id: number): Promise<void> {
	const res = await fetch(`${API_URL}/tasks/${id}`, {
		method: "DELETE",
	});
	if (!res.ok) throw new Error(`Could not delete task: ${res.status}`);
}
