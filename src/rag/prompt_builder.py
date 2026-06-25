"""Build LLM prompts from prepared RAG contexts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .context_builder import RAGContext


@dataclass(frozen=True)
class RAGPrompt:
    """A prompt packet ready to be passed to a generator later."""

    question: str
    prompt_text: str
    context_text: str
    instruction: str
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "question": self.question,
            "prompt_text": self.prompt_text,
            "context_text": self.context_text,
            "instruction": self.instruction,
            "metadata": self.metadata,
        }


class PromptBuilder:
    """Create a deterministic prompt from a RAGContext."""

    def __init__(
        self,
        instruction: str,
        answer_language_policy: str = "Answer in the same language as the question.",
        require_sources: bool = True,
        language_policies: dict[str, dict[str, Any]] | None = None,
    ) -> None:
        instruction = instruction.strip()
        answer_language_policy = answer_language_policy.strip()
        if not instruction:
            raise ValueError("instruction must not be empty.")
        if not answer_language_policy:
            raise ValueError("answer_language_policy must not be empty.")

        self.instruction = instruction
        self.answer_language_policy = answer_language_policy
        self.require_sources = require_sources
        self.language_policies = language_policies or self._default_language_policies()

    def build(self, context: RAGContext, question: str | None = None) -> RAGPrompt:
        final_question = (question or context.question).strip()
        if not final_question:
            raise ValueError("question must not be empty.")
        if not context.context_text.strip():
            raise ValueError("context.context_text must not be empty.")

        language = self._resolve_language(context)
        language_policy = self.language_policies.get(language, {})
        answer_language = str(language_policy.get("answer_language", "same language as the question"))
        hard_rules = self._build_hard_rules(language=language, language_policy=language_policy)
        answer_format = self._build_answer_format(language=language, language_policy=language_policy)
        labels = self._labels(language)

        prompt_text = "\n\n".join(
            [
                self._assistant_identity(language),
                labels["rules"],
                self._format_rules(hard_rules),
                labels["format"],
                answer_format,
                labels["instruction"],
                self.instruction,
                self.answer_language_policy,
                labels["expected_language"].format(answer_language=answer_language),
                labels["question"],
                final_question,
                labels["context"],
                context.context_text,
                labels["answer"],
            ],
        )

        return RAGPrompt(
            question=final_question,
            prompt_text=prompt_text,
            context_text=context.context_text,
            instruction=self.instruction,
            metadata={
                "documents": len(context.documents),
                "context_truncated": context.truncated,
                "omitted_documents": context.omitted_documents,
                "require_sources": self.require_sources,
                "expected_language": language,
                "answer_language": answer_language,
                "answer_format": language_policy.get("answer_format"),
                "no_answer_format": language_policy.get("no_answer_format"),
            },
        )

    @staticmethod
    def _default_language_policies() -> dict[str, dict[str, Any]]:
        return {
            "kk": {
                "answer_language": "Kazakh",
                "hard_rules": [
                    "Жауапты тек қазақ тілінде бер.",
                    "Ағылшын тілінде жауап берме.",
                    "Орыс тілінде жауап берме.",
                    "Тек берілген контексті пайдалан.",
                    "Контексте жоқ ақпаратты ойдан шығарма.",
                    "Бір фразаны қайталама.",
                    "Міндетті форматтан тыс түсіндірме жазба.",
                    "\"Context Items Used\" деген блок жазба.",
                    "Контексте жоқ дереккөз нөмірлерін қолданба.",
                    "Егер контексте жауап жеткіліксіз болса, тек no-answer форматын қолдан.",
                ],
                "answer_format": (
                    "Жауап:\n"
                    "<1-3 қысқа сөйлем. Тек қазақ тілінде. Тек контекст бойынша.>\n\n"
                    "Дереккөздер: [1]"
                ),
                "no_answer_format": (
                    "Жауап:\n"
                    "Берілген контексте бұл сұраққа нақты жауап жоқ.\n\n"
                    "Дереккөздер: []"
                ),
            },
            "ru": {
                "answer_language": "Russian",
                "hard_rules": [
                    "Отвечай только на русском языке.",
                    "Не отвечай на английском языке.",
                    "Используй только предоставленный контекст.",
                    "Не выдумывай информацию, которой нет в контексте.",
                    "Не повторяй одну и ту же фразу.",
                    "Не пиши объяснения вне обязательного формата.",
                    "Не пиши блок \"Context Items Used\".",
                    "Не используй номера источников, которых нет в контексте.",
                    "Если в контексте нет ответа, используй только no-answer формат.",
                ],
                "answer_format": (
                    "Ответ:\n"
                    "<1-3 коротких предложения. Только на русском языке. Только по контексту.>\n\n"
                    "Источники: [1]"
                ),
                "no_answer_format": (
                    "Ответ:\n"
                    "В предоставленном контексте нет точного ответа на этот вопрос.\n\n"
                    "Источники: []"
                ),
            },
        }

    @staticmethod
    def _resolve_language(context: RAGContext) -> str:
        if not context.documents:
            return "unknown"

        language = context.documents[0].language.strip().lower()
        return language or "unknown"

    def _build_hard_rules(
        self,
        language: str,
        language_policy: dict[str, Any],
    ) -> list[str]:
        configured_rules = language_policy.get("hard_rules", [])
        hard_rules = [str(rule).strip() for rule in configured_rules if str(rule).strip()]

        if not hard_rules:
            hard_rules = [
                "Answer only using the retrieved context.",
                self.answer_language_policy,
                "Do not invent facts that are not present in the context.",
                "Do not repeat the same phrase.",
                "Do not write outside the required answer format.",
                "Do not write a 'Context Items Used' block.",
            ]

        has_citation_rule = any("[1]" in rule or "[2]" in rule for rule in hard_rules)
        if self.require_sources and not has_citation_rule:
            citation_rule = (
                "Жауапта тек қолданылған дереккөз нөмірлерін көрсет: [1], [2]."
                if language == "kk"
                else "Указывай только номера использованных источников: [1], [2]."
                if language == "ru"
                else "Cite only the retrieved context item numbers you used: [1], [2]."
            )
            return [*hard_rules, citation_rule]

        if self.require_sources or has_citation_rule:
            return hard_rules

        return [*hard_rules, "Do not add citations unless they are already present in the context."]

    @staticmethod
    def _build_answer_format(language: str, language_policy: dict[str, Any]) -> str:
        answer_format = language_policy.get("answer_format")
        no_answer_format = language_policy.get("no_answer_format")
        if answer_format and no_answer_format:
            if language == "kk":
                return (
                    "Жауап форматы міндетті түрде осындай болсын:\n\n"
                    f"{answer_format}\n\n"
                    "Егер жауап контексте жоқ болса, дәл осы форматты қолдан:\n\n"
                    f"{no_answer_format}"
                )
            if language == "ru":
                return (
                    "Формат ответа строго такой:\n\n"
                    f"{answer_format}\n\n"
                    "Если ответа нет в контексте, используй строго этот формат:\n\n"
                    f"{no_answer_format}"
                )
            return (
                "Use this exact answer format:\n\n"
                f"{answer_format}\n\n"
                "If the answer is not in the context, use this exact format:\n\n"
                f"{no_answer_format}"
            )

        return "Use a concise answer followed by source citations."

    @staticmethod
    def _assistant_identity(language: str) -> str:
        if language == "kk":
            return "Сен білім беру ассистентісің."
        if language == "ru":
            return "Ты образовательный ассистент."
        return "You are an educational assistant."

    @staticmethod
    def _labels(language: str) -> dict[str, str]:
        if language == "kk":
            return {
                "rules": "Қатаң ережелер:",
                "format": "Міндетті жауап форматы:",
                "instruction": "Жүйелік нұсқаулық:",
                "expected_language": "Күтілетін жауап тілі: {answer_language}.",
                "question": "Сұрақ:",
                "context": "Контекст:",
                "answer": "Жауап:",
            }
        if language == "ru":
            return {
                "rules": "Строгие правила:",
                "format": "Обязательный формат ответа:",
                "instruction": "Системная инструкция:",
                "expected_language": "Ожидаемый язык ответа: {answer_language}.",
                "question": "Вопрос:",
                "context": "Контекст:",
                "answer": "Ответ:",
            }
        return {
            "rules": "Strict rules:",
            "format": "Required answer format:",
            "instruction": "System instruction:",
            "expected_language": "Expected answer language: {answer_language}.",
            "question": "Question:",
            "context": "Context:",
            "answer": "Answer:",
        }

    @staticmethod
    def _format_rules(rules: list[str]) -> str:
        return "\n".join(f"{index}. {rule}" for index, rule in enumerate(rules, start=1))
