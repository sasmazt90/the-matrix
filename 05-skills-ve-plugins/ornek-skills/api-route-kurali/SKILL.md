---
name: api-route-convention
description: |
  TRIGGER when: creating or editing files under app/api/ in a Next.js project.
  Enforces: zod validation, error envelope, type-safe responses, rate limiting.
  SKIP: webhook routes that follow different conventions (e.g., Stripe webhooks).
---

# Next.js API Route Convention

When creating or editing API route files (`app/api/**/route.ts`), follow these conventions.

## Required structure

```typescript
import { z } from 'zod';
import { ok, err } from '@/lib/api/envelope';
import { rateLimit } from '@/lib/api/rate-limit';

const Body = z.object({
  // ... define input shape
});

export async function POST(req: Request) {
  // 1. Rate limit
  const rl = await rateLimit(req);
  if (!rl.ok) return err(429, 'Too many requests');

  // 2. Parse + validate
  const parsed = Body.safeParse(await req.json());
  if (!parsed.success) {
    return err(400, parsed.error.flatten());
  }

  // 3. Auth (if needed)
  // const { userId } = await auth(req);
  // if (!userId) return err(401, 'Unauthorized');

  // 4. Business logic
  const result = await businessLogic(parsed.data);

  // 5. Return envelope
  return ok({ data: result });
}
```

## Error envelope

Always use the shared envelope from `@/lib/api/envelope`:

```typescript
ok({ data: T })           // 200 with data
err(status, message|obj)  // 4xx/5xx with error
```

## Don't

- ❌ Don't return raw `NextResponse.json` — always use envelope
- ❌ Don't skip `zod` validation, even for "simple" routes
- ❌ Don't `try/catch` and silently swallow errors
- ❌ Don't expose internal error messages to client (use generic message + log internally)
- ❌ Don't read `req.body` directly — use `req.json()` and validate

## Required tests

Every API route must have:
- `__tests__/route.test.ts` covering 200, 400, 401, 429
- E2E test if it's user-facing

## Reference

See `examples/route-with-auth.ts` for a complete example with auth and rate limiting.
