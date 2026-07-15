// Phase-authorization gate.
//
// Authorization is monotonic and only advances through an explicit human
// decision that raises `authorized_through_phase`. A task in phase N may
// become `ready` only when N <= authorized_through_phase. The immediately
// next phase must be demonstrably rejected (see tests/harness).

export function isPhaseAuthorized(phase, authorizedThroughPhase) {
  return Number.isInteger(phase) && phase <= authorizedThroughPhase;
}

/** Throw if a task's phase is not authorized for activation. */
export function assertPhaseAuthorized(task, authorizedThroughPhase) {
  if (!isPhaseAuthorized(task.phase, authorizedThroughPhase)) {
    throw new Error(
      `phase ${task.phase} not authorized (authorized_through_phase=${authorizedThroughPhase}); task ${task.id} rejected`,
    );
  }
  return true;
}

/**
 * Dependencies must all be `verified` or `done` before a task is `ready`.
 */
export function dependenciesSatisfied(task, tasksById) {
  return (task.depends_on || []).every((dep) => {
    const d = tasksById.get(dep);
    return d && (d.state === 'verified' || d.state === 'done');
  });
}
