# Go Best Practices

Progressive disclosure resource for idiomatic Go patterns.

## Error Handling

```go
// Always check errors
func ReadFile(path string) ([]byte, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("reading file %s: %w", path, err)
    }
    return data, nil
}
```

## Struct Patterns

```go
// Constructor pattern
type User struct {
    Name  string
    Email string
}

func NewUser(name, email string) (*User, error) {
    if email == "" {
        return nil, errors.New("email required")
    }
    return &User{Name: name, Email: email}, nil
}
```

## Testing

```go
func TestCreateUser(t *testing.T) {
    user, err := NewUser("Alice", "alice@example.com")
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if user.Name != "Alice" {
        t.Errorf("got %s, want Alice", user.Name)
    }
}
```

## Concurrency

```go
// Goroutines and channels
func ProcessItems(items []Item) []Result {
    results := make(chan Result, len(items))

    for _, item := range items {
        go func(i Item) {
            results <- process(i)
        }(item)
    }

    // Collect results
    var out []Result
    for range items {
        out = append(out, <-results)
    }
    return out
}
```

## Token Budget

This skill: ~400 tokens
