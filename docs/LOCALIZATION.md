# Localization Support

Decidely supports both English and Spanish for improved user experience.

## Supported Languages

- **English** (en, en_US)
- **Spanish** (es, es_ES, es_MX, etc.)

## Inline Command Usage

### English
```
/decidely authority couldn't approve budget
/decidely initiative team didn't fix bug
/decidely la need manager approval
/decidely ei ignored code review
```

### Spanish
```
/decidely autoridad no pude aprobar presupuesto
/decidely iniciativa equipo no corrigió error
/decidely fa necesito aprobación del gerente
/decidely ie ignoró revisión de código
```

## Keywords and Shortcuts

### English
- **Lacked Authority**: `authority`, `lacked`, `la`
- **Expected Initiative**: `initiative`, `expected`, `ei`

### Spanish
- **Faltó Autoridad**: `autoridad`, `faltó`, `fa`
- **Iniciativa Esperada**: `iniciativa`, `esperaba`, `ie`

## How It Works

1. The bot detects user's Slack locale from their profile
2. All messages (help, confirmations, forms) are shown in the user's language
3. Command keywords work in both languages simultaneously
4. Falls back to English if locale is not supported

## Adding New Languages

To add a new language:
1. Add translations to `get_localized_messages()` in `decidely_report.py`
2. Add keywords to the report type detection logic
3. Add tests for the new language keywords