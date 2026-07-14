
<script lang="ts">
	import type { NewTask } from '$lib/types';

	// $props() just means "this component gets handed some data from its parent"
	let { onCreate }: { onCreate: (task: NewTask) => void } = $props();

	// $state() means "this value can change, and Svelte will re-render when it does"
	let title = $state('');
	let description = $state('');
	let showError = $state(false);

	function handleSubmit(e: SubmitEvent) {
		e.preventDefault();
		if (!title.trim()) {
			// no title? show the error and bail out before calling the API
			showError = true;
			return;
		}
		onCreate({ title, description: description || undefined });
		title = '';
		description = '';
		showError = false;
	}
</script>

<form class="task-form" onsubmit={handleSubmit}>
	<label class="sr-only" for="new-task-title">Task title</label>
	<input
		id="new-task-title"
		class="pixel-input"
		class:pixel-input--error={showError}
		placeholder="what needs doing? ✨"
		bind:value={title}
		oninput={() => (showError = false)}
		aria-invalid={showError}
		aria-describedby={showError ? 'new-task-title-error' : undefined}
	/>
	{#if showError}
		<p class="error-message" id="new-task-title-error" role="alert">
			<span aria-hidden="true">⚠</span> needs a title first, bestie
		</p>
	{/if}
	<label class="sr-only" for="new-task-description">Task description (optional)</label>
	<textarea
		id="new-task-description"
		class="pixel-input"
		placeholder="any extra notes? (optional)"
		bind:value={description}
	></textarea>
	<button class="pixel-btn pixel-btn--save" type="submit">
		<span aria-hidden="true">➕</span> add task
	</button>
</form>

<style>
	.task-form {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
		margin-bottom: 2rem;
	}
</style>
