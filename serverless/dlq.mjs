/**
 * DLQ enqueue / replay contract helpers (synthetic unit-test surface).
 */
export class Dlq {
  constructor({ maxReceiveCount = 3 } = {}) {
    this.maxReceiveCount = maxReceiveCount;
    this.messages = [];
    this.alarms = [];
  }

  receiveAttempt(message) {
    const receiveCount = (message.receiveCount ?? 0) + 1;
    const next = { ...message, receiveCount };
    if (receiveCount > this.maxReceiveCount) {
      this.messages.push(next);
      this.alarms.push({ type: 'dlq_depth', at: new Date().toISOString(), message_id: message.id });
      return { action: 'dlq', message: next };
    }
    return { action: 'retry', message: next };
  }

  replay(messageId, { approved = false } = {}) {
    if (!approved) throw new Error('DLQ replay requires approval');
    const idx = this.messages.findIndex((m) => m.id === messageId);
    if (idx < 0) throw new Error('message not in DLQ');
    const [msg] = this.messages.splice(idx, 1);
    return { action: 'requeued', message: { ...msg, receiveCount: 0 } };
  }
}

export function isPoison(event, contract) {
  if (!event || typeof event !== 'object') return true;
  for (const field of contract.required_fields) {
    if (event[field] === undefined || event[field] === null) return true;
  }
  if (!contract.types.includes(event.type)) return true;
  return false;
}
