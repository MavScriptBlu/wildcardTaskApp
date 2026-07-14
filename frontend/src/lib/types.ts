/** @format */

// This describes exactly what a "task" looks like, so TypeScript can catch
// typos and mistakes for me before we even run the app.
export interface Task {
	id: number;
	title: string;
	description: string | null;
	is_completed: boolean;
	created_at: string;
	updated_at: string;
}

// When we send to the backend when creating a new task
export interface NewTask {
	title: string;
	description?: string;
}

// What we send to the backend when updating a task (everything is optional
// since you might just be checking a box)
export interface TaskUpdate {
	title?: string;
	description?: string;
	is_completed?: boolean;
}
