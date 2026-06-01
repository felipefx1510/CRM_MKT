class LeadScoringService:
    ORIGEM_SCORES = {
        "Google Ads": 30,
        "Instagram": 20,
        "Facebook": 15,
        "Site": 25,
        "Indicado": 10,
        "Outro": 5,
    }
    INTERESSE_SCORES = {
        "Alta": 40,
        "Media": 20,
        "Baixa": 10,
    }

    @classmethod
    def calculate_score(cls, origem, interesse):
        score = cls.ORIGEM_SCORES.get(origem, 0)
        score += cls.INTERESSE_SCORES.get(interesse, 0)
        return min(score, 100)

    @staticmethod
    def classify(score):
        if score >= 80:
            return "Quente"
        if score >= 50:
            return "Morno"
        return "Frio"
