<script lang="ts">
	import type { Task, TaskUpdate } from '$lib/types';

	// $props() just means "this component gets handed some data from its parent"
	let {
		task,
		onUpdate,
		onDelete
	}: {
		task: Task;
		onUpdate: (id: number, updates: TaskUpdate) => void;
		onDelete: (id: number) => void;
	} = $props();

	// whether this card is currently showing the edit form or the normal view
	let editing = $state(false);
	let editTitle = $state('');
	let editDescription = $state('');
	let showError = $state(false);

	function toggleComplete() {
		onUpdate(task.id, { is_completed: !task.is_completed });
	}

	function startEdit() {
		// pull the current values in fresh every time edit opens,
		// so we're never showing stale data from way earlier
		editTitle = task.title;
		editDescription = task.description ?? '';
		showError = false;
		editing = true;
	}

	function saveEdit() {
		if (!editTitle.trim()) {
			// no title? show the error and don't save
			showError = true;
			return;
		}
		onUpdate(task.id, { title: editTitle, description: editDescription });
		editing = false;
	}
</script>

<div class="task-card" class:done={task.is_completed}>
	{#if editing}
		<label class="sr-only" for="task-{task.id}-title">Task title</label>
		<input
			id="task-{task.id}-title"
			class="pixel-input"
			class:pixel-input--error={showError}
			bind:value={editTitle}
			oninput={() => (showError = false)}
			aria-invalid={showError}
			aria-describedby={showError ? `task-${task.id}-title-error` : undefined}
		/>
		{#if showError}
			<p class="error-message" id="task-{task.id}-title-error" role="alert">
				<span aria-hidden="true">⚠</span> needs a title first, bestie
			</p>
		{/if}
		<label class="sr-only" for="task-{task.id}-description">Task description</label>
		<textarea id="task-{task.id}-description" class="pixel-input" bind:value={editDescription}
		></textarea>
		<div class="task-actions">
			<button class="pixel-btn pixel-btn--save" onclick={saveEdit}>
				<span aria-hidden="true">💾</span> save
			</button>
			<button class="pixel-btn" onclick={() => (editing = false)}>
				<span aria-hidden="true">✖</span> cancel
			</button>
		</div>
	{:else}
		<div class="task-row">
			<input
				type="checkbox"
				class="pixel-checkbox"
				checked={task.is_completed}
				onchange={toggleComplete}
				aria-label={task.is_completed
					? `Mark "${task.title}" as not done`
					: `Mark "${task.title}" as done`}
			/>
			<h2 class="task-title">{task.title}</h2>
		</div>
		{#if task.description}
			<p class="task-description">{task.description}</p>
		{/if}
		<div class="task-actions">
			<button class="pixel-btn" onclick={startEdit}>
				<span aria-hidden="true">✏️</span> edit
			</button>
			<button class="pixel-btn pixel-btn--danger" onclick={() => onDelete(task.id)}>
				<span aria-hidden="true">🗑️</span> delete
			</button>
		</div>
	{/if}
</div>

<style>
	.task-card {
		position: relative;
		background: var(--card-background);
		border: 4px solid #000;
		box-shadow: 6px 6px 0 #000;
		padding: 1rem 1rem 1rem 1.5rem;
		margin-bottom: 1rem;
		transition: background-color 0.2s ease;
	}

	/* little pixel tab in the top-left corner, like a sticker */
	.task-card::before {
		content: '';
		position: absolute;
		top: -4px;
		left: -4px;
		width: 14px;
		height: 14px;
		background: var(--color-yellow);
		border: 3px solid #000;
	}

	/* once a task is done, the whole card turns minty green instead of
	   just fading, and the corner tab becomes a checkmark badge */
	.task-card.done {
		background: var(--color-mint);
	}

	.task-card.done::before {
		content: '✓';
		background: var(--color-teal);
		display: flex;
		align-items: center;
		justify-content: center;
		font-family: var(--font-body);
		font-size: 0.8rem;
		color: #000;
	}

	.task-card.done .task-title {
		text-decoration: line-through;
	}

	.task-row {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.task-title {
		font-family: var(--font-heading);
		font-size: 0.9rem;
		color: var(--color-ink);
		margin: 0;
	}

	.task-description {
		font-family: var(--font-body);
		font-size: 1.1rem;
		margin: 0.5rem 0 0 1.75rem;
	}

	.task-actions {
		display: flex;
		gap: 0.5rem;
		margin-top: 0.75rem;
	}
</style>
