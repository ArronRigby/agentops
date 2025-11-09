# JavaScript/TypeScript Patterns

Progressive disclosure resource for modern JavaScript and TypeScript patterns.

## Modern ES6+ Patterns

```javascript
// Destructuring
const { name, email } = user;

// Spread operator
const newUser = { ...user, active: true };

// Arrow functions
const greet = (name) => `Hello, ${name}`;

// Async/await
const fetchData = async () => {
  const response = await fetch('/api/data');
  return response.json();
};
```

## React Patterns

```typescript
// Functional component with hooks
import { useState, useEffect } from 'react';

function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, [userId]);

  if (!user) return <div>Loading...</div>;
  return <div>{user.name}</div>;
}
```

## Testing with Jest/Vitest

```javascript
import { describe, it, expect } from 'vitest';

describe('User', () => {
  it('creates user with valid email', () => {
    const user = new User('alice@example.com');
    expect(user.email).toBe('alice@example.com');
  });
});
```

## Token Budget

This skill: ~400 tokens
