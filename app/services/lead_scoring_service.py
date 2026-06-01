from app.models.lead import Lead


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

    CONVERTED_STATUS = "Fechado"
    LOST_STATUS = "Perdido"
    MIN_TRAIN_SAMPLES = 6
    CATEGORICAL_FIELDS = ("origem", "interesse", "segmento")
    FIELD_FALLBACKS = {
        "origem": "Outro",
        "interesse": "Media",
        "segmento": "Nao informado",
    }

    _model = None
    _encoders = None
    _trained_signature = None

    @classmethod
    def calculate_score(cls, origem, interesse, segmento=None):
        model, encoders = cls._get_model_bundle()
        if not model or not encoders:
            return cls._calculate_rule_based_score(origem, interesse)

        features = cls._encode_features(encoders, origem, interesse, segmento)
        prediction = float(model.predict([features])[0])
        return cls._prediction_to_score(prediction)

    @staticmethod
    def classify(score):
        if score >= 80:
            return "Quente"
        if score >= 50:
            return "Morno"
        return "Frio"

    @classmethod
    def _calculate_rule_based_score(cls, origem, interesse):
        score = cls.ORIGEM_SCORES.get(origem, 0)
        score += cls.INTERESSE_SCORES.get(interesse, 0)
        return min(score, 100)

    @classmethod
    def _get_model_bundle(cls):
        training_rows = cls._load_training_rows()
        if len(training_rows) < cls.MIN_TRAIN_SAMPLES:
            return None, None

        signature = cls._training_signature(training_rows)
        if cls._model and cls._encoders and cls._trained_signature == signature:
            return cls._model, cls._encoders

        features, targets, encoders = cls._build_training_matrix(training_rows)
        if not features or not targets or not encoders:
            return None, None

        if len(set(targets)) < 2:
            return None, None

        model = cls._train_model(features, targets)
        if not model:
            return None, None

        cls._model = model
        cls._encoders = encoders
        cls._trained_signature = signature
        return model, encoders

    @classmethod
    def _load_training_rows(cls):
        leads = (
            Lead.query.filter(
                Lead.status.in_([cls.CONVERTED_STATUS, cls.LOST_STATUS])
            ).all()
        )
        rows = []
        for lead in leads:
            rows.append(
                {
                    "origem": cls._normalize_value(
                        lead.origem,
                        cls.FIELD_FALLBACKS["origem"],
                    ),
                    "interesse": cls._normalize_value(
                        lead.interesse,
                        cls.FIELD_FALLBACKS["interesse"],
                    ),
                    "segmento": cls._normalize_value(
                        lead.segmento,
                        cls.FIELD_FALLBACKS["segmento"],
                    ),
                    "target": 1.0
                    if lead.status == cls.CONVERTED_STATUS
                    else 0.0,
                }
            )
        return rows

    @classmethod
    def _build_training_matrix(cls, rows):
        try:
            from sklearn.preprocessing import LabelEncoder
        except ImportError:
            return None, None, None

        encoders = {}
        for field in cls.CATEGORICAL_FIELDS:
            encoder = LabelEncoder()
            encoder.fit([row[field] for row in rows])
            encoders[field] = encoder

        features = []
        targets = []
        for row in rows:
            encoded = []
            for field in cls.CATEGORICAL_FIELDS:
                encoded.append(int(encoders[field].transform([row[field]])[0]))
            features.append(encoded)
            targets.append(row["target"])
        return features, targets, encoders

    @classmethod
    def _train_model(cls, features, targets):
        try:
            from sklearn.linear_model import LinearRegression
        except ImportError:
            return None

        model = LinearRegression()
        model.fit(features, targets)
        return model

    @classmethod
    def _encode_features(cls, encoders, origem, interesse, segmento):
        values = {
            "origem": cls._normalize_value(
                origem,
                cls.FIELD_FALLBACKS["origem"],
            ),
            "interesse": cls._normalize_value(
                interesse,
                cls.FIELD_FALLBACKS["interesse"],
            ),
            "segmento": cls._normalize_value(
                segmento,
                cls.FIELD_FALLBACKS["segmento"],
            ),
        }

        encoded = []
        for field in cls.CATEGORICAL_FIELDS:
            encoder = encoders[field]
            value = values[field]
            if value not in encoder.classes_:
                value = cls._fallback_label(encoder, cls.FIELD_FALLBACKS[field])
            encoded.append(int(encoder.transform([value])[0]))
        return encoded

    @staticmethod
    def _normalize_value(value, fallback):
        if value is None:
            return fallback
        text = str(value).strip()
        return text if text else fallback

    @staticmethod
    def _fallback_label(encoder, fallback):
        if fallback in encoder.classes_:
            return fallback
        return encoder.classes_[0]

    @staticmethod
    def _prediction_to_score(prediction):
        clipped = max(0.0, min(1.0, prediction))
        return int(round(clipped * 100))

    @staticmethod
    def _training_signature(rows):
        normalized = tuple(
            (
                row["origem"],
                row["interesse"],
                row["segmento"],
                row["target"],
            )
            for row in rows
        )
        return hash(normalized)
