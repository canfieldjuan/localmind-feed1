def handler(event, context):
    import json
    # Simulated dynamic report logic
    query = event.get("queryStringParameters", {}).get("competitor", "Unknown")
    report = {
        "competitor": query,
        "strengths": ["Strong branding", "Good pricing"],
        "weaknesses": ["Poor SEO", "Outdated UX"]
    }
    return {
        "statusCode": 200,
        "body": json.dumps(report)
    }