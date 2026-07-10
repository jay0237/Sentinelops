try:
    from presidio_analyzer import AnalyzerEngine
except ImportError:
    AnalyzerEngine = None

analyzer = None

def detect_pii(text):

    if AnalyzerEngine is None:
        return []

    global analyzer

    if analyzer is None:
        analyzer = AnalyzerEngine()

    result = analyzer.analyze(
        text=text,
        language='en',
    )

    detected_pii = []

    for result in result:

        detected_pii.append({
            "entity": result.entity_type,
            "start": result.start,
            "end": result.end,
            "score": result.score
        })

    return detected_pii
    