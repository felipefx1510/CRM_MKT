class FollowupAgent:
    def __init__(self, ollama_service):
        self.ollama_service = ollama_service

    def run(self, lead, variation=None, extra_instruction=None):
        prompt = self._build_prompt(lead, variation, extra_instruction)
        return self.ollama_service.generate_followup(prompt)

    def _build_prompt(self, lead, variation, extra_instruction):
        variation_text = (
            f"Gerar variacao {variation}." if variation else ""
        )
        extra_text = (
            f"Instrucao extra: {extra_instruction}\n" if extra_instruction else ""
        )
        return (
            "Voce e um especialista em prospeccao de marketing digital. "
            "Crie uma mensagem de follow-up curta, educada e personalizada. "
            "Nao invente dados, use apenas o que foi informado.\n\n"
            f"{variation_text}\n"
            f"{extra_text}"
            f"Nome: {lead.nome}\n"
            f"Empresa: {lead.empresa or 'Nao informado'}\n"
            f"Origem: {lead.origem}\n"
            f"Segmento: {lead.segmento or 'Nao informado'}\n"
            f"Interesse (urgencia): {lead.interesse}\n"
            f"Mensagem original: {lead.mensagem or 'Nao informado'}\n\n"
            "Responda em portugues do Brasil e apenas com a mensagem pronta para envio."
        )
