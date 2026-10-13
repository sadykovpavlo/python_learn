def clean_up_url(url: str) -> str:
        symbols = (';', '<', '>', '.', ',','?')
        cleaned_url = [u for u in url if u not in symbols]
        if cleaned_url[0] == '/':
            cleaned_url.pop(0)
        if cleaned_url[-1] == '/':
            cleaned_url.pop(-1)
        return "".join(cleaned_url)

# print(clean_up_url("/some/some/"))

print(clean_up_url('./test/test/abra/>?'))