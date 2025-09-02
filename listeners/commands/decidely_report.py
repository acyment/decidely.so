from slack_bolt import Ack, Respond
from slack_sdk import WebClient
from typing import Dict, Any, Optional
from models.report import ReportType
from listeners.commands.decidely_list import report_service


def get_user_locale(client: WebClient, user_id: str) -> Optional[str]:
    """Get user's locale from Slack profile."""
    try:
        result = client.users_info(user=user_id)
        if result["ok"]:
            return result["user"].get("locale", "en_US")
    except Exception:
        pass
    return "en_US"


def get_localized_messages(locale: str) -> Dict[str, str]:
    """Get localized messages based on user locale."""
    messages = {
        "es": {
            "help_text": "ℹ️ Uso: `/decidely [autoridad|iniciativa] <descripción>`\n"
                         "O simplemente usa `/decidely` para abrir el formulario.",
            "help_blocks": "ℹ️ *Uso rápido:*\n"
                          "`/decidely autoridad no pude aprobar aumento de presupuesto`\n"
                          "`/decidely iniciativa miembro del equipo no corrigió error obvio`\n\n"
                          "*Atajos:* `fa` = faltó autoridad, `ie` = iniciativa esperada",
            "report_created": "✅ ¡Reporte creado!",
            "type_label": "*Tipo:*",
            "description_label": "*Descripción:*",
            "modal_title": "Reportar Decisión",
            "modal_submit": "Enviar",
            "modal_select_type": "Selecciona el tipo de situación:",
            "modal_select_placeholder": "Seleccionar tipo",
            "modal_authority_option": "🔒 Faltó Autoridad/Información",
            "modal_initiative_option": "💡 Iniciativa Esperada",
            "modal_description_label": "Descripción",
            "modal_description_placeholder": "Describe la situación..."
        },
        "en": {
            "help_text": "ℹ️ Usage: `/decidely [authority|initiative] <description>`\n"
                         "Or just use `/decidely` to open the form.",
            "help_blocks": "ℹ️ *Quick usage:*\n"
                          "`/decidely authority couldn't approve budget increase`\n"
                          "`/decidely initiative team member didn't fix obvious typo`\n\n"
                          "*Shortcuts:* `la` = lacked authority, `ei` = expected initiative",
            "report_created": "✅ Report created!",
            "type_label": "*Type:*",
            "description_label": "*Description:*",
            "modal_title": "Report Decision",
            "modal_submit": "Submit",
            "modal_select_type": "Select the type of situation:",
            "modal_select_placeholder": "Select type",
            "modal_authority_option": "🔒 Lacked Authority/Information",
            "modal_initiative_option": "💡 Expected Initiative",
            "modal_description_label": "Description",
            "modal_description_placeholder": "Describe the situation..."
        }
    }
    
    # Default to English if locale not found
    lang = locale[:2] if locale else "en"
    return messages.get(lang, messages["en"])


def decidely_report_callback(
    ack: Ack, 
    command: Dict[str, Any], 
    client: WebClient,
    respond: Respond
) -> None:
    print(f"📥 Received /decidely command from user {command.get('user_id')}")
    
    # Get command text
    text = command.get("text", "").strip()
    
    # Parse inline format: /decidely [authority|initiative] <description>
    if text:
        parts = text.split(" ", 1)
        if len(parts) >= 2:
            report_type_str = parts[0].lower()
            description = parts[1]
            
            # Map keywords to report types (English and Spanish)
            report_type = None
            if report_type_str in ["authority", "lacked", "la", "autoridad", "faltó", "fa"]:
                report_type = ReportType.LACKED_AUTHORITY
            elif report_type_str in ["initiative", "expected", "ei", "iniciativa", "esperaba", "ie"]:
                report_type = ReportType.EXPECTED_INITIATIVE
            
            # If we have valid type and description, create report directly
            if report_type and description:
                ack()
                
                # Create the report
                report = report_service.create_report(
                    user_id=command["user_id"],
                    workspace_id=command["team_id"],
                    report_type=report_type,
                    description=description
                )
                
                # Get user locale and messages
                locale = get_user_locale(client, command["user_id"])
                msgs = get_localized_messages(locale)
                
                # Confirm creation
                respond(
                    text=f"{msgs['report_created']} {report_type.value}",
                    blocks=[
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"{msgs['report_created']}\n{msgs['type_label']} {report_type.value}\n{msgs['description_label']} {description}"
                            }
                        }
                    ]
                )
                print(f"✅ Report created via inline command: {report_type.value} by {command['user_id']}")
                return
    
    # If we don't have complete inline data, show the form
    ack()
    
    # If text was provided but couldn't be parsed, show help
    if text and len(parts) < 2:
        # Get user locale and messages
        locale = get_user_locale(client, command["user_id"])
        msgs = get_localized_messages(locale)
        
        respond(
            text=msgs["help_text"],
            blocks=[
                {
                    "type": "section", 
                    "text": {
                        "type": "mrkdwn",
                        "text": msgs["help_blocks"]
                    }
                }
            ]
        )
        return
    
    # Get user locale and messages for modal
    locale = get_user_locale(client, command["user_id"])
    msgs = get_localized_messages(locale)
    
    view = {
        "type": "modal",
        "callback_id": "decidely_report_submission",
        "title": {
            "type": "plain_text",
            "text": msgs["modal_title"]
        },
        "submit": {
            "type": "plain_text",
            "text": msgs["modal_submit"]
        },
        "blocks": [
            {
                "type": "section",
                "block_id": "report_type_block",
                "text": {
                    "type": "mrkdwn",
                    "text": msgs["modal_select_type"]
                },
                "accessory": {
                    "type": "static_select",
                    "action_id": "report_type",
                    "placeholder": {
                        "type": "plain_text",
                        "text": msgs["modal_select_placeholder"]
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": msgs["modal_authority_option"]
                            },
                            "value": "lacked_authority"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": msgs["modal_initiative_option"]
                            },
                            "value": "expected_initiative"
                        }
                    ]
                }
            },
            {
                "type": "input",
                "block_id": "description_block",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "description",
                    "multiline": True,
                    "placeholder": {
                        "type": "plain_text",
                        "text": msgs["modal_description_placeholder"]
                    }
                },
                "label": {
                    "type": "plain_text",
                    "text": msgs["modal_description_label"]
                }
            }
        ]
    }
    
    client.views_open(
        trigger_id=command["trigger_id"],
        view=view
    )