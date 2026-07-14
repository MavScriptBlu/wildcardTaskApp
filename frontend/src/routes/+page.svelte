<script lang="ts">
	import { onMount } from 'svelte';
	import { flip } from 'svelte/animate';
	import type { Task, NewTask, TaskUpdate } from '$lib/types';
	import { getTasks, createTask, updateTask, deleteTask } from '$lib/api';
	import TaskForm from '$lib/components/TaskForm.svelte';
	import TaskCard from '$lib/components/TaskCard.svelte';

	let tasks = $state<Task[]>([]);
	let loading = $state(true);
	let errorMessage = $state('');

	// incomplete tasks stay on top, completed ones sink to the bottom
	let sortedTasks = $derived(
		[...tasks].sort((a, b) => Number(a.is_completed) - Number(b.is_completed))
	);

	async function loadTasks() {
		try {
			loading = true;
			tasks = await getTasks();
			errorMessage = '';
		} catch {
			errorMessage = 'could not load tasks 💔 is the backend running?';
		} finally {
			loading = false;
		}
	}

	async function handleCreate(newTask: NewTask) {
		const task = await createTask(newTask);
		tasks = [task, ...tasks];
	}

	async function handleUpdate(id: number, updates: TaskUpdate) {
		const updated = await updateTask(id, updates);
		tasks = tasks.map((t) => (t.id === id ? updated : t));
	}

	async function handleDelete(id: number) {
		await deleteTask(id);
		tasks = tasks.filter((t) => t.id !== id);
	}

	onMount(loadTasks);
</script>

<main class="page">
	<div class="page-banner">
		<h1 class="page-title">💖 task app 💖</h1>
		<p class="page-subtitle">get 'er done, son!</p>
	</div>

	<TaskForm onCreate={handleCreate} />

	<div role="status" aria-live="polite">
		{#if loading}
			<p class="status-message">loading tasks...</p>
		{:else if errorMessage}
			<p class="status-message status-message--error">{errorMessage}</p>
		{:else if tasks.length === 0}
			<p class="status-message">no tasks yet! add one above ⬆️</p>
		{/if}
	</div>

	{#if !loading && !errorMessage && tasks.length > 0}
		{#each sortedTasks as task (task.id)}
			<div animate:flip={{ duration: 250 }}>
				<TaskCard {task} onUpdate={handleUpdate} onDelete={handleDelete} />
			</div>
		{/each}
	{/if}
</main>

<style>
	.page {
		max-width: 640px;
		margin: 0 auto;
		padding: 2rem 1rem 4rem;
	}

	/* retro arcade-marquee style banner so the title doesn't get lost
	   in the busy dotted background */
	.page-banner {
		position: relative;
		background: linear-gradient(135deg, var(--color-cyan), var(--color-hotpink));
		border: 4px solid #000;
		box-shadow: 6px 6px 0 #000;
		padding: 1.5rem 1rem;
		margin-bottom: 2rem;
		text-align: center;
	}

	/* same little pixel tabs as the task cards, for consistency */
	.page-banner::before,
	.page-banner::after {
		content: '';
		position: absolute;
		width: 14px;
		height: 14px;
		background: var(--color-yellow);
		border: 3px solid #000;
	}

	.page-banner::before {
		top: -4px;
		left: -4px;
	}

	.page-banner::after {
		bottom: -4px;
		right: -4px;
	}

	.page-title {
		font-family: var(--font-heading);
		font-size: 1.75rem;
		/* ink instead of white — white text only hit ~1.5-2.8:1 against
		   the cyan/hotpink banner gradient, well under WCAG AA's 4.5:1 */
		color: var(--color-ink);
		text-shadow: 2px 2px 0 rgba(255, 255, 255, 0.6);
		margin: 0;
	}

	.page-subtitle {
		font-family: var(--font-body);
		font-size: 1.3rem;
		color: var(--color-ink);
		text-shadow: 1px 1px 0 rgba(255, 255, 255, 0.6);
		margin: 0.5rem 0 0;
	}

	.status-message {
		font-family: var(--font-body);
		text-align: center;
		font-size: 1.2rem;
	}

	.status-message--error {
		color: var(--color-hotpink-dark);
	}
</style>
