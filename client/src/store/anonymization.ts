import { signal, computed } from '@preact/signals';
import type { AnonymizeResponse } from '../services/api';

export const originalText = signal('');
export const isLoading = signal(false);
export const error = signal<string | null>(null);
export const result = signal<AnonymizeResponse | null>(null);

// Helper computed signals
export const hasValidationIssues = computed(() =>
  (result.value?.validation.issues.length ?? 0) > 0
);

export const isSuccessful = computed(() =>
  result.value?.success ?? false
);
