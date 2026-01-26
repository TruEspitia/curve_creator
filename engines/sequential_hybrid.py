```python
# ...existing code...
if isinstance(result, dict):
    value = result.get('key_name', default_value)
else:
    # result es un escalar (float, int, etc.)
    value = result
# ...existing code...
```