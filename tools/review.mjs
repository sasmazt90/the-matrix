import { createHash, randomUUID } from 'node:crypto';
import { mkdir, readFile, writeFile, rename, rm } from 'node:fs/promises';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

function requireValue(condition, message) {
  if (!condition) throw new Error(message);
}

export function review(input) {
  requireValue(input?.source === 'synthetic' && input.currency === 'EUR',
    'This local exercise accepts synthetic EUR data.');
  for (const field of ['campaign', 'market', 'period']) {
    requireValue(typeof input[field] === 'string' && input[field].trim(), 'Missing ' + field);
  }
  requireValue(Array.isArray(input.lines) && input.lines.length, 'Expected media lines.');
  const seen = new Set();
  let planned = 0;
  let spent = 0;
  const lines = input.lines.map(({ id, planned: plan, spent: actual }) => {
    requireValue(typeof id === 'string' && id.trim() && !seen.has(id), 'Missing or duplicate line ID.');
    seen.add(id);
    // This exercise uses whole euros. Reject other precision instead of silently rounding money.
    requireValue([plan, actual].every(n => Number.isSafeInteger(n) && n >= 0), 'Invalid media amount.');
    planned += plan;
    spent += actual;
    requireValue(Number.isSafeInteger(planned) && Number.isSafeInteger(spent), 'Totals exceed safe range.');
    return { id, planned: plan, spent: actual, gap: actual - plan };
  });
  requireValue(planned > 0, 'A positive total plan is required.');
  const { line, changePercent } = input.request ?? {};
  requireValue(seen.has(line) && Number.isFinite(changePercent) && changePercent >= -100 && changePercent !== 0,
    'Invalid proposed change.');
  const finance = input.finance;
  if (finance != null) {
    requireValue(finance.scope === 'campaign' && Number.isSafeInteger(finance.contributionBeforeMedia)
      && Number.isSafeInteger(finance.contributionBeforeMedia - spent), 'Invalid campaign finance evidence.');
  }
  const evidence = input.evidence;
  if (evidence != null) {
    requireValue(typeof evidence.scope === 'string' && evidence.scope.trim() &&
      typeof evidence.comparison === 'string' && evidence.comparison.trim(), 'Invalid experiment description.');
  }
  return {
    source: input.source, market: input.market, campaign: input.campaign, period: input.period,
    currency: input.currency, lines, planned, spent, gap: spent - planned,
    pacingVariancePct: Math.round((spent - planned) / planned * 1000) / 10,
    financeScope: finance?.scope ?? null, contributionAfterMedia: finance ? finance.contributionBeforeMedia - spent : null,
    experiment: evidence ?? null, request: { line, changePercent },
    decision: 'NEEDS_EVIDENCE', reason: 'This input contains no estimated profit effect for the proposed budget step.',
    approval: 'pending', mode: 'local-draft', modelCalls: 0
  };
}

async function publish(path, content) {
  const tmp = path + '.' + randomUUID() + '.tmp';
  try {
    await writeFile(tmp, content, { flag: 'wx' });
    await rename(tmp, path);
  } finally {
    await rm(tmp, { force: true });
  }
}

export async function run(input, workspace = '.matrix') {
  const result = review(input);
  const record = JSON.stringify(result, null, 2) + '\n';
  const id = createHash('sha256').update(record).digest('hex');
  const journal = join(workspace, 'journal');
  const outputs = join(workspace, 'outputs');
  await Promise.all([mkdir(journal, { recursive: true }), mkdir(outputs, { recursive: true })]);
  const evidencePath = join(journal, id + '.json');
  const draftPath = join(outputs, id + '.md');
  const draft = [
    '# Budget test proposal | Synthetic exercise', '',
    'Source record: ' + id, 'Campaign: ' + result.campaign + ' / ' + result.period,
    'Flight plan variance: ' + result.gap + ' EUR (' + result.pacingVariancePct + '%).',
    'Campaign contribution after media: ' + (result.contributionAfterMedia == null ? 'unavailable' : result.contributionAfterMedia + ' EUR') + '.',
    'Available comparison: ' + (result.experiment?.comparison ?? 'unavailable') + '.',
    'Proposed comparison: current spend versus ' + result.request.changePercent + '% on ' + result.request.line + '.',
    'Primary outcome: incremental completed-rental contribution after media.',
    'Next: Measurement specifies assignment, duration and uncertainty; Finance checks cost coverage.',
    'Owner: channel owner. Approval: pending. Execution: local draft.', ''
  ].join('\n');
  await publish(evidencePath, record);
  await publish(draftPath, draft);
  return { result, evidencePath, draftPath };
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  try {
    const path = process.argv[2];
    requireValue(path, 'Usage: node tools/review.mjs examples/munich/input.json');
    const report = await run(JSON.parse(await readFile(path, 'utf8')));
    console.log(JSON.stringify(report, null, 2));
  } catch (error) {
    console.error(error.message);
    process.exitCode = 1;
  }
}
