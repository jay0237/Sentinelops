from presidio_analyzer import AnalyzerEngine

analyzer = AnalyzerEngine()

def detect_pii(text):

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

    