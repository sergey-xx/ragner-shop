import re


def validate_telegram_html(text: str) -> bool:
    """
    Проверяет, валиден ли HTML-текст для отправки в Telegram с parse_mode='HTML'.
    Возвращает True, если можно отправить, иначе False.
    """

    # Ограничения Telegram
    if len(text) > 4096:
        return False

    # Разрешённые теги
    allowed_tags = {
        'b', 'i', 'u', 's', 'strong', 'em', 'ins', 'del', 'span', 'a', 'code',
        'pre', 'tg-emoji', 'blockquote', 'blockquote expandable',
    }

    # Проверка корректности HTML-тегов (грубая, но быстрая)
    tag_stack = []
    tag_pattern = re.compile(r'</?([a-zA-Z0-9]+)(\s[^<>]*)?>')

    for match in tag_pattern.finditer(text):
        tag = match.group(1).lower()
        is_closing = match.group(0).startswith('</')

        if tag not in allowed_tags:
            return False

        if is_closing:
            if not tag_stack or tag_stack[-1] != tag:
                return False
            tag_stack.pop()
        else:
            # запрещаем вложенные <code> или <pre>
            if tag in ('code', 'pre') and tag in tag_stack:
                return False
            tag_stack.append(tag)

    if tag_stack:
        return False
    return True
