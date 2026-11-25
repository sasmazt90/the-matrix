import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, readFile, readdir, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { review, run } from '../tools/review.mjs';
const fixture = JSON.parse(await readFile(new URL('../examples/munich/input.json', import.meta.url)));
test('separates media delivery, campaign margin and causal evidence', () => {
  const r = review(fixture);
  assert.deepEqual(r.lines.map(x => x.gap), [240, -40]);
  assert.deepEqual([r.planned, r.spent, r.pacingVariancePct, r.contributionAfterMedia], [2000, 2200, 10, 800]);
  assert.equal(r.decision, 'NEEDS_EVIDENCE');
  assert.equal(r.modelCalls, 0);
});
test('unknown finance and experiment stay unknown', () => {
  const r = review({ ...fixture, finance: null, evidence: null });
  assert.equal(r.contributionAfterMedia, null);
  assert.equal(r.experiment, null);
  assert.equal(r.approval, 'pending');
});
test('rejects invalid money, duplicate lines, and out-of-scope changes', () => {
  for (const value of [null, '800', -1, 0.5]) {
    const x = structuredClone(fixture); x.lines[0].spent = value;
    assert.throws(() => review(x));
  }
  assert.throws(() => review({ ...fixture, lines: [fixture.lines[0], fixture.lines[0]] }));
  assert.throws(() => review({ ...fixture, request: { line: 'unknown', changePercent: -10 } }));
});
test('concurrent replay converges; a finance correction creates a new revision', async t => {
  const dir = await mkdtemp(join(tmpdir(), 'matrix-'));
  t.after(() => rm(dir, { recursive: true, force: true }));
  const [a,b] = await Promise.all([run(fixture,dir), run(fixture,dir)]);
  assert.equal(a.evidencePath,b.evidencePath);
  assert.equal((await readdir(join(dir, 'journal'))).length, 1);
  assert.match(await readFile(a.draftPath,'utf8'), /Approval: pending/);
  const updated = structuredClone(fixture); updated.finance.contributionBeforeMedia -= 30;
  const c = await run(updated,dir);
  assert.equal(c.result.contributionAfterMedia,770);
  assert.notEqual(c.evidencePath,a.evidencePath);
  assert.equal(JSON.parse(await readFile(a.evidencePath)).contributionAfterMedia,800);
});
